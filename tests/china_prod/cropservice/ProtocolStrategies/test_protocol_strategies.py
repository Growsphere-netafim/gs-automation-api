import allure


@allure.epic("Crop Service")
@allure.feature("Protocol Strategies")
class TestProtocolStrategies:

    @allure.story("Get Protocol Strategies List")
    def test_get_protocol_strategies(self, crop_service):
        crop_service.get_protocol_strategies().assert_ok()

    @allure.story("Get Protocol Strategy by ID")
    def test_get_protocol_strategy_by_id(self, crop_service):
        crop_service.get_protocol_strategy().assert_ok()
