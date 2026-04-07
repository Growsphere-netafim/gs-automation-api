import allure


@allure.epic("Lookup Service")
@allure.feature("Timezones")
class TestTimezones:

    @allure.story("List all timezones")
    def test_list_timezones(self, lookup_service):
        lookup_service.get_timezones().assert_ok()

    @allure.story("List timezones with pageSize")
    def test_list_timezones_paged(self, lookup_service):
        lookup_service.get_timezones().assert_ok()

    @allure.story("List Windows timezones")
    def test_list_windows_timezones(self, lookup_service):
        lookup_service.get_timezones_windows().assert_ok()

    @allure.story("List IANA timezones")
    def test_list_iana_timezones(self, lookup_service):
        lookup_service.get_timezones_iana().assert_ok()
