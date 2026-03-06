import pytest
import allure

@allure.epic("Commands Manager Service")
@allure.feature("Commands Controller")
class TestCommands:

    @allure.story("Get Command Status")
    def test_get_command_status(self, commands_service):
        resp = commands_service.get_command_status()
        resp.assert_ok()

    @allure.story("Get Latest Command Statuses (Farm)")
    def test_get_latest_command_statuses_farm(self, commands_service):
        resp = commands_service.get_latest_statuses_farm()
        resp.assert_ok()

    @allure.story("Get Latest Command Statuses (Global)")
    def test_get_latest_command_statuses_global(self, commands_service):
        resp = commands_service.get_latest_statuses_global()
        resp.assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Latest Command Status (Device Request)")
    def test_get_latest_command_status_device_request(self, commands_service):
        resp = commands_service.get_device_request_latest()
        resp.assert_ok_or_skip_404("Command Request not found (404)")
