import pytest
from config.prod_config import ProdDeviceStateManagerConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.device_state_manager import DeviceStateManagerService

_fixtures = create_service_fixtures(ProdDeviceStateManagerConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def dsm_service(api, test_data):
    return DeviceStateManagerService(api, test_data)
