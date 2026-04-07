import pytest
from config.prod_config import ProdDataAPIConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.data_api import DataAPIService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = "SI"
    client.headers["x-gs-farm-timezone"] = "Israel Standard Time"


_fixtures = create_service_fixtures(ProdDataAPIConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def dataapi_service(api, test_data):
    return DataAPIService(api, test_data)
