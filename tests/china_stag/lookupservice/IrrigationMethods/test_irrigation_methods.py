import allure


@allure.epic("Lookup Service")
@allure.feature("Irrigation Methods")
class TestIrrigationMethods:

    @allure.story("Get Irrigation Methods List")
    def test_get_irrigation_methods(self, lookup_service):
        lookup_service.get_irrigation_methods().assert_ok()

    @allure.story("Get Irrigation Method by ID")
    def test_get_irrigation_method_by_id(self, lookup_service):
        lookup_service.get_irrigation_method().assert_ok()
