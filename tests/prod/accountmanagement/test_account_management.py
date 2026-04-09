import allure


@allure.epic("System")
@allure.feature("Account Management")
class TestAccountManagement:

    @allure.story("License Management")
    def test_get_packages(self, accountmanagement_service):
        accountmanagement_service.get_packages().assert_ok()
