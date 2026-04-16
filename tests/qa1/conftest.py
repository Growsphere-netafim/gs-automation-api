import os
import logging
import pytest
import allure
import requests

from config.settings import get_settings
from core.token_manager import TokenManager
from api.client.api_client import QAApiClient
from core.test_data import TestData

log = logging.getLogger(__name__)


def create_service_fixtures(config_class, api_customizer=None):
    """Factory that returns a dict of common fixtures for a service.

    Args:
        config_class: The service config class (must have BASE_URL and TEST_DATA).
                      May optionally define IDS_URL, OIDC_CLIENT_ID, OIDC_REDIRECT_URI,
                      and ENV_NAME to override auth settings per environment (stag/prod).
        api_customizer: Optional callable(client, data) to customize the API client
                        (e.g. adding custom headers).

    Returns:
        Dict of fixture functions keyed by name.
    """
    # Read per-environment auth overrides from the config class (optional)
    _ids_url = getattr(config_class, 'IDS_URL', None)
    _client_id = getattr(config_class, 'OIDC_CLIENT_ID', None)
    _redirect_uri = getattr(config_class, 'OIDC_REDIRECT_URI', None)
    _scopes_val = getattr(config_class, 'SCOPES_VAL', None)
    _env_name = getattr(config_class, 'ENV_NAME', None)
    _user_email = getattr(config_class, 'USER_EMAIL', None)

    @pytest.fixture(scope="session")
    def settings():
        base = get_settings()
        overrides = {}
        if _ids_url:
            overrides["IDS_URL"] = _ids_url
        if _client_id:
            overrides["OIDC_CLIENT_ID"] = _client_id
        if _redirect_uri:
            overrides["OIDC_REDIRECT_URI"] = _redirect_uri
        if _scopes_val:
            overrides["SCOPES_VAL"] = _scopes_val
        if _env_name:
            overrides["ENV_NAME"] = _env_name
        if _user_email:
            overrides["USER_EMAIL"] = _user_email
        if overrides:
            return base.model_copy(update=overrides)
        return base

    @pytest.fixture(scope="session")
    def token_manager(settings):
        session = requests.Session()
        session.verify = False
        return TokenManager(session, settings.USER_EMAIL, settings)

    @pytest.fixture(scope="session")
    def auth_token(token_manager):
        pre_token = os.getenv("AUTH_TOKEN")
        if pre_token and TokenManager.is_token_valid(pre_token):
            log.info("Using pre-stored AUTH_TOKEN from environment (skipping login)")
            return pre_token
        if pre_token:
            log.warning("AUTH_TOKEN from environment is expired or invalid — falling back to OAuth2 login")
        try:
            return token_manager.get_or_fetch_token()
        except Exception as e:
            pytest.skip(f"Authentication failed — skipping all tests: {e}")

    @pytest.fixture(scope="session")
    def api(auth_token, data):
        if not auth_token:
            pytest.skip("No auth token available")
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
