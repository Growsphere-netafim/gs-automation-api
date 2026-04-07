import allure


@allure.epic("CS API")
@allure.feature("Farms")
class TestFarms:

    @allure.story("Get All Farms")
    def test_get_all_farms(self, csapi_service):
        csapi_service.get_farms().assert_ok()

    @allure.story("Get Enterprise Farms (Alt)")
    def test_get_enterprise_farms_alt(self, csapi_service):
        csapi_service.get_farms_by_enterprise().assert_ok()

    @allure.story("Get Farm by ID")
    def test_get_farm_by_id(self, csapi_service):
        csapi_service.get_farm().assert_ok()

    @allure.story("Get Farm Users Details")
    def test_get_farm_users_details(self, csapi_service):
        csapi_service.get_farm_users_details().assert_ok()

    @allure.story("Get Farm Roles")
    def test_get_farm_roles(self, csapi_service):
        csapi_service.get_farm_roles().assert_ok()

    @allure.story("Get Enterprise Category by Farm ID")
    def test_get_enterprise_category_by_farm(self, csapi_service):
        csapi_service.get_farm_enterprise_category().assert_ok()
