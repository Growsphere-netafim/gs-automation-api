import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropUnitsItemGroups")
class TestCropUnitsItemGroups:
    @allure.story("List ItemGroups for CropUnit")
    def test_list_item_groups(self, dataapi_service):
        resp = dataapi_service.get_crop_unit_item_groups()
        resp.assert_ok()

    @pytest.mark.flaky
    # TODO: CropUnit 0a1e91a7-4223-4e9d-ba84-19d410de1753 has no ItemGroups in QA1.
    # To fix: find a cropUnitId that has ItemGroups and update DataAPIConfig.crop_unit_id
    @allure.story("Get ItemGroup by id for CropUnit")
    def test_get_item_group_by_id(self, dataapi_service):
        resp = dataapi_service.get_crop_unit_item_group()
        resp.assert_ok()
