import allure

@allure.epic("Device State Manager")
@allure.feature("Device States Controller")
class TestDeviceStates:

    @allure.story("Get Device State by ID")
    def test_get_device_state_by_id(self, dsm_service):
        resp = dsm_service.get_device_state_by_id()
        resp.assert_ok()

    @allure.story("Get Device State by UUID")
    def test_get_device_state_by_uuid(self, dsm_service):
        resp = dsm_service.get_device_state_by_uuid()
        resp.assert_ok()

    @allure.story("Get Device States by Farm ID")
    def test_get_device_states_by_farm_id(self, dsm_service):
        resp = dsm_service.get_device_states_by_farm()
        resp.assert_ok()
