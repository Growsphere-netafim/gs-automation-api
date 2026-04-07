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

    @allure.story("Get PLC Hex Support Info")
    def test_get_plc_hex_support(self, csapi_service):
        csapi_service.get_device_hex_support().assert_ok()
