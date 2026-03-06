class WeatherForecastEndpoints:
    @staticmethod
    def forecast(farm_id: str) -> str:
        return f"api/CurrentWeather/{farm_id}"

    @staticmethod
    def historical(farm_id: str) -> str:
        return f"api/farms/{farm_id}/dailyData"
