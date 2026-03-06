from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.account_management import AccountManagementEndpoints


class AccountManagementService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data

    def get_packages(self) -> ApiResponse:
        return self._client.get(AccountManagementEndpoints.packages())
