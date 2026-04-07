import allure


@allure.epic("Data API")
@allure.feature("CropModel")
class TestCropModel:
    @allure.story("Get CropModel CropUnits by farmId and cropUnitId")
    def test_get_crop_model_crop_units(self, dataapi_service):
        dataapi_service.get_crop_model_crop_units().assert_any_of(200, 204)

    @allure.story("Get CropModel ResponseData by farmId and date parts")
    def test_get_crop_model_response_data(self, dataapi_service):
        dataapi_service.get_crop_model_response_data().assert_any_of(200, 204)
