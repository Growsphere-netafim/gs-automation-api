import allure


@allure.epic("CS API")
@allure.feature("Enterprises")
class TestEnterprises:

    @allure.story("Get All Enterprises")
    def test_get_enterprises(self, csapi_service):
        csapi_service.get_enterprises().assert_ok()

    @allure.story("Get Enterprise by ID")
    def test_get_enterprise_by_id(self, csapi_service):
        csapi_service.get_enterprise().assert_ok()

    @allure.story("Get Enterprise IDs")
    def test_get_enterprise_ids(self, csapi_service):
        csapi_service.get_enterprise_ids().assert_ok()

    @allure.story("Get Enterprise Farms")
    def test_get_enterprise_farms(self, csapi_service):
        csapi_service.get_enterprise_farms().assert_ok()

    @allure.story("Get Enterprise Users Details")
    def test_get_enterprise_users_details(self, csapi_service):
        csapi_service.get_enterprise_users_details().assert_ok()

    # test_get_enterprise_hierarchy excluded — enterprise 3001 has no hierarchy registered in China prod (returns 404)
