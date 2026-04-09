import allure
import pytest


@allure.epic("Data API")
@allure.feature("SeasonProperties")
class TestSeasonProperties:
    @pytest.mark.flaky
    @allure.story("Get SeasonProperties by farmId and seasonId")
    def test_get_season_properties(self, dataapi_service):
        dataapi_service.get_season_properties().assert_ok_or_skip_404("Season has no properties in this environment")
