import allure
import pytest


@allure.epic("Field IO")
@allure.feature("FieldIO - Repeaters")
class TestRepeaters:

    @allure.story("List Repeaters")
    def test_get_repeaters(self, fieldio_service):
        fieldio_service.get_repeaters().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Repeater by ID")
    def test_get_repeater_by_id(self, fieldio_service):
        fieldio_service.get_repeater().assert_ok()
