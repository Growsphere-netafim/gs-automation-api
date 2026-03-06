import allure
import pytest


@allure.epic("CS API")
@allure.feature("Versions")
class TestVersions:

    @allure.story("Get Versions")
    def test_get_versions(self, csapi_service):
        csapi_service.get_versions().assert_ok()

    @pytest.mark.flaky
    # TODO: version blob not found in QA1 blob storage for any version from GET /api/v1/Versions.
    # To fix: find a version ID that exists in blob storage via GET /api/v1/Versions/{id}
    @allure.story("Get PLC Version Details")
    def test_get_plc_version_details(self, csapi_service):
        csapi_service.get_version().assert_ok()

    @pytest.mark.flaky
    # TODO: version details not found in QA1 blob storage for the FLEX system type.
    # To fix: find a version ID that has VersionDetails for the configured systemType.
    @allure.story("Get Version Details")
    def test_get_version_details(self, csapi_service):
        csapi_service.get_version_details().assert_ok()

    @pytest.mark.flaky
    # TODO: version file not found in QA1 blob storage for the FLEX system type.
    # To fix: find a version ID that has a version file for the configured systemType.
    @allure.story("Get Version File")
    def test_get_version_file(self, csapi_service):
        csapi_service.get_version_file().assert_ok()
