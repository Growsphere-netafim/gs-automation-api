import allure
import pytest


@allure.epic("CS API")
@allure.feature("Devices")
class TestDevices:

    @allure.story("Get Devices by Enterprise")
    def test_get_devices_by_enterprise(self, csapi_service):
        csapi_service.get_devices_by_enterprise().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Device by Serial")
    def test_get_device_by_serial(self, csapi_service):
        csapi_service.get_device_by_serial().assert_ok()
