import allure

@allure.epic("Crop Service")
@allure.feature("ParameterPerStage")
class TestParameterPerStage:

    @allure.story("Get Parameters Per Stage")
    def test_get_parameter_per_stage(self, crop_service):
        resp = crop_service.get_parameter_per_stage()
        resp.assert_ok()

    @allure.story("Get Parameters Per Stage Lite")
    def test_get_parameter_per_stage_lite(self, crop_service):
        resp = crop_service.get_parameter_per_stage_lite()
        resp.assert_ok()
