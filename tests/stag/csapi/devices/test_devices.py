import allure
import pytest


@allure.epic("CS API")
@allure.feature("Devices")
class TestDevices:

    @allure.story("Get Device Registry Item")
    def test_get_device_registry_item(self, csapi_service):
        csapi_service.get_device().assert_ok()

    @allure.story("Get Devices by Enterprise")
    def test_get_devices_by_enterprise(self, csapi_service):
        csapi_service.get_devices_by_enterprise().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Device by Serial Number")
    def test_get_device_by_serial(self, csapi_service):
        csapi_service.get_device_by_serial().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Device Certificate")
    def test_get_device_certificate(self, csapi_service):
        csapi_service.get_device_cert().assert_ok_or_skip_404("Device certificate not found")

    @pytest.mark.flaky
    @allure.story("Get Device Private Key")
    def test_get_device_private_key(self, csapi_service):
        csapi_service.get_device_prkey().assert_ok_or_skip_404("Device private key not found")

    @pytest.mark.flaky
    @allure.story("Check Farm Assignability")
    def test_check_farm_assignability(self, csapi_service):
        csapi_service.get_device_assignable().assert_ok()

    @allure.story("Get PLC Hex Support Info")
    def test_get_plc_hex_support(self, csapi_service):
        csapi_service.get_device_hex_support().assert_ok()
