import pytest
from config.qa1_config import CSAPIConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.settings_api import SettingsAPIService


class SettingsAPIConfig(CSAPIConfig):
    BASE_URL = "https://settingsapi-qa1.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
        "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
    })


_fixtures = create_service_fixtures(SettingsAPIConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def settingsapi_service(api, test_data):
    return SettingsAPIService(api, test_data)
