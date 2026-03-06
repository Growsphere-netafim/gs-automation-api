import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Devices")
class TestFieldIODevices:

    @allure.story("List Devices")
    def test_get_devices(self, fieldio_service):
        resp = fieldio_service.get_devices()
        resp.assert_ok()

    @allure.story("Get Device by ID")
    def test_get_device_by_id(self, fieldio_service):
        resp = fieldio_service.get_device()
        resp.assert_ok()

    @allure.story("Get Device Address")
    def test_get_device_address(self, fieldio_service):
        resp = fieldio_service.get_device_address()
        resp.assert_ok()
