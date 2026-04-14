import allure


@allure.epic("CS API")
@allure.feature("Users")
class TestUsers:

    @allure.story("Get All Users")
    def test_get_users(self, csapi_service):
        csapi_service.get_users().assert_ok()

    @allure.story("Get User by ID")
    def test_get_user_by_id(self, csapi_service):
        csapi_service.get_user().assert_ok()

    @allure.story("Get User Roles")
    def test_get_user_roles(self, csapi_service):
        csapi_service.get_user_roles().assert_ok()

    @allure.story("Get User Farms")
    def test_get_user_farms(self, csapi_service):
        csapi_service.get_user_farms().assert_ok()
