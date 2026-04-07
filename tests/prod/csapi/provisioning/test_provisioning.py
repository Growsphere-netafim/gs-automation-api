import allure


@allure.epic("CS API")
@allure.feature("Provisioning")
class TestProvisioning:

    @allure.story("Get Provision Steps")
    def test_get_provision_steps(self, csapi_service):
        csapi_service.get_provisioning_steps().assert_ok()

    @allure.story("Get Active Flows for Farm")
    def test_get_active_flows_farm(self, csapi_service):
        csapi_service.get_provisioning_farm().assert_ok()

    @allure.story("Get Provisioning Error Codes")
    def test_get_error_codes(self, csapi_service):
        csapi_service.get_provisioning_error_codes().assert_ok()
