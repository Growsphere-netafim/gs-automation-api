import allure


@allure.epic("System")
@allure.feature("Account Management")
class TestAccountManagement:

    @allure.story("License Management")
    def test_get_packages(self, accountmanagement_service):
        resp = accountmanagement_service.get_packages()
        resp.assert_ok()
