import allure


@allure.epic("Crop Service")
@allure.feature("Irrigation Strategies")
class TestIrrigationStrategies:

    @allure.story("Get Irrigation Strategies List")
    def test_get_irrigation_strategies(self, crop_service):
        crop_service.get_irrigation_strategies().assert_ok()
