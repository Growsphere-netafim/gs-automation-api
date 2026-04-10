import allure
import pytest


@allure.epic("Field IO")
@allure.feature("FieldIO - Devices")
class TestFieldIODevices:

    @allure.story("List Devices")
    def test_get_devices(self, fieldio_service):
        fieldio_service.get_devices().assert_ok()

    @allure.story("Get Device by ID")
    def test_get_device_by_id(self, fieldio_service):
        fieldio_service.get_device().assert_ok()

    @pytest.mark.flaky  # GET /api/devices/{referenceId}/address returns 404 — A0PM5052-R-ETHL2200000242 has no address registered in STAG
    @allure.story("Get Device Address")
    def test_get_device_address(self, fieldio_service):
        fieldio_service.get_device_address().assert_ok()
