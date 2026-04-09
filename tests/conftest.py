"""
Pytest configuration and shared fixtures
Available to all tests
"""
import pytest
import requests
import os
import allure
from typing import Generator
import logging

from config.settings import Settings, get_settings
from core.token_manager import TokenManager


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
                "[!] Verify the service is running in the k8s cluster",
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
            f.write(f"Status=Active\n")
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


@pytest.fixture(scope="session")
def base_url_override(request) -> str:
    return request.config.getoption("--base-url")
