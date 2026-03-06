import allure


@allure.epic("Field IO")
@allure.feature("FieldIO - Connections")
class TestConnections:

    @allure.story("Get Davis Weather Station Connections")
    def test_get_davis_ws_connections(self, fieldio_service):
        resp = fieldio_service.get_davis_ws_connections()
        resp.assert_ok()
