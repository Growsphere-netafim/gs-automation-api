import pytest
import allure


@allure.epic("Mobile BFF")
@allure.feature("Devices Controller")
class TestMobileDevices:

    @allure.story("Get Device State")
    def test_get_device_state(self, mobile_service):
        resp = mobile_service.get_device_state()
        resp.assert_ok()

    @allure.story("Check Device Assignable")
    def test_device_assignable(self, mobile_service):
        resp = mobile_service.get_device_assignable()
        resp.assert_any_of(200, 204)

    @allure.story("Get General Settings")
    def test_get_general_settings(self, mobile_service):
        resp = mobile_service.get_general_settings()
        resp.assert_ok()

    @allure.story("Get Alert Settings")
    def test_get_alert_settings(self, mobile_service):
        resp = mobile_service.get_alert_settings()
        resp.assert_ok()

    @allure.story("Get Delay Settings")
    def test_get_delay_settings(self, mobile_service):
        resp = mobile_service.get_delay_settings()
        resp.assert_ok()

    @allure.story("Get Device States by Farm")
    def test_get_device_states_by_farm(self, mobile_service):
        resp = mobile_service.get_device_states_by_farm()
        resp.assert_ok()

    @allure.story("Get Device Connection Status")
    def test_get_device_connection_status(self, mobile_service):
        resp = mobile_service.get_device_connection_status()
        resp.assert_ok()

    @allure.story("Get Device Tree")
    def test_get_device_tree(self, mobile_service):
        resp = mobile_service.get_device_tree()
        resp.assert_ok()

    @allure.story("Get Device Details")
    def test_get_device_details(self, mobile_service):
        resp = mobile_service.get_device_details()
        resp.assert_ok()

    @allure.story("Get Device Recipes")
    def test_get_device_recipes(self, mobile_service):
        resp = mobile_service.get_device_recipes()
        resp.assert_ok()

    @allure.story("Get Device Recipes With Usage")
    def test_get_device_recipes_with_usage(self, mobile_service):
        resp = mobile_service.get_device_recipes_with_usage()
        resp.assert_ok()

    @allure.story("Get User Device Graphs")
    def test_get_user_device_graphs(self, mobile_service):
        resp = mobile_service.get_user_device_graphs()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: no user device graphs saved for the configured farm/device in QA1.
    # To fix: save a user device graph for the configured farmId+deviceId combination.
    @allure.story("Get Specific User Device Graph")
    def test_get_specific_user_device_graph(self, mobile_service):
        graphs_resp = mobile_service.get_user_device_graphs()
        graphs_resp.assert_ok()
        graphs = graphs_resp.json()
        graph_id = (graphs[0] if isinstance(graphs, list) and graphs else {}).get("id")
        if not graph_id:
            pytest.skip("No user device graphs found")
        resp = mobile_service.get_user_device_graph(graph_id)
        resp.assert_ok_or_skip_404("User Device Graph not found")
