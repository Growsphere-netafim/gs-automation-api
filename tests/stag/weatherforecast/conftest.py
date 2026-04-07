import pytest
from config.stag_config import StagWeatherForecastConfig
from tests.qa1.conftest import create_service_fixtures
from api.services.weather_forecast import WeatherForecastService


def _customize_api(client, data):
    client.headers["x-nbvx-usr-pref-unit-system"] = "SI"


_fixtures = create_service_fixtures(StagWeatherForecastConfig, api_customizer=_customize_api)
settings = _fixtures["settings"]
token_manager = _fixtures["token_manager"]
auth_token = _fixtures["auth_token"]
api = _fixtures["api"]
data = _fixtures["data"]
test_data = _fixtures["test_data"]


@pytest.fixture(scope="session")
def weatherforecast_service(api, test_data):
    return WeatherForecastService(api, test_data)
