import pytest
from config.china_stag_config import ChinaStagSettingsAPIConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.settings_api import SettingsAPIService

_fixtures = create_service_fixtures(ChinaStagSettingsAPIConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def settingsapi_service(api, test_data):
    return SettingsAPIService(api, test_data)
