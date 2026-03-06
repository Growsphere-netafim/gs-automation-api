import allure
import pytest


@allure.epic("Field IO")
@allure.feature("FieldIO - Repeaters")
class TestRepeaters:

    @allure.story("List Repeaters")
    def test_get_repeaters(self, fieldio_service):
        resp = fieldio_service.get_repeaters()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: no farm in QA1 has Repeaters configured.
    # To fix: find a farmId where GET /api/repeaters?farmId={id} returns non-empty list
    @allure.story("Get Repeater by ID")
    def test_get_repeater_by_id(self, fieldio_service):
        resp = fieldio_service.get_repeater()
        resp.assert_ok()
