import allure


@allure.epic("CS API")
@allure.feature("Provisioning")
class TestProvisioning:

    @allure.story("Get Provisioning Steps")
    def test_get_provisioning_steps(self, csapi_service):
        csapi_service.get_provisioning_steps().assert_ok()

    @allure.story("Get Provisioning Error Codes")
    def test_get_provisioning_error_codes(self, csapi_service):
        csapi_service.get_provisioning_error_codes().assert_ok()

    @allure.story("Get Provisioning Farm")
    def test_get_provisioning_farm(self, csapi_service):
        csapi_service.get_provisioning_farm().assert_ok()
