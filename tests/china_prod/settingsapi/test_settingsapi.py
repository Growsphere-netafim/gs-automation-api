import allure


@allure.epic("Settings API")
@allure.feature("Settings Controller")
class TestSettings:

    @allure.story("Get Device Alert Settings")
    def test_get_alert_settings(self, settingsapi_service):
        settingsapi_service.get_alert_settings().assert_ok()
