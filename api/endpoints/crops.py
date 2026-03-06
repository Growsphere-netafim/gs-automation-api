"""
Crops API Client
Handles all crop-related API operations
Automatically generated from Swagger: cropservice-qa1
"""
from typing import List, Optional, Dict, Any
from requests import Response

from api.base_client import APIClient
from config.settings import get_settings


class CropsAPI(APIClient):
    """
    API client for Crop Families and Crops management
    """
    
    def __init__(self, session, user_email: str):
        super().__init__(session, user_email)
        settings = get_settings()
        # Note: base_url is set to the Crops Service URL
        # We'll need to add this to settings if it's not there
        self.base_url = f"{settings.base_urls.get('cropservice_url', 'https://cropservice-qa1.k8s.growsphere.netafim.com')}/api"

    # ==================== Crop Families ====================

    def get_crop_families(
        self, 
        name: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 25, 
        include_inactive: bool = False
    ) -> Response:
        """
        Queries the crop families list
        """
        params = {
            "name": name,
            "page": page,
            "pageSize": page_size,
            "includeInactive": include_inactive
        }
        return self.get("/CropFamilies", params=params)

    def create_crop_family(self, crop_family_data: Dict[str, Any]) -> Response:
        """
        Creates a new crop family
        """
        return self.post("/CropFamilies", json_data=crop_family_data)

    def get_crop_family_by_id(self, crop_family_id: int) -> Response:
        """
        Gets a specific crop family by ID
        """
        return self.get(f"/CropFamilies/{crop_family_id}")

    def update_crop_family(self, crop_family_id: int, crop_family_data: Dict[str, Any]) -> Response:
        """
        Updates a crop family by ID
        """
        return self.put(f"/CropFamilies/{crop_family_id}", json_data=crop_family_data)

    # ==================== Crops ====================

    def get_crops(
        self, 
        name: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 25, 
        include_inactive: bool = False
    ) -> Response:
        """
        Queries the crops list
        """
        params = {
            "name": name,
            "page": page,
            "pageSize": page_size,
            "includeInactive": include_inactive
        }
        return self.get("/Crops", params=params)

    def create_crop(self, crop_data: Dict[str, Any]) -> Response:
        """
        Creates a new crop
        """
        return self.post("/Crops", json_data=crop_data)

    def get_crop_by_id(self, crop_id: int) -> Response:
        """
        Gets a specific crop by ID
        """
        return self.get(f"/Crops/{crop_id}")

    def update_crop(self, crop_id: int, crop_data: Dict[str, Any]) -> Response:
        """
        Updates a crop by ID
        """
        return self.put(f"/Crops/{crop_id}", json_data=crop_data)
