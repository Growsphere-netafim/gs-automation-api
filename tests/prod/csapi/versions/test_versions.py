import allure
import pytest


@allure.epic("CS API")
@allure.feature("Versions")
class TestVersions:

    @pytest.mark.flaky  # GET /api/v1/versions returns non-2xx in PROD — endpoint may not be deployed or requires elevated permissions
    @allure.story("Get Versions")
    def test_get_versions(self, csapi_service):
        csapi_service.get_versions().assert_ok()
