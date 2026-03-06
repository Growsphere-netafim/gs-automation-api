"""
Farms API Client
Handles all farm-related API operations
"""
from typing import List, Optional, Dict, Any
import jmespath
from requests import Response

from api.base_client import APIClient
from config.settings import get_settings


class FarmsAPI(APIClient):
    """
    API client for farm management operations
    """
    
    def __init__(self, session, user_email: str):
        super().__init__(session, user_email)
        settings = get_settings()
        self.base_url = f"{settings.base_urls['csapi_url']}/farms"
    
    def get_all_farms(self) -> Response:
        """
        Get all farms for authenticated user
        
        Returns:
            Response with list of farms
        """
        response = self.get(self.base_url)
        self.assert_status_code(
            response, 
            200, 
            f"Failed to get farms for user {self.user_email}"
        )
        return response
    
    def get_farm_by_id(self, farm_id: str) -> Response:
        """
        Get specific farm by ID
        
        Args:
            farm_id: Farm identifier
            
        Returns:
            Response with farm details
        """
        url = f"{self.base_url}/{farm_id}"
        response = self.get(url)
        self.assert_status_code(
            response,
            200,
            f"Failed to get farm {farm_id}"
        )
        return response
    
    def create_farm(self, farm_data: Dict[str, Any]) -> Response:
        """
        Create new farm
        
        Args:
            farm_data: Farm details (name, location, etc.)
            
        Returns:
            Response with created farm details
        """
        response = self.post(self.base_url, json_data=farm_data)
        self.assert_status_code(
            response,
            [200, 201],
            f"Failed to create farm"
        )
        return response
    
    def update_farm(self, farm_id: str, farm_data: Dict[str, Any]) -> Response:
        """
        Update existing farm
        
        Args:
            farm_id: Farm identifier
            farm_data: Updated farm details
            
        Returns:
            Response with updated farm
        """
        url = f"{self.base_url}/{farm_id}"
        response = self.put(url, json_data=farm_data)
        self.assert_status_code(
            response,
            [200, 204],
            f"Failed to update farm {farm_id}"
        )
        return response
    
    def delete_farm(self, farm_id: str) -> Response:
        """
        Delete farm
        
        Args:
            farm_id: Farm identifier
            
        Returns:
            Response confirming deletion
        """
        url = f"{self.base_url}/{farm_id}"
        response = self.delete(url)
        self.assert_status_code(
            response,
            [200, 204],
            f"Failed to delete farm {farm_id}"
        )
        return response
    
    def get_farm_ids_by_name_prefix(self, prefix: str) -> List[str]:
        """
        Get farm IDs that start with specific prefix
        Useful for finding test farms
        
        Args:
            prefix: Farm name prefix to search for
            
        Returns:
            List of farm IDs matching prefix
        """
        response = self.get_all_farms()
        farms_data = response.json()
        
        # Use JMESPath to filter farms by name prefix
        farm_ids = jmespath.search(
            f"farms[?starts_with(farmName, '{prefix}')].farmId",
            farms_data
        )
        
        return farm_ids if farm_ids else []
    
    def delete_farms_by_prefix(self, prefix: str) -> int:
        """
        Delete all farms matching name prefix
        Useful for test cleanup
        
        Args:
            prefix: Farm name prefix
            
        Returns:
            Number of farms deleted
        """
        farm_ids = self.get_farm_ids_by_name_prefix(prefix)
        
        deleted_count = 0
        for farm_id in farm_ids:
            try:
                self.delete_farm(farm_id)
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete farm {farm_id}: {e}")
        
        return deleted_count
    
    def get_farm_statistics(self, farm_id: str) -> Dict:
        """
        Get statistics for a farm
        
        Args:
            farm_id: Farm identifier
            
        Returns:
            Farm statistics
        """
        url = f"{self.base_url}/{farm_id}/statistics"
        response = self.get(url)
        self.assert_status_code(response, 200)
        return self.get_json(response)
    
    def search_farms(
        self,
        name: Optional[str] = None,
        location: Optional[str] = None,
        **filters
    ) -> List[Dict]:
        """
        Search farms with filters
        
        Args:
            name: Farm name (partial match)
            location: Farm location
            **filters: Additional filter parameters
            
        Returns:
            List of matching farms
        """
        params = {}
        if name:
            params['name'] = name
        if location:
            params['location'] = location
        params.update(filters)
        
        response = self.get(self.base_url, params=params)
        self.assert_status_code(response, 200)
        
        data = self.get_json(response)
        return data.get('farms', [])
    
    def get_farm_count(self) -> int:
        """
        Get total number of farms for user
        
        Returns:
            Number of farms
        """
        response = self.get_all_farms()
        data = self.get_json(response)
        return len(data.get('farms', []))
    
    def farm_exists(self, farm_id: str) -> bool:
        """
        Check if farm exists
        
        Args:
            farm_id: Farm identifier
            
        Returns:
            True if farm exists, False otherwise
        """
        try:
            response = self.get_farm_by_id(farm_id)
            return self.is_success(response)
        except Exception:
            return False
