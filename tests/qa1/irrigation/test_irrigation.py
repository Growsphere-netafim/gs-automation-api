import allure

@allure.epic("Irrigation Service")
@allure.feature("Irrigation Controller")
class TestIrrigation:

    @allure.story("Get IO Modes")
    def test_get_io_modes(self, irrigation_service):
        resp = irrigation_service.get_io_modes()
        resp.assert_ok()

    @allure.story("Get Last Irrigation")
    def test_get_last_irrigation(self, irrigation_service):
        resp = irrigation_service.get_last_irrigation()
        resp.assert_ok()

    @allure.story("Get Last Eco Daily Program Scheme")
    def test_get_last_eco_daily_program_scheme(self, irrigation_service):
        resp = irrigation_service.get_last_eco_daily_program_scheme()
        resp.assert_ok()

    @allure.story("Get Daily Irrigation")
    def test_get_daily_irrigation(self, irrigation_service):
        resp = irrigation_service.get_daily_irrigation()
        resp.assert_ok()

    @allure.story("Get Daily Eco Flex Report")
    def test_get_daily_eco_flex_report(self, irrigation_service):
        resp = irrigation_service.get_daily_eco_flex_report()
        resp.assert_ok()

    @allure.story("Get Eco Flex Controller Report")
    def test_get_eco_flex_controller_report(self, irrigation_service):
        resp = irrigation_service.get_eco_flex_controller_report()
        resp.assert_ok()

    @allure.story("Get Mainline by ID")
    def test_get_mainline_by_id(self, irrigation_service):
        resp = irrigation_service.get_mainline()
        resp.assert_ok()

    @allure.story("Get Device Mainlines")
    def test_get_device_mainlines(self, irrigation_service):
        resp = irrigation_service.get_device_mainlines()
        resp.assert_ok()

    @allure.story("Get OData Alarms")
    def test_get_odata_alarms(self, irrigation_service):
        resp = irrigation_service.get_odata_alarms()
        resp.assert_ok()

    @allure.story("Get OData Irrigation Logs")
    def test_get_odata_irrigation_logs(self, irrigation_service):
        resp = irrigation_service.get_odata_irrigation_logs()
        resp.assert_ok()

    @allure.story("Get Program Schemes")
    def test_get_program_schemes(self, irrigation_service):
        resp = irrigation_service.get_program_schemes()
        resp.assert_ok()

    @allure.story("Get Program Scheme by UUID")
    def test_get_program_scheme_by_uuid(self, irrigation_service):
        resp = irrigation_service.get_program_scheme()
        resp.assert_ok()

    @allure.story("Get Irrigation Programs Status")
    def test_get_irrigation_programs_status(self, irrigation_service):
        resp = irrigation_service.get_irrigation_programs_status()
        resp.assert_ok()

    @allure.story("Get Recipes")
    def test_get_recipes(self, irrigation_service):
        resp = irrigation_service.get_recipes()
        resp.assert_ok()
