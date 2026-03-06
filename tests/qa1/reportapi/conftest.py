import pytest
from config.qa1_config import ReportAPIConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.report_api import ReportAPIService

_fixtures = create_service_fixtures(ReportAPIConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def reportapi_service(api, test_data):
    return ReportAPIService(api, test_data)
