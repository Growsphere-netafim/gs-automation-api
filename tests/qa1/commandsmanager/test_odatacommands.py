import allure
import pytest

@allure.epic("Commands Manager Service")
@allure.feature("ODataCommands Controller")
class TestODataCommands:

    @allure.story("Get OData Commands (Global)")
    def test_get_odata_commands_global(self, commands_service):
        resp = commands_service.get_odata_commands_global()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: farm-specific OData endpoint returns 403 for all QA1 farms — requires elevated permissions not held by the test user.
    @allure.story("Get OData Commands (Farm)")
    def test_get_odata_commands_farm(self, commands_service):
        resp = commands_service.get_odata_commands_farm()
        resp.assert_ok()
