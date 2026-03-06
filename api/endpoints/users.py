"""
Users API Client
Handles all user-related API operations
Based on your existing users.py
"""
from typing import Dict, Any, Optional
from requests import Response

from api.base_client import APIClient
from config.settings import get_settings


class UsersAPI(APIClient):
    """
    API client for user management operations
    """
    
    def __init__(self, session, user_email: str):
        super().__init__(session, user_email)
        settings = get_settings()
        self.base_url = f"{settings.base_urls['csapi_url']}/users"
    
    def get_user(self, user_id: str) -> Response:
        """
        Get user information by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            Response with user details
        """
        url = f"{self.base_url}/{user_id}"
        response = self.get(url)
        self.assert_status_code(response, 200, f"Failed to get user {user_id}")
        return response
    
    def get_user_details_for_enterprise(self, enterprise_id: str) -> Response:
        """
        Get user details for specific enterprise
        
        Args:
            enterprise_id: Enterprise identifier
            
        Returns:
            Response with users list
        """
        settings = get_settings()
        url = f"{settings.base_urls['csapi_url']}/enterprises/{enterprise_id}/users/details"
        response = self.get(url)
        return response
    
    def update_user(
        self,
        user_id: str,
        user_data: Dict[str, Any]
    ) -> Response:
        """
        Update user information
        
        Args:
            user_id: User identifier
            user_data: Updated user details
            
        Returns:
            Response with updated user
        """
        url = f"{self.base_url}/{user_id}"
        response = self.put(url, json_data=user_data)
        self.assert_status_code(
            response,
            [200, 204],
            f"Failed to update user {user_id}"
        )
        return response
    
    def update_user_culture(self, user_id: str, language: str) -> Response:
        """
        Update user's language/culture setting
        
        Args:
            user_id: User identifier
            language: Language code (e.g., 'en-US', 'he-IL')
            
        Returns:
            Response confirming update
        """
        # Map language names to culture codes if needed
        language_map = {
            "english": "en-US",
            "hebrew": "he-IL",
            "spanish": "es-ES",
            "french": "fr-FR"
        }
        
        culture = language_map.get(language.lower(), language)
        payload = {"culture": culture}
        
        return self.update_user(user_id, payload)
    
    def update_user_unit_system(
        self,
        user_id: str,
        unit_system: str = "metric"
    ) -> Response:
        """
        Update user's unit system (metric/imperial)
        
        Args:
            user_id: User identifier
            unit_system: 'metric' or 'imperial'
            
        Returns:
            Response confirming update
        """
        if unit_system not in ["metric", "imperial"]:
            raise ValueError("unit_system must be 'metric' or 'imperial'")
        
        payload = {"unitSystem": unit_system}
        return self.update_user(user_id, payload)
    
    def update_initial_params(
        self,
        user_id: str,
        params: Dict[str, Any]
    ) -> Response:
        """
        Update user's initial parameters
        
        Args:
            user_id: User identifier
            params: Initial parameters to set
            
        Returns:
            Response confirming update
        """
        return self.update_user(user_id, params)
    
    def get_my_profile(self) -> Response:
        """
        Get current authenticated user's profile
        
        Returns:
            Response with user profile
        """
        # Assuming there's a /me or /my-account endpoint
        settings = get_settings()
        url = f"{settings.base_urls['csapi_url']}/users/my-account"
        response = self.get(url)
        return response
    
    def update_my_profile(self, profile_data: Dict[str, Any]) -> Response:
        """
        Update current user's profile
        
        Args:
            profile_data: Profile data to update
            
        Returns:
            Response with updated profile
        """
        settings = get_settings()
        url = f"{settings.base_urls['csapi_url']}/users/my-account"
        response = self.put(url, json_data=profile_data)
        return response
    
    def create_user(self, user_data: Dict[str, Any]) -> Response:
        """
        Create new user (admin operation)
        
        Args:
            user_data: User details
            
        Returns:
            Response with created user
        """
        response = self.post(self.base_url, json_data=user_data)
        self.assert_status_code(
            response,
            [200, 201],
            "Failed to create user"
        )
        return response
    
    def delete_user(self, user_id: str) -> Response:
        """
        Delete user (admin operation)
        
        Args:
            user_id: User identifier
            
        Returns:
            Response confirming deletion
        """
        url = f"{self.base_url}/{user_id}"
        response = self.delete(url)
        self.assert_status_code(
            response,
            [200, 204],
            f"Failed to delete user {user_id}"
        )
        return response
    
    def search_users(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: Optional[str] = None,
        **filters
    ) -> Response:
        """
        Search users with filters
        
        Args:
            email: Filter by email
            name: Filter by name
            role: Filter by role
            **filters: Additional filters
            
        Returns:
            Response with matching users
        """
        params = {}
        if email:
            params['email'] = email
        if name:
            params['name'] = name
        if role:
            params['role'] = role
        params.update(filters)
        
        response = self.get(self.base_url, params=params)
        return response
    
    def user_exists(self, user_id: str) -> bool:
        """
        Check if user exists
        
        Args:
            user_id: User identifier
            
        Returns:
            True if user exists, False otherwise
        """
        try:
            response = self.get_user(user_id)
            return self.is_success(response)
        except Exception:
            return False
    
    def get_user_permissions(self, user_id: str) -> Dict:
        """
        Get user's permissions
        
        Args:
            user_id: User identifier
            
        Returns:
            User permissions
        """
        url = f"{self.base_url}/{user_id}/permissions"
        response = self.get(url)
        self.assert_status_code(response, 200)
        return self.get_json(response)
    
    def update_user_permissions(
        self,
        user_id: str,
        permissions: Dict[str, Any]
    ) -> Response:
        """
        Update user's permissions (admin operation)
        
        Args:
            user_id: User identifier
            permissions: New permissions
            
        Returns:
            Response confirming update
        """
        url = f"{self.base_url}/{user_id}/permissions"
        response = self.put(url, json_data=permissions)
        self.assert_status_code(response, [200, 204])
        return response


# Helper function to get user ID from email
def get_user_id_by_email(users_api: UsersAPI, email: str) -> Optional[str]:
    """
    Get user ID by email address
    
    Args:
        users_api: UsersAPI instance
        email: User email
        
    Returns:
        User ID if found, None otherwise
    """
    try:
        response = users_api.search_users(email=email)
        if users_api.is_success(response):
            users = users_api.get_json(response)
            if users and len(users) > 0:
                return users[0].get('userId')
    except Exception:
        pass
    return None
