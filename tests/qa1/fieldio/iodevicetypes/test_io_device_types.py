import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - IoDeviceTypes")
class TestIoDeviceTypes:

    @allure.story("List IO Device Types")
    def test_get_io_device_types(self, fieldio_service):
        resp = fieldio_service.get_io_device_types()
        resp.assert_ok()

    @allure.story("Get IO Device Type by ID")
    def test_get_io_device_type_by_id(self, fieldio_service):
        resp = fieldio_service.get_io_device_type()
        resp.assert_ok()
