import allure


@allure.epic("Data API")
@allure.feature("CropProtocols")
class TestCropProtocols:
    @allure.story("Get CropProtocols by cropProtocolId")
    def test_get_crop_protocol_by_id(self, dataapi_service):
        dataapi_service.get_crop_protocol().assert_ok()

    @allure.story("List CropProtocols by farmId")
    def test_list_crop_protocols(self, dataapi_service):
        dataapi_service.get_crop_protocols().assert_ok()

    @allure.story("List deleted CropProtocols by farmId")
    def test_list_deleted_crop_protocols(self, dataapi_service):
        dataapi_service.get_crop_protocols_deleted().assert_ok()
