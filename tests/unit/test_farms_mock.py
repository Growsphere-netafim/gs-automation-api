"""
Unit tests for Farms API using mocks
Fast tests that don't require real API
"""
import pytest
import responses
import unittest
from requests import Session

from api.endpoints.farms import FarmsAPI
from mocks.mock_responses import MockResponses, MockFactory
from config.settings import get_settings


@pytest.mark.mock
class TestFarmsAPIMocked:
    """
    Test Farms API with mocked responses
    These tests run fast and don't need network
    """

    @pytest.fixture(autouse=True)
    def mock_token_manager(self):
        """Mock TokenManager to avoid complex auth flow"""
        with unittest.mock.patch("core.token_manager.TokenManager.get_token", return_value="mock_token"):
            yield

    @responses.activate
    def test_get_all_farms_success(self):
        """Test getting list of farms with mock"""
        settings = get_settings()
        base_url = f"{settings.base_urls['csapi_url']}/farms"

        responses.add(
            responses.GET,
            base_url,
            json=MockResponses.farm_list(count=5),
            status=200
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")

        response = farms_api.get_all_farms()

        assert response.status_code == 200
        data = response.json()
        assert len(data['farms']) == 5
        assert data['total'] == 5

    @responses.activate
    def test_get_farm_by_id_success(self):
        """Test getting single farm by ID"""
        settings = get_settings()
        farm_id = "farm-001"
        url = f"{settings.base_urls['csapi_url']}/farms/{farm_id}"

        responses.add(
            responses.GET,
            url,
            json=MockResponses.single_farm(farm_id),
            status=200
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")
        response = farms_api.get_farm_by_id(farm_id)

        assert response.status_code == 200
        farm = response.json()
        assert farm['farmId'] == farm_id
        assert 'farmName' in farm
        assert 'location' in farm

    @responses.activate
    def test_create_farm_success(self):
        """Test creating new farm"""
        settings = get_settings()
        base_url = f"{settings.base_urls['csapi_url']}/farms"

        farm_data = {
            "farmName": "New Test Farm",
            "area": 150,
            "areaUnit": "hectare"
        }

        responses.add(
            responses.POST,
            base_url,
            json=MockResponses.created_farm(farm_data),
            status=201
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")
        response = farms_api.create_farm(farm_data)

        assert response.status_code == 201
        created_farm = response.json()
        assert created_farm['farmName'] == farm_data['farmName']
        assert 'farmId' in created_farm

    @responses.activate
    def test_delete_farm_success(self):
        """Test deleting farm"""
        settings = get_settings()
        farm_id = "farm-001"
        url = f"{settings.base_urls['csapi_url']}/farms/{farm_id}"

        responses.add(
            responses.DELETE,
            url,
            json=MockResponses.deleted_farm(),
            status=200
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")
        response = farms_api.delete_farm(farm_id)

        assert response.status_code == 200
        result = response.json()
        assert result['success'] is True

    @responses.activate
    def test_get_farm_by_id_not_found(self):
        """Test handling of farm not found"""
        settings = get_settings()
        farm_id = "nonexistent-farm"
        url = f"{settings.base_urls['csapi_url']}/farms/{farm_id}"

        responses.add(
            responses.GET,
            url,
            json=MockResponses.error_response(404, "Farm not found"),
            status=404
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")

        with pytest.raises(AssertionError) as exc_info:
            farms_api.get_farm_by_id(farm_id)

        assert "Failed to get farm" in str(exc_info.value)

    @responses.activate
    def test_get_farms_by_prefix(self):
        """Test filtering farms by name prefix"""
        settings = get_settings()
        base_url = f"{settings.base_urls['csapi_url']}/farms"

        mock_farms = {
            "farms": [
                {"farmId": "f1", "farmName": "TEST_FARM_1"},
                {"farmId": "f2", "farmName": "TEST_FARM_2"},
                {"farmId": "f3", "farmName": "PROD_FARM_1"},
                {"farmId": "f4", "farmName": "TEST_FARM_3"},
            ],
            "total": 4
        }

        responses.add(
            responses.GET,
            base_url,
            json=mock_farms,
            status=200
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")
        farm_ids = farms_api.get_farm_ids_by_name_prefix("TEST_FARM_")

        assert len(farm_ids) == 3
        assert "f1" in farm_ids
        assert "f2" in farm_ids
        assert "f4" in farm_ids
        assert "f3" not in farm_ids

    @responses.activate
    def test_create_farm_validation_error(self):
        """Test handling of validation errors"""
        settings = get_settings()
        base_url = f"{settings.base_urls['csapi_url']}/farms"

        invalid_farm_data = {
            "farmName": "",
            "area": -10
        }

        responses.add(
            responses.POST,
            base_url,
            json=MockResponses.validation_error(
                "farmName",
                "Farm name cannot be empty"
            ),
            status=400
        )

        session = Session()
        farms_api = FarmsAPI(session, "test@example.com")

        with pytest.raises(AssertionError) as exc_info:
            farms_api.create_farm(invalid_farm_data)

        assert "400" in str(exc_info.value) or "Failed to create farm" in str(exc_info.value)


@pytest.mark.mock
class TestMockFactory:
    """Test the mock factory utilities"""

    def test_create_multiple_farms(self):
        """Test creating multiple mock farms"""
        farms = MockFactory.create_farms(count=10, name_prefix="MyFarm")

        assert len(farms) == 10
        assert all("farmId" in farm for farm in farms)
        assert all(farm["farmName"].startswith("MyFarm") for farm in farms)

    def test_create_farm_with_devices(self):
        """Test creating farm with devices"""
        farm = MockFactory.create_farm_with_devices("farm-123", device_count=5)

        assert farm["farmId"] == "farm-123"
        assert len(farm["devices"]) == 5
        assert all("deviceId" in device for device in farm["devices"])
