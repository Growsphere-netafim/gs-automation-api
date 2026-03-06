import allure

@allure.epic("Lookup Service")
@allure.feature("States")
class TestStates:

    @allure.story("List states by country ISO symbol")
    def test_list_states(self, lookup_service):
        resp = lookup_service.get_states()
        resp.assert_ok()
