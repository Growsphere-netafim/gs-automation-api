import allure


@allure.epic("Commands Manager Service")
@allure.feature("Commands Controller")
class TestCommands:

    @allure.story("Get Latest Command Statuses (Global)")
    def test_get_latest_command_statuses_global(self, commands_service):
        commands_service.get_latest_statuses_global().assert_ok()
