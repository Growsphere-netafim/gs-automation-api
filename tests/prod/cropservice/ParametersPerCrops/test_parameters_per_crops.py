import allure

@allure.epic("Crop Service")
@allure.feature("ParametersPerCrops")
class TestParametersPerCrops:

    @allure.story("Get Parameters Per Crops")
    def test_get_parameters_per_crops(self, crop_service):
        crop_service.get_parameters_per_crops().assert_ok()
