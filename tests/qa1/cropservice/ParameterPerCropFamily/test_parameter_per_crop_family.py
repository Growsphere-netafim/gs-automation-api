import allure

@allure.epic("Crop Service")
@allure.feature("ParameterPerCropFamily")
class TestParameterPerCropFamily:

    @allure.story("Get Parameters Per Crop Family")
    def test_get_parameter_per_crop_family(self, crop_service):
        resp = crop_service.get_parameter_per_crop_family()
        resp.assert_ok()
