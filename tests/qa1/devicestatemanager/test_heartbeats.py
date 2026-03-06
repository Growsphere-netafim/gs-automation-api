import allure

@allure.epic("Device State Manager")
@allure.feature("Heartbeats Controller")
class TestHeartbeats:

    @allure.story("Get Heartbeats by Range")
    def test_get_heartbeats(self, dsm_service):
        resp = dsm_service.get_heartbeats()
        resp.assert_ok()

    @allure.story("Query Heartbeats by Range and Device IDs")
    def test_query_heartbeats(self, dsm_service):
        resp = dsm_service.query_heartbeats()
        resp.assert_ok()
