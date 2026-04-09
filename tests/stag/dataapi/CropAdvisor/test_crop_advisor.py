import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropAdvisor")
class TestCropAdvisor:
    @pytest.mark.flaky
    @allure.story("Get CropAdvisor by farmId")
    def test_get_crop_advisor_by_farm(self, dataapi_service):
        dataapi_service.get_crop_advisor().assert_any_of(200, 204, 404)
