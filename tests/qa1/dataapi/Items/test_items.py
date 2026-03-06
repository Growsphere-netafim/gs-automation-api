import allure
import pytest


@allure.epic("Data API")
@allure.feature("Items")
class TestItems:
    @pytest.mark.flaky
    # TODO: requires a valid itemId resolved from a farm ItemGroup.
    # Same dependency as FarmsItems — needs a farmId with non-empty ItemGroup/Items
    @allure.story("Get Item by itemId")
    def test_get_item_by_id(self, dataapi_service):
        resp = dataapi_service.get_item()
        resp.assert_ok()
