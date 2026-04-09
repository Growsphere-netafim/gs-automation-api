import pytest
import allure

@allure.epic("Lookup Service")
@allure.feature("MeasureUnits")
class TestMeasureUnits:

    @allure.story("List measure units by unitSystem")
    def test_list_measure_units(self, lookup_service):
        lookup_service.get_measure_units().assert_ok()

    @allure.story("Get measure unit by id")
    def test_get_measure_unit_by_id(self, lookup_service):
        lookup_service.get_measure_unit().assert_ok()
