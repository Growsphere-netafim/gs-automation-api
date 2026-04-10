import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropProtocols")
class TestCropProtocols:
    @pytest.mark.flaky  # cropProtocolId=10 does not exist in PROD DB — need to query /CropProtocols first and use a valid id from the PROD environment
    @allure.story("Get CropProtocols by cropProtocolId")
    def test_get_crop_protocol_by_id(self, dataapi_service):
        dataapi_service.get_crop_protocol().assert_ok()
