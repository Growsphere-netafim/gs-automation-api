import allure

@allure.epic("Crop Service")
@allure.feature("ParameterPerVarieties")
class TestParameterPerVarieties:

    @allure.story("Get Parameters Per Varieties")
    def test_get_parameter_per_varieties(self, crop_service):
        crop_service.get_parameter_per_varieties().assert_ok()

    @allure.story("Get Parameters Per Varieties Lite")
    def test_get_parameter_per_varieties_lite(self, crop_service):
        crop_service.get_parameter_per_varieties_lite().assert_ok()
