import allure


@allure.epic("Field IO")
@allure.feature("System Types")
class TestSystemTypes:

    @allure.story("Get System Types List")
    def test_get_system_types(self, fieldio_service):
        fieldio_service.get_system_types().assert_ok()

    @allure.story("Get System Type by ID")
    def test_get_system_type_by_id(self, fieldio_service):
        fieldio_service.get_system_type().assert_ok()
