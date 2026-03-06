import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("Irrigation Controller")
class TestMobileIrrigation:

    @allure.story("Get Farm Program Schemes")
    def test_get_farm_program_schemes(self, mobile_service):
        resp = mobile_service.get_farm_program_schemes()
        resp.assert_ok()

    @allure.story("Get Device Program Schemes")
    def test_get_device_program_schemes(self, mobile_service):
        resp = mobile_service.get_device_program_schemes()
        resp.assert_ok()

    @allure.story("Get Specific Program Scheme")
    def test_get_specific_program_scheme(self, mobile_service):
        resp = mobile_service.get_program_scheme()
        resp.assert_ok()

    @allure.story("Get Program Scheme Status")
    def test_get_program_scheme_status(self, mobile_service):
        resp = mobile_service.get_program_scheme_status()
        resp.assert_ok()

    @allure.story("Get Device Program Schemes Statuses")
    def test_get_device_program_schemes_statuses(self, mobile_service):
        resp = mobile_service.get_device_program_schemes_statuses()
        resp.assert_ok()

    @allure.story("Get Irrigation Programs")
    def test_get_irrigation_programs(self, mobile_service):
        resp = mobile_service.get_irrigation_programs()
        resp.assert_ok()

    @allure.story("Get Daily Irrigation Programs")
    def test_get_daily_irrigation_programs(self, mobile_service):
        resp = mobile_service.get_irrigation_programs_daily()
        resp.assert_ok()

    @allure.story("Get Last Irrigation for Program")
    def test_get_last_irrigation(self, mobile_service):
        resp = mobile_service.get_last_irrigation()
        resp.assert_any_of(200, 204)

    @allure.story("Get Device Irrigation Blocks")
    def test_get_device_irrigation_blocks(self, mobile_service):
        resp = mobile_service.get_device_irrigation_blocks()
        resp.assert_ok()

    @allure.story("Get All Irrigation Blocks")
    def test_get_all_irrigation_blocks(self, mobile_service):
        resp = mobile_service.get_irrigation_blocks()
        resp.assert_ok()

    @allure.story("Get Max Program Overview")
    def test_get_max_program_overview(self, mobile_service):
        resp = mobile_service.get_max_program_overview()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: program has no active progress data in QA1 — requires an actively running irrigation program.
    # To fix: trigger irrigation on the configured device before running this test.
    @allure.story("Get Program Progress")
    def test_get_program_progress(self, mobile_service):
        resp = mobile_service.get_program_progress()
        resp.assert_ok()
