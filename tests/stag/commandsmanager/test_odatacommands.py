import allure
import pytest

@allure.epic("Commands Manager Service")
@allure.feature("ODataCommands Controller")
class TestODataCommands:

    @allure.story("Get OData Commands (Global)")
    def test_get_odata_commands_global(self, commands_service):
        commands_service.get_odata_commands_global().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get OData Commands (Farm)")
    def test_get_odata_commands_farm(self, commands_service):
        commands_service.get_odata_commands_farm().assert_ok()
