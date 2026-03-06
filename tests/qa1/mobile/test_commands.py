import allure


@allure.epic("Mobile BFF")
@allure.feature("Commands Controller")
class TestMobileCommands:

    @allure.story("Get Command by Reference ID")
    def test_get_command_by_reference_id(self, mobile_service):
        resp = mobile_service.get_command()
        resp.assert_ok()

    @allure.story("Get Commands by Farm and Device")
    def test_get_commands_by_farm_and_device(self, mobile_service):
        resp = mobile_service.get_commands_by_farm_device()
        resp.assert_ok()

    @allure.story("Get Commands List for Device")
    def test_get_commands_list(self, mobile_service):
        resp = mobile_service.get_commands_list()
        resp.assert_ok()

    @allure.story("Request Command")
    def test_request_command(self, mobile_service):
        resp = mobile_service.request_command()
        resp.assert_any_of(200, 204)
