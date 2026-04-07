import allure

@allure.epic("Crop Service")
@allure.feature("IrrigationStrategies")
class TestIrrigationStrategies:

    @allure.story("Get Irrigation Strategies")
    def test_get_irrigation_strategies(self, crop_service):
        crop_service.get_irrigation_strategies().assert_ok()
