import allure


@allure.epic("Mobile BFF")
@allure.feature("Users Controller")
class TestMobileUsers:

    @allure.story("Get User Details")
    def test_get_user_details(self, mobile_service):
        resp = mobile_service.get_user_details()
        resp.assert_ok()

    @allure.story("Get User Graphs")
    def test_get_user_graphs(self, mobile_service):
        resp = mobile_service.get_user_graphs()
        resp.assert_ok()
