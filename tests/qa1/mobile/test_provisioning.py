import allure


@allure.epic("Mobile BFF")
@allure.feature("Provisioning Controller")
class TestMobileProvisioning:

    @allure.story("Get Provisioning by Farm")
    def test_get_provisioning_by_farm(self, mobile_service):
        resp = mobile_service.get_provisioning_farm()
        resp.assert_any_of(200, 204)

    @allure.story("Get Provisioning Status by Flow UUID")
    def test_get_provisioning_status(self, mobile_service):
        resp = mobile_service.get_provisioning_status()
        resp.assert_ok()
