import os
import pytest
import allure
import requests

from config.settings import get_settings
from core.token_manager import TokenManager
from api.client.api_client import QAApiClient
from core.test_data import TestData


def create_service_fixtures(config_class, api_customizer=None):
    """Factory that returns a dict of common fixtures for a service.

    Args:
        config_class: The service config class (must have BASE_URL and TEST_DATA).
        api_customizer: Optional callable(client, data) to customize the API client
                        (e.g. adding custom headers).

    Returns:
        Dict of fixture functions keyed by name.
    """

    @pytest.fixture(scope="session")
    def settings():
        return get_settings()

    @pytest.fixture(scope="session")
    def token_manager(settings):
        session = requests.Session()
        session.verify = False
        return TokenManager(session, settings.USER_EMAIL, settings)

    @pytest.fixture(scope="session")
    def auth_token(token_manager):
        try:
            return token_manager.get_or_fetch_token()
        except Exception as e:
            print(f"Failed to get token: {e}")
            return None

    @pytest.fixture(scope="session")
    def api(auth_token, data):
        client = QAApiClient(base_url=config_class.BASE_URL, token=auth_token)
        if api_customizer:
            api_customizer(client, data)
        return client

    @pytest.fixture(scope="session")
    def data():
        return config_class.TEST_DATA

    @pytest.fixture(scope="session")
    def test_data():
        return TestData.from_dict(config_class.TEST_DATA)

    return {
        "settings": settings,
        "token_manager": token_manager,
        "auth_token": auth_token,
        "api": api,
        "data": data,
        "test_data": test_data,
    }


@pytest.fixture(autouse=True)
def set_allure_suites(request):
    try:
        path = str(request.node.fspath)
    except Exception:
        path = ""
    parts = path.split("/tests/qa1/")[-1].split("/") if "/tests/qa1/" in path else []
    parent = "QA1"
    suite = parts[0] if parts and parts[0] else "qa1"
    filename = os.path.basename(path) if path else ""
    name_no_ext = os.path.splitext(filename)[0] if filename else ""
    sub = parts[1] if len(parts) > 1 else name_no_ext
    allure.dynamic.parent_suite(parent)
    allure.dynamic.suite(suite)
    if sub:
        allure.dynamic.sub_suite(sub)
