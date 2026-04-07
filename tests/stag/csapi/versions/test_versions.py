import allure
import pytest


@allure.epic("CS API")
@allure.feature("Versions")
class TestVersions:

    @allure.story("Get Versions")
    def test_get_versions(self, csapi_service):
        csapi_service.get_versions().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get PLC Version Details")
    def test_get_plc_version_details(self, csapi_service):
        csapi_service.get_version().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Version Details")
    def test_get_version_details(self, csapi_service):
        csapi_service.get_version_details().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Version File")
    def test_get_version_file(self, csapi_service):
        csapi_service.get_version_file().assert_ok()
