"""
Pytest configuration and shared fixtures
Available to all tests
"""
import pytest
import requests
import os
import json
import allure
from typing import Generator, List, Dict
import logging

from config.settings import Settings, get_settings
from core.token_manager import TokenManager
from api.endpoints.farms import FarmsAPI


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()

    from helpers.allure_helpers import log_response

    def allure_logger(response, *args, **kwargs):
        log_response(response)

    session.hooks['response'].append(allure_logger)

    yield session
    session.close()


@pytest.fixture(scope="function")
def test_user_email(settings: Settings) -> str:
    return settings.USER_EMAIL


@pytest.fixture(scope="function")
def farms_api(api_session: requests.Session, test_user_email: str) -> FarmsAPI:
    return FarmsAPI(api_session, test_user_email)


@pytest.fixture(scope="function")
def cleanup_farms(farms_api: FarmsAPI, settings: Settings) -> Generator[List[str], None, None]:
    farms_to_cleanup = []

    yield farms_to_cleanup

    if settings.should_cleanup():
        for farm_id in farms_to_cleanup:
            try:
                farms_api.delete_farm(farm_id)
                logging.info(f"Cleaned up farm: {farm_id}")
            except Exception as e:
                logging.warning(f"Failed to cleanup farm {farm_id}: {e}")


@pytest.fixture(scope="function")
def test_farm_data(settings: Settings) -> Dict:
    try:
        from helpers.data_generator import generate_farm_data
        return generate_farm_data(name_prefix=settings.TEST_FARM_PREFIX)
    except ImportError:
        return {
            "farmName": f"{settings.TEST_FARM_PREFIX}Default",
            "location": "Test Location"
        }


@pytest.fixture(scope="function")
def created_test_farm(
    farms_api: FarmsAPI,
    test_farm_data: Dict,
    cleanup_farms: List[str]
) -> Dict:
    response = farms_api.create_farm(test_farm_data)
    farm = farms_api.get_json(response)

    cleanup_farms.append(farm['farmId'])

    return farm


