import allure


@allure.epic("Agriculture")
@allure.feature("Irrigation Manager")
class TestIrrigationManager:

    @allure.story("Real-time Operations")
    def test_get_active_commands(self, irrigationmanager_service):
        irrigationmanager_service.get_active_commands().assert_ok()
