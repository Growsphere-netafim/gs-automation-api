import allure
import pytest


@allure.epic("CS API")
@allure.feature("Provisioning")
class TestProvisioning:

    @pytest.mark.flaky
    @allure.story("Get Active Provisioning Flow for Device")
    def test_get_active_flow_device(self, csapi_service):
        csapi_service.get_provisioning_device().assert_ok_or_skip_404(
            "Active provisioning flow not found for device"
        )

    @allure.story("Get Provision Steps")
    def test_get_provision_steps(self, csapi_service):
        csapi_service.get_provisioning_steps().assert_ok()

    @allure.story("Get Active Flows for Farm")
    def test_get_active_flows_farm(self, csapi_service):
        csapi_service.get_provisioning_farm().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Provisioning Flow")
    def test_get_provisioning_flow(self, csapi_service):
        csapi_service.get_provisioning_flow().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Flow Topology")
    def test_get_flow_topology(self, csapi_service):
        csapi_service.get_provisioning_topology().assert_ok()

    @allure.story("Get Provisioning Error Codes")
    def test_get_error_codes(self, csapi_service):
        csapi_service.get_provisioning_error_codes().assert_ok()
