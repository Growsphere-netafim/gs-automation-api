import allure


@allure.epic("Lookup Service")
@allure.feature("Measure Units")
class TestMeasureUnits:

    @allure.story("Get Measure Units List")
    def test_get_measure_units(self, lookup_service):
        lookup_service.get_measure_units().assert_ok()

    @allure.story("Get Measure Unit by ID")
    def test_get_measure_unit_by_id(self, lookup_service):
        lookup_service.get_measure_unit().assert_ok()
