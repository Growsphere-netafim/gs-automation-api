import allure


@allure.epic("CS API")
@allure.feature("Versions")
class TestVersions:

    @allure.story("Get Versions")
    def test_get_versions(self, csapi_service):
        csapi_service.get_versions().assert_ok()
