import allure

@allure.epic("Lookup Service")
@allure.feature("Countries")
class TestCountries:

    @allure.story("List countries")
    def test_list_countries(self, lookup_service):
        resp = lookup_service.get_countries()
        resp.assert_ok()

    @allure.story("Search countries by name")
    def test_search_countries_by_name(self, lookup_service):
        resp = lookup_service.get_countries(params={"name": "Isr"})
        resp.assert_ok()
