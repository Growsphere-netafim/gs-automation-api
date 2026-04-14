import allure


@allure.epic("Lookup Service")
@allure.feature("Countries")
class TestCountries:

    @allure.story("List Countries")
    def test_list_countries(self, lookup_service):
        lookup_service.get_countries().assert_ok()

    @allure.story("Search Countries by Name")
    def test_search_countries_by_name(self, lookup_service):
        lookup_service.get_countries(params={"name": "Chi"}).assert_ok()
