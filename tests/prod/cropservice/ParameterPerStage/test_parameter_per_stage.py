import allure

@allure.epic("Crop Service")
@allure.feature("ParameterPerStage")
class TestParameterPerStage:

    @allure.story("Get Parameters Per Stage")
    def test_get_parameter_per_stage(self, crop_service):
        crop_service.get_parameter_per_stage().assert_ok()

    @allure.story("Get Parameters Per Stage Lite")
    def test_get_parameter_per_stage_lite(self, crop_service):
        crop_service.get_parameter_per_stage_lite().assert_ok()
