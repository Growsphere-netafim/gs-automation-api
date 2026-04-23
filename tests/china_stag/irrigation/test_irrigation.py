import allure
import pytest


@allure.epic("Irrigation Service")
@allure.feature("Irrigation Controller")
class TestIrrigation:

    @allure.story("Get IO Modes")
    def test_get_io_modes(self, irrigation_service):
        irrigation_service.get_io_modes().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Last Irrigation")
    def test_get_last_irrigation(self, irrigation_service):
        irrigation_service.get_last_irrigation().assert_ok_or_skip_404("No irrigation data in china prod for configured farm")

    @pytest.mark.flaky
    @allure.story("Get Program Schemes")
    def test_get_program_schemes(self, irrigation_service):
        irrigation_service.get_program_schemes().assert_ok_or_skip_404("No program schemes in china prod for configured farm")

    @pytest.mark.flaky
    @allure.story("Get Recipes")
    def test_get_recipes(self, irrigation_service):
        irrigation_service.get_recipes().assert_ok_or_skip_404("No recipes in china prod for configured farm")
