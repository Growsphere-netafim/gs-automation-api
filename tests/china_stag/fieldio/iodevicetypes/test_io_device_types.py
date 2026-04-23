import allure


@allure.epic("Field IO")
@allure.feature("IO Device Types")
class TestIODeviceTypes:

    @allure.story("Get IO Device Types List")
    def test_get_io_device_types(self, fieldio_service):
        fieldio_service.get_io_device_types().assert_ok()

    @allure.story("Get IO Device Type by ID")
    def test_get_io_device_type_by_id(self, fieldio_service):
        fieldio_service.get_io_device_type().assert_ok()
