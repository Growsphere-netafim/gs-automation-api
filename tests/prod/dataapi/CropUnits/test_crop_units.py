import allure


@allure.epic("Data API")
@allure.feature("CropUnits")
class TestCropUnits:
    @allure.story("Get CropUnit by id")
    def test_get_crop_unit_by_id(self, dataapi_service):
        dataapi_service.get_crop_unit().assert_ok()
