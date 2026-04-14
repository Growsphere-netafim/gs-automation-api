import allure


@allure.epic("Lookup Service")
@allure.feature("Timezones")
class TestTimezones:

    @allure.story("Get Timezones List")
    def test_get_timezones(self, lookup_service):
        lookup_service.get_timezones().assert_ok()

    @allure.story("Get Windows Timezones")
    def test_get_timezones_windows(self, lookup_service):
        lookup_service.get_timezones_windows().assert_ok()

    @allure.story("Get IANA Timezones")
    def test_get_timezones_iana(self, lookup_service):
        lookup_service.get_timezones_iana().assert_ok()
