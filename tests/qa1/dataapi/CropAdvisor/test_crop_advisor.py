import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropAdvisor")
class TestCropAdvisor:
    @pytest.mark.flaky
    # TODO: endpoint returns 500 in QA1 (server-side issue, not data related)
    @allure.story("Get CropAdvisor by farmId")
    def test_get_crop_advisor_by_farm(self, dataapi_service):
        resp = dataapi_service.get_crop_advisor()
        resp.assert_any_of(200, 204, 404)
