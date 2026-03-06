import allure


@allure.epic("Agriculture")
@allure.feature("Irrigation Manager")
class TestIrrigationManager:

    @allure.story("Real-time Operations")
    def test_get_active_commands(self, irrigationmanager_service):
        resp = irrigationmanager_service.get_active_commands()
        resp.assert_ok()
