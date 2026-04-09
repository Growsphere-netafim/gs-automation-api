import pytest
from config.stag_config import StagLookupServiceConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.lookup_service import LookupServiceService

_fixtures = create_service_fixtures(StagLookupServiceConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def lookup_service(api, test_data):
    return LookupServiceService(api, test_data)
