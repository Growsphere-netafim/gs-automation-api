import allure


@allure.epic("Data API")
@allure.feature("CropProtocols")
class TestCropProtocols:

    @allure.story("Get Crop Protocols")
    def test_get_crop_protocols(self, dataapi_service):
        dataapi_service.get_crop_protocols().assert_ok()
