import pytest
from config.china_prod_config import ChinaProdIrrigationConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.irrigation import IrrigationService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = data.get("unitSystem", "SI")


_fixtures = create_service_fixtures(ChinaProdIrrigationConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def irrigation_service(api, test_data):
    return IrrigationService(api, test_data)
