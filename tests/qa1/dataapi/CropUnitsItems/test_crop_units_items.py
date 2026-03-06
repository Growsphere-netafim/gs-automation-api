import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropUnitsItems")
class TestCropUnitsItems:
    @pytest.mark.flaky
    # TODO: CropUnit 0a1e91a7-4223-4e9d-ba84-19d410de1753 has no ItemGroups in QA1.
    # To fix: find a cropUnitId that has ItemGroups and update DataAPIConfig.crop_unit_id
    @allure.story("List Items for ItemGroup in CropUnit")
    def test_list_items(self, dataapi_service):
        resp = dataapi_service.get_crop_unit_items()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: same as above — needs a valid cropUnitId with ItemGroups
    @allure.story("Get Item by id in ItemGroup for CropUnit")
    def test_get_item_by_id(self, dataapi_service):
        resp = dataapi_service.get_crop_unit_item()
        resp.assert_ok()
