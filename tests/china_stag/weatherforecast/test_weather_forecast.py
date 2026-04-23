import allure
import pytest


@allure.epic("Insights & Analytics")
@allure.feature("Weather Forecast")
class TestWeatherForecast:

    @pytest.mark.flaky
    @allure.story("Get Forecast by Farm")
    def test_get_forecast(self, weatherforecast_service):
        weatherforecast_service.get_forecast().assert_ok_or_skip_404("No forecast data for configured farm in china prod")

    @pytest.mark.flaky
    @allure.story("Get Historical Weather by Farm")
    def test_get_historical(self, weatherforecast_service):
        weatherforecast_service.get_historical().assert_ok_or_skip_404("No historical data for configured farm in china prod")
