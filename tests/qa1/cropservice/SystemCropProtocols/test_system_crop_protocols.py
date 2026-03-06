import pytest
import allure

@allure.epic("Crop Service")
@allure.feature("SystemCropProtocols")
class TestSystemCropProtocols:

    @pytest.mark.flaky
    @allure.story("Get System Crop Protocols")
    def test_get_system_crop_protocols(self, crop_service):
        resp = crop_service.get_system_crop_protocols()
        resp.assert_ok()
