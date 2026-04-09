import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropUnitsItemGroups")
class TestCropUnitsItemGroups:
    @allure.story("List ItemGroups for CropUnit")
    def test_list_item_groups(self, dataapi_service):
        dataapi_service.get_crop_unit_item_groups().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get ItemGroup by id for CropUnit")
    def test_get_item_group_by_id(self, dataapi_service):
        dataapi_service.get_crop_unit_item_group().assert_ok()
