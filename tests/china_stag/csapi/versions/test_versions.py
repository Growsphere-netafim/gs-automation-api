import allure
import pytest


@allure.epic("CS API")
@allure.feature("Versions")
class TestVersions:

    @allure.story("Get Versions List")
    def test_get_versions(self, csapi_service):
        csapi_service.get_versions().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Version by ID")
    def test_get_version(self, csapi_service):
        csapi_service.get_version().assert_ok()
