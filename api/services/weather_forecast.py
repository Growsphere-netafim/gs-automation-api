import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.weather_forecast import WeatherForecastEndpoints


class WeatherForecastService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_forecast(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(WeatherForecastEndpoints.forecast(self._data.farm_id))

    def get_historical(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        params = {
            "startDate": self._data.start_date,
            "endDate": self._data.end_date
        }
        return self._client.get(WeatherForecastEndpoints.historical(self._data.farm_id), params=params)
