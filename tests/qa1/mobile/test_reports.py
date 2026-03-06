import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("Reports Controller")
class TestMobileReports:

    @pytest.mark.flaky
    # TODO: eco daily program report availability depends on the daily report job having run for some farm.
    # The report is time-dependent; farms in the fallback list may return 400 if no report exists for today.
    @allure.story("Get Last Eco Daily Program Report")
    def test_get_last_eco_daily_program_report(self, mobile_service):
        resp = mobile_service.get_last_eco_daily_program_report()
        resp.assert_any_of(200, 204)

    @allure.story("Get Daily Report")
    def test_get_daily_report(self, mobile_service):
        resp = mobile_service.get_daily_report()
        resp.assert_any_of(200, 204)

    @allure.story("Get Irrigation Logs")
    def test_get_irrigation_logs(self, mobile_service):
        resp = mobile_service.get_irrigation_logs()
        resp.assert_any_of(200, 204)
