import pytest
from config.stag_config import StagCSAPIConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.csapi import CSAPIService

_fixtures = create_service_fixtures(StagCSAPIConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def dashboard_filters():
    return StagCSAPIConfig.DASHBOARD_FILTERS


@pytest.fixture(scope="session")
def csapi_service(api, test_data):
    return CSAPIService(api, test_data)
