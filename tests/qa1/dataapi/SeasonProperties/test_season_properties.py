import allure
import pytest


@allure.epic("Data API")
@allure.feature("SeasonProperties")
class TestSeasonProperties:
    @pytest.mark.flaky
    # TODO: active season found in qa1-nb14218 has no SeasonProperties configured.
    # To fix: find a farmId + seasonId where GET /api/farms/{id}/Seasons/{id}/SeasonProperties returns 200
    @allure.story("Get SeasonProperties by farmId and seasonId")
    def test_get_season_properties(self, dataapi_service):
        resp = dataapi_service.get_season_properties()
        resp.assert_ok_or_skip_404("Season has no properties in this environment")
