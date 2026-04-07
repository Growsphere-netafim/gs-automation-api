import pytest
import allure


@allure.epic("Data API")
@allure.feature("Geolocation")
class TestGeolocation:
    @pytest.mark.flaky
    @allure.story("Get Geolocation by irrigationBlockId")
    def test_get_geolocation(self, dataapi_service):
        dataapi_service.get_geolocation().assert_ok()
