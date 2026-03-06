import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.lookup_service import LookupServiceEndpoints


class LookupServiceService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_countries(self, params: dict = None) -> ApiResponse:
        return self._client.get(LookupServiceEndpoints.countries(), params=params)

    def get_irrigation_methods(self, params: dict = None) -> ApiResponse:
        return self._client.get(LookupServiceEndpoints.irrigation_methods(), params=params)

    def get_irrigation_method(self) -> ApiResponse:
        if not self._data.irrigation_method_id:
            pytest.skip("irrigationMethodId not configured")
        return self._client.get(
            LookupServiceEndpoints.irrigation_method(self._data.irrigation_method_id)
        )

    def get_measure_units(self) -> ApiResponse:
        params = {}
        if self._data.unit_system:
            params["unitSystem"] = self._data.unit_system
        return self._client.get(LookupServiceEndpoints.measure_units(), params=params)

    def get_measure_unit(self) -> ApiResponse:
        if not self._data.uom_id:
            pytest.skip("uomId not configured")
        return self._client.get(LookupServiceEndpoints.measure_unit(self._data.uom_id))

    def get_states(self) -> ApiResponse:
        if not self._data.country_iso_symbol:
            pytest.skip("countryIsoSymbol not configured")
        return self._client.get(
            LookupServiceEndpoints.states(self._data.country_iso_symbol)
        )

    def get_timezones(self) -> ApiResponse:
        return self._client.get(LookupServiceEndpoints.timezones())

    def get_timezones_windows(self) -> ApiResponse:
        return self._client.get(LookupServiceEndpoints.timezones_windows())

    def get_timezones_iana(self) -> ApiResponse:
        return self._client.get(LookupServiceEndpoints.timezones_iana())
