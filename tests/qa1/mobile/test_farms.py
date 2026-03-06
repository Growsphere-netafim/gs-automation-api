import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("Farms Controller")
class TestMobileFarms:

    @allure.story("Get IO List")
    def test_get_io_list(self, mobile_service):
        resp = mobile_service.get_io_list()
        resp.assert_ok()

    @allure.story("Get Trees")
    def test_get_trees(self, mobile_service):
        resp = mobile_service.get_trees()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: dashboard data returns 409 for qa1-nb10047 (farm conflict/state issue).
    # To fix: find a farmId where GET /api/Mobile/Dashboard/data/farm/{id} returns 200.
    @allure.story("Get Dashboard Data")
    def test_get_dashboard_data(self, mobile_service):
        resp = mobile_service.get_dashboard_data()
        resp.assert_ok()

    @allure.story("Get HomePage Devices")
    def test_get_homepage_devices(self, mobile_service):
        resp = mobile_service.get_homepage_devices()
        resp.assert_ok()
