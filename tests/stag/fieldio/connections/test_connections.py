import allure
import pytest


@allure.epic("Field IO")
@allure.feature("FieldIO - Connections")
class TestConnections:

    @pytest.mark.flaky  # Davis weather station not configured in STAG — no Davis WS device exists for this farm/user
    @allure.story("Get Davis Weather Station Connections")
    def test_get_davis_ws_connections(self, fieldio_service):
        fieldio_service.get_davis_ws_connections().assert_ok()
