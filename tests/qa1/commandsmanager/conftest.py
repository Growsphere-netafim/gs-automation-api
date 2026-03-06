import pytest
from config.qa1_config import CommandsManagerConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.commands_manager import CommandsManagerService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = data.get("unitSystem", "Metric")
    client.headers["x-gs-farm-timezone"] = data.get("farmTimezone", "UTC")


_fixtures = create_service_fixtures(CommandsManagerConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def commands_service(api, test_data):
    return CommandsManagerService(api, test_data)
