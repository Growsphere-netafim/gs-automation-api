import allure


@allure.epic("Field IO")
@allure.feature("IO Types")
class TestIOTypes:

    @allure.story("Get IO Types List")
    def test_get_io_types(self, fieldio_service):
        fieldio_service.get_io_types().assert_ok()

    @allure.story("Get IO Type by ID")
    def test_get_io_type_by_id(self, fieldio_service):
        fieldio_service.get_io_type().assert_ok()
