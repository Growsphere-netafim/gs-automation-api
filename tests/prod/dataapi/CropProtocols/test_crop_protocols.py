import allure


@allure.epic("Data API")
@allure.feature("CropProtocols")
class TestCropProtocols:
    @allure.story("Get CropProtocols by cropProtocolId")
    def test_get_crop_protocol_by_id(self, dataapi_service):
        dataapi_service.get_crop_protocol().assert_ok()
