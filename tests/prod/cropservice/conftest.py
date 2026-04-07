import pytest
from config.prod_config import ProdCropServiceConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.crop_service import CropServiceService

_fixtures = create_service_fixtures(ProdCropServiceConfig)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def crop_service(api, test_data):
    return CropServiceService(api, test_data)
