import allure


@allure.epic("CS API")
@allure.feature("TextResources")
class TestTextResources:

    @allure.story("Get App Ids")
    def test_get_app_ids(self, csapi_service):
        csapi_service.get_text_resource_app_ids().assert_ok()

    @allure.story("Get Text Resources (List)")
    def test_get_text_resources(self, csapi_service):
        csapi_service.get_text_resources().assert_ok()

    @allure.story("Get Text Resources by Category")
    def test_get_resources_by_category(self, csapi_service):
        csapi_service.get_text_resources_by_category().assert_ok()

    @allure.story("Get Text Resources by Key")
    def test_get_resources_by_key(self, csapi_service):
        csapi_service.get_text_resources_by_key().assert_ok()

    @allure.story("Get Text Resources by Key and Category")
    def test_get_resources_by_key_in_category(self, csapi_service):
        csapi_service.get_text_resources_by_key_and_category().assert_ok()

    @allure.story("Get Grouped Resources")
    def test_get_grouped_resources(self, csapi_service):
        csapi_service.get_text_resources_grouped().assert_ok()

    @allure.story("Get Grouped Resources by Category")
    def test_get_grouped_resources_by_category(self, csapi_service):
        csapi_service.get_text_resources_grouped_by_category().assert_ok()
