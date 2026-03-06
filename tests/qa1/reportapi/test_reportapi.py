import pytest
import allure

@allure.epic("Report API")
@allure.feature("Configuration Controller")
class TestConfiguration:

    @allure.story("Get Configuration by User ID")
    def test_get_configuration_by_user_id(self, reportapi_service):
        resp = reportapi_service.get_configuration()
        resp.assert_ok()

@allure.epic("Report API")
@allure.feature("ReportsPreferences Controller")
class TestReportsPreferences:

    @pytest.mark.flaky
    @allure.story("Get Reports Preferences by Farm ID")
    def test_get_reports_preferences_by_farm_id(self, reportapi_service):
        resp = reportapi_service.get_reports_preferences()
        resp.assert_ok()