@pytest.fixture(scope="function")
def mock_api(settings: Settings):
    import responses as responses_lib

    if settings.USE_MOCKS:
        with responses_lib.RequestsMock() as rsps:
            yield rsps
    else:
        yield None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and call.excinfo is not None:
        import requests.exceptions as req_exc

        exc_type = call.excinfo.type
        exc_val = call.excinfo.value
        test_name = item.name
        url = ""
        if hasattr(exc_val, "request") and exc_val.request:
            url = str(exc_val.request.url)

        diagnosis = None

        if exc_type in (req_exc.ReadTimeout, req_exc.ConnectTimeout, req_exc.Timeout):
            diagnosis = "\n".join([
                "=" * 60,
                "NETWORK FAILURE DIAGNOSIS  —  TIMEOUT",
                "=" * 60,
                f"Error Type : {exc_type.__name__}",
                f"Test       : {test_name}",
                f"URL        : {url or '(unknown)'}",
                "",
                "WHY IT FAILED",
                "-" * 40,
                "The server did not respond within the 30-second timeout.",
                "This is NOT an HTTP error — the connection was made but",
                "the server never completed the response.",
                "",
                "POSSIBLE CAUSES",
                "-" * 40,
                "* The endpoint runs a heavy query without pagination (e.g. OData without $top)",
                "* The service pod is overloaded or under k8s resource pressure",
                "* The endpoint requires filter parameters to reduce the dataset",
                "* Background maintenance or a cold-start is blocking the pod",
                "",
                "WHAT THE API NEEDS TO WORK",
                "-" * 40,
                "* Add $top / $skip OData params to paginate: ?$top=10&$skip=0",
                "* Add a farmId filter header or query param to reduce scope",
                "* Add a date range filter if the endpoint supports it",
                "",
                "RECOMMENDATIONS",
                "-" * 40,
                "[!] Add ?$top=10 to the OData endpoint URL to limit results",
                "[!] Check k8s pod health for this service",
                "[!] Try the endpoint manually with Postman to confirm it responds",
                "[!] Consider increasing timeout for OData-heavy endpoints (e.g. 60s)",
                "=" * 60,
            ])

        elif issubclass(exc_type, req_exc.ConnectionError):
            diagnosis = "\n".join([
                "=" * 60,
                "NETWORK FAILURE DIAGNOSIS  —  CONNECTION ERROR",
                "=" * 60,
                f"Error Type : {exc_type.__name__}",
                f"Test       : {test_name}",
                f"URL        : {url or '(unknown)'}",
                f"Details    : {str(exc_val)[:300]}",
                "",
                "WHY IT FAILED",
                "-" * 40,
                "Could not establish a connection to the server.",
                "The host may be unreachable, DNS may have failed, or VPN is not active.",
                "",
                "RECOMMENDATIONS",
                "-" * 40,
                "[!] Check VPN / network connectivity to *.k8s.growsphere.netafim.com",
                "[!] Verify the service is running in the QA1 k8s cluster",
                "[!] Confirm the hostname/URL is correct",
                "=" * 60,
            ])

        if diagnosis:
            print(f"\n{diagnosis}")
            with allure.step(f"Network Failure — {exc_type.__name__}"):
                allure.attach(
                    diagnosis,
                    name=f"[NETWORK ERROR] {exc_type.__name__} — {test_name}",
                    attachment_type=allure.attachment_type.TEXT
                )


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data_before_run(settings: Settings):
    if settings.should_cleanup():
        logging.info("Cleaning up test data before run...")

        session = requests.Session()
        session.verify = False

        try:
            farms_api = FarmsAPI(session, settings.USER_EMAIL)
            deleted = farms_api.delete_farms_by_prefix(settings.TEST_FARM_PREFIX)
            logging.info(f"Cleaned up {deleted} test farms")
        except Exception as e:
            logging.warning(f"Pre-run cleanup failed: {e}")
        finally:
            session.close()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data_after_run(settings: Settings):
    yield

    if settings.should_cleanup():
        logging.info("Cleaning up test data after run...")

        session = requests.Session()
        session.verify = False

        try:
            farms_api = FarmsAPI(session, settings.USER_EMAIL)
            deleted = farms_api.delete_farms_by_prefix(settings.TEST_FARM_PREFIX)
            logging.info(f"Cleaned up {deleted} test farms")
        except Exception as e:
            logging.warning(f"Post-run cleanup failed: {e}")
        finally:
            session.close()


@pytest.fixture(scope="function")
def wait_for_condition():
    import time

    def _wait(condition_func, timeout=30, interval=1):
        start_time = time.time()

        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)

        return False

    return _wait


def pytest_addoption(parser):
    parser.addoption(
        "--bearer",
        action="store",
        default=os.getenv("API_BEARER", ""),
        help="Bearer token for API authentication"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("API_BASE_URL", ""),
        help="Override base URL for Swagger tests"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_allure_environment(request, settings):
    alluredir = request.config.getoption("--alluredir")
    if alluredir:
        if not os.path.exists(alluredir):
            os.makedirs(alluredir, exist_ok=True)

        env_file = os.path.join(alluredir, "environment.properties")
        with open(env_file, "w") as f:
            f.write(f"Environment={settings.ENV_NAME}\n")
            f.write(f"User={settings.USER_EMAIL}\n")
            f.write(f"IDS_URL={settings.IDS_URL}\n")
            f.write(f"QA1_Status=Active\n")
            f.write(f"Framework=Pytest-Automation-Architect\n")


@pytest.fixture(scope="function")
def bearer_token(request, api_session) -> str:
    cli_token = request.config.getoption("--bearer")
    if cli_token:
        return cli_token

    settings = get_settings()
    if settings.PASSWORD:
        token_manager = TokenManager(api_session, settings.USER_EMAIL, settings)
        return token_manager.get_or_fetch_token()

    return ""


@pytest.fixture(scope="session")
def smoke_farm_id(request, api_session, settings) -> str:
    """Session-scoped: discover a real farm ID from QA1 for smoke tests."""
    token = request.config.getoption("--bearer", default="")
    if not token and settings.PASSWORD:
        token = TokenManager(api_session, settings.USER_EMAIL, settings).get_or_fetch_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "x-nbvx-client-app-name": "Growsphere-Automation"
    }
    url = "https://csapi-qa1.k8s.growsphere.netafim.com/api/v1/farms"
    try:
        response = api_session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            farms = data if isinstance(data, list) else data.get("farms", [])
            if farms:
                return farms[0].get("id") or farms[0].get("farmId")
    except Exception:
        pass
    logging.warning("smoke_farm_id: could not discover farm from csapi, falling back to config default")
    return "qa1-nb10000"


