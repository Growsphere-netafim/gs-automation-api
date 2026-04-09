import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("Reports Controller")
class TestMobileReports:

    @pytest.mark.flaky
    @allure.story("Get Last Eco Daily Program Report")
    def test_get_last_eco_daily_program_report(self, mobile_service):
        mobile_service.get_last_eco_daily_program_report().assert_any_of(200, 204)

    @allure.story("Get Daily Report")
    def test_get_daily_report(self, mobile_service):
        mobile_service.get_daily_report().assert_any_of(200, 204)

    @allure.story("Get Irrigation Logs")
    def test_get_irrigation_logs(self, mobile_service):
        mobile_service.get_irrigation_logs().assert_any_of(200, 204)
