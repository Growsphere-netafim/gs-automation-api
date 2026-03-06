import allure

@allure.epic("Crop Service")
@allure.feature("ParameterPerProtocolStrategy")
class TestParameterPerProtocolStrategy:

    @allure.story("Get Parameters Per Protocol Strategy")
    def test_get_parameter_per_protocol_strategy(self, crop_service):
        resp = crop_service.get_parameter_per_protocol_strategy()
        resp.assert_ok()