@pytest.fixture(scope="function")
def farm_id(api_session, bearer_token) -> str:
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
        "x-nbvx-client-app-name": "Growsphere-Automation"
    }

    url_toolbox = "https://csapi-qa1.k8s.growsphere.netafim.com/api/v1/techtoolbox/Filters/Dashboard"
    try:
        with allure.step("Discovery Strategy 1: TechToolbox Meta-Dashboard"):
            response = api_session.get(url_toolbox, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                farms_group = next((item for item in data if item["id"] == "farms"), None)
                if farms_group and farms_group.get("values"):
                    fid = farms_group["values"][0]["id"]
                    allure.dynamic.parameter("Discovery Source", "TechToolbox")
                    return fid
    except: pass

    url_csapi = "https://csapi-qa1.k8s.growsphere.netafim.com/api/v1/farms"
    try:
        with allure.step("Discovery Strategy 2: CSAPI Farms List"):
            response = api_session.get(url_csapi, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                farms = data if isinstance(data, list) else data.get("farms", [])
                if farms:
                    fid = farms[0].get("id") or farms[0].get("farmId")
                    return fid
    except: pass

    url_fieldio = "https://fieldio-qa1.k8s.growsphere.netafim.com/api/bases"
    try:
        with allure.step("Discovery Strategy 3 (Fallback): FieldIO Bases"):
            response = api_session.get(url_fieldio, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                bases = data if isinstance(data, list) else data.get("bases", [])
                if bases and bases[0].get("farmId"):
                    fid = bases[0]["farmId"]
                    return fid
    except: pass

    logging.warning("Discovery: Failed to find any active Farm ID across all sources.")
    return None


@pytest.fixture(scope="function")
def device_context(api_session, bearer_token, farm_id):
    if not farm_id: return None

    url = f"https://fieldio-qa1.k8s.growsphere.netafim.com/api/devices?farmId={farm_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Accept": "application/json"}
    try:
        with allure.step(f"Discovery: Fetching devices for farm {farm_id}"):
            response = api_session.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                devices = []
                if isinstance(data, list): devices = data
                elif isinstance(data, dict): devices = data.get("devices", [])

                if devices:
                    device = devices[0]
                    ctx = {
                        "deviceUuid": device.get("deviceUuid"),
                        "deviceId": device.get("deviceId"),
                        "name": device.get("deviceName")
                    }
                    allure.dynamic.parameter("Discovered Device UUID", ctx["deviceUuid"])
                    return ctx
    except: pass
    return None


@pytest.fixture(scope="function")
def crop_unit_context(api_session, bearer_token, farm_id):
    if not farm_id: return None

    url = f"https://cropservice-qa1.k8s.growsphere.netafim.com/api/CropUnits?farmId={farm_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Accept": "application/json"}
    try:
        with allure.step(f"Discovery: Fetching crop units for farm {farm_id}"):
            response = api_session.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                units = []
                if isinstance(data, list): units = data
                elif isinstance(data, dict): units = data.get("cropUnits") or data.get("items", [])

                if units:
                    unit = units[0]
                    ctx = {
                        "cropUnitId": unit.get("cropUnitId"),
                        "name": unit.get("cropUnitName")
                    }
                    allure.dynamic.parameter("Discovered Crop Unit ID", ctx["cropUnitId"])
                    return ctx
    except: pass
    return None


@pytest.fixture(scope="session")
def base_url_override(request) -> str:
    return request.config.getoption("--base-url")
