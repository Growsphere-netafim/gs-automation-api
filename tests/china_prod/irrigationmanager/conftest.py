import pytest
from config.china_prod_config import ChinaProdIrrigationManagerConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.irrigation_manager import IrrigationManagerService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = data.get("unitSystem", "Metric")
    client.headers["x-gs-farm-timezone"] = data.get("farmTimezone", "UTC")


_fixtures = create_service_fixtures(ChinaProdIrrigationManagerConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def irrigationmanager_service(api, test_data):
    return IrrigationManagerService(api, test_data)
