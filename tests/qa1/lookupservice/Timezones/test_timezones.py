import allure

@allure.epic("Lookup Service")
@allure.feature("Timezones")
class TestTimezones:

    @allure.story("List all timezones")
    def test_list_timezones(self, lookup_service):
        resp = lookup_service.get_timezones()
        resp.assert_ok()

    @allure.story("List Windows timezones")
    def test_list_windows_timezones(self, lookup_service):
        resp = lookup_service.get_timezones_windows()
        resp.assert_ok()

    @allure.story("List IANA timezones")
    def test_list_iana_timezones(self, lookup_service):
        resp = lookup_service.get_timezones_iana()
        resp.assert_ok()
