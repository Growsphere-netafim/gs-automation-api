import pytest
from config.prod_config import ProdAccountManagementConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.account_management import AccountManagementService

_fixtures = create_service_fixtures(ProdAccountManagementConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def accountmanagement_service(api, test_data):
    return AccountManagementService(api, test_data)
