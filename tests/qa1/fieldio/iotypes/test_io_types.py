import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - IoTypes")
class TestIoTypes:

    @allure.story("List IO Types")
    def test_get_io_types(self, fieldio_service):
        resp = fieldio_service.get_io_types()
        resp.assert_ok()

    @allure.story("Get IO Type by ID")
    def test_get_io_type_by_id(self, fieldio_service):
        resp = fieldio_service.get_io_type()
        resp.assert_ok()
