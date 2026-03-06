import pytest
from config.qa1_config import MobileConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.mobile import MobileService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = data.get("unitSystem", "Metric")
    client.headers["x-gs-farm-timezone"] = data.get("farmTimezone", "UTC")
    client.headers["farmId"] = data.get("farmId")


_fixtures = create_service_fixtures(MobileConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def mobile_service(api, test_data):
    return MobileService(api, test_data)
