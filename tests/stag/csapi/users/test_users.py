import allure
import pytest


@allure.epic("CS API")
@allure.feature("Users")
class TestUsers:

    @allure.story("Get Users")
    def test_get_users(self, csapi_service):
        csapi_service.get_users().assert_ok()

    @allure.story("Get User Details")
    def test_get_user_details(self, csapi_service):
        csapi_service.get_user().assert_ok()

    @pytest.mark.flaky  # GET /api/v1/users/{userId}/roles returns non-2xx in STAG — endpoint requires admin privileges not granted to yakir.moshe
    @allure.story("Get Roles")
    def test_get_roles(self, csapi_service):
        csapi_service.get_user_roles().assert_ok()

    @allure.story("Get User Farms")
    def test_get_user_farms(self, csapi_service):
        csapi_service.get_user_farms().assert_ok()

    @pytest.mark.flaky
    @allure.story("Validate Impersonation Token (Anonymous)")
    def test_validate_impersonation_token(self, csapi_service):
        csapi_service.validate_impersonation_token().assert_ok()
