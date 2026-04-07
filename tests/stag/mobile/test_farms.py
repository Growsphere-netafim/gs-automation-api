import allure
import pytest


@allure.epic("Mobile BFF")
@allure.feature("Farms Controller")
class TestMobileFarms:

    @allure.story("Get IO List")
    def test_get_io_list(self, mobile_service):
        mobile_service.get_io_list().assert_ok()

    @allure.story("Get Trees")
    def test_get_trees(self, mobile_service):
        mobile_service.get_trees().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Dashboard Data")
    def test_get_dashboard_data(self, mobile_service):
        mobile_service.get_dashboard_data().assert_ok()

    @allure.story("Get HomePage Devices")
    def test_get_homepage_devices(self, mobile_service):
        mobile_service.get_homepage_devices().assert_ok()
