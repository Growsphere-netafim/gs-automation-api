import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - IO")
class TestIO:

    @allure.story("Get IO by ID")
    def test_get_io_by_id(self, fieldio_service):
        resp = fieldio_service.get_io()
        resp.assert_ok()

    @allure.story("List IOs")
    def test_get_ios(self, fieldio_service):
        resp = fieldio_service.get_ios()
        resp.assert_ok()
