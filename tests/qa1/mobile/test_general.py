import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("General Controller")
class TestMobileGeneral:

    @allure.story("Get Notes")
    def test_get_notes(self, mobile_service):
        resp = mobile_service.get_notes()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: gateway dynamic call for system types returns 400 in QA1 (FieldIO service error).
    # Infrastructure issue — endpoint intermittently broken in this environment.
    @allure.story("Gateway Dynamic Call")
    def test_gateway_dynamic_call(self, mobile_service):
        resp = mobile_service.get_system_types()
        resp.assert_ok()
