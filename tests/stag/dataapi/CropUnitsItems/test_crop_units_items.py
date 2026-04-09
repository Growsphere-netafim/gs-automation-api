import allure
import pytest


@allure.epic("Data API")
@allure.feature("CropUnitsItems")
class TestCropUnitsItems:
    @pytest.mark.flaky
    @allure.story("List Items for ItemGroup in CropUnit")
    def test_list_items(self, dataapi_service):
        dataapi_service.get_crop_unit_items().assert_ok()

    @pytest.mark.flaky
    @allure.story("Get Item by id in ItemGroup for CropUnit")
    def test_get_item_by_id(self, dataapi_service):
        dataapi_service.get_crop_unit_item().assert_ok()
