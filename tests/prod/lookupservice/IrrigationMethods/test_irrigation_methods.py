import pytest
import allure

@allure.epic("Lookup Service")
@allure.feature("IrrigationMethods")
class TestIrrigationMethods:

    @allure.story("List irrigation methods")
    def test_list_irrigation_methods(self, lookup_service):
        lookup_service.get_irrigation_methods().assert_ok()

    @allure.story("Search irrigation methods by name")
    def test_search_irrigation_methods_by_name(self, lookup_service):
        lookup_service.get_irrigation_methods(params={"name": "drip"}).assert_ok()

    @allure.story("Get irrigation method by id")
    def test_get_irrigation_method_by_id(self, lookup_service):
        lookup_service.get_irrigation_method().assert_ok()
