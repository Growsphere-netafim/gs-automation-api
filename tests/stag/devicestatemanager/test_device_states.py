import allure

@allure.epic("Device State Manager")
@allure.feature("Device States Controller")
class TestDeviceStates:

    @allure.story("Get Device State by ID")
    def test_get_device_state_by_id(self, dsm_service):
        dsm_service.get_device_state_by_id().assert_ok()

    @allure.story("Get Device State by UUID")
    def test_get_device_state_by_uuid(self, dsm_service):
        dsm_service.get_device_state_by_uuid().assert_ok()

    @allure.story("Get Device States by Farm ID")
    def test_get_device_states_by_farm_id(self, dsm_service):
        dsm_service.get_device_states_by_farm().assert_ok()
