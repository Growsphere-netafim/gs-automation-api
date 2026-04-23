import allure
import pytest


@allure.epic("Device State Manager")
@allure.feature("Device States Controller")
class TestDeviceStates:

    @pytest.mark.flaky
    @allure.story("Get Device States by Farm ID")
    def test_get_device_states_by_farm_id(self, dsm_service):
        dsm_service.get_device_states_by_farm().assert_ok_or_skip_404("Farm not found in china prod")
