import allure


@allure.epic("Insights & Analytics")
@allure.feature("Weather Forecast")
class TestWeatherForecast:

    @allure.story("Get Forecast by Farm")
    def test_get_forecast(self, weatherforecast_service):
        weatherforecast_service.get_forecast().assert_ok()

    @allure.story("Get Historical Weather by Farm")
    def test_get_historical(self, weatherforecast_service):
        weatherforecast_service.get_historical().assert_ok()
