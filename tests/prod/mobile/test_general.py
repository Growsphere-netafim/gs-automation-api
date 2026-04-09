import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("General Controller")
class TestMobileGeneral:

    @allure.story("Get Notes")
    def test_get_notes(self, mobile_service):
        mobile_service.get_notes().assert_ok()

    @pytest.mark.flaky
    @allure.story("Gateway Dynamic Call")
    def test_gateway_dynamic_call(self, mobile_service):
        mobile_service.get_system_types().assert_ok()
