import allure


@allure.epic("Lookup Service")
@allure.feature("States")
class TestStates:

    @allure.story("Get States by Country ISO")
    def test_get_states_by_country(self, lookup_service):
        lookup_service.get_states().assert_ok()
