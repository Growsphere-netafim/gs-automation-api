import allure


@allure.epic("Commands Manager Service")
@allure.feature("ODataCommands Controller")
class TestODataCommands:

    @allure.story("Get OData Commands (Global)")
    def test_get_odata_commands_global(self, commands_service):
        commands_service.get_odata_commands_global().assert_ok()
