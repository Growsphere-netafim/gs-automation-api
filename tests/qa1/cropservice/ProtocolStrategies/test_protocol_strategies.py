import allure

@allure.epic("Crop Service")
@allure.feature("ProtocolStrategies")
class TestProtocolStrategies:

    @allure.story("Get Protocol Strategies")
    def test_get_protocol_strategies(self, crop_service):
        resp = crop_service.get_protocol_strategies()
        resp.assert_ok()

    @allure.story("Get Protocol Strategy by ID")
    def test_get_protocol_strategy_by_id(self, crop_service):
        resp = crop_service.get_protocol_strategy()
        resp.assert_ok()
