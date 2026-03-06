"""
Mock responses for API testing
Use these to test without hitting real API
"""
from typing import Dict, List, Any
from datetime import datetime


class MockResponses:
    """
    Collection of mock API responses
    Matches the structure of real API responses
    """

    @staticmethod
    def farm_list(count: int = 3) -> Dict[str, Any]:
        """Mock response for GET /farms"""
        farms = []
        for i in range(count):
            farms.append({
                "farmId": f"farm-{i+1:03d}",
                "farmName": f"Test Farm {i+1}",
                "location": {
                    "latitude": 32.0 + i * 0.1,
                    "longitude": 35.0 + i * 0.1,
                    "address": f"Test Address {i+1}"
                },
                "area": 100 + i * 10,
                "areaUnit": "hectare",
                "createdAt": "2024-01-15T10:00:00Z",
                "updatedAt": "2024-01-20T15:30:00Z",
                "status": "active"
            })

        return {
            "farms": farms,
            "total": count
        }

    @staticmethod
    def single_farm(farm_id: str = "farm-001") -> Dict[str, Any]:
        """Mock response for GET /farms/{farmId}"""
        return {
            "farmId": farm_id,
            "farmName": "Test Farm",
            "location": {
                "latitude": 32.0853,
                "longitude": 34.7818,
                "address": "Test Farm Location"
            },
            "area": 150,
            "areaUnit": "hectare",
            "cropType": "vegetables",
            "irrigationSystem": "drip",
            "devices": [
                {
                    "deviceId": "device-001",
                    "deviceType": "sensor",
                    "status": "online"
                }
            ],
            "createdAt": "2024-01-15T10:00:00Z",
            "updatedAt": "2024-01-20T15:30:00Z",
            "status": "active"
        }

    @staticmethod
    def created_farm(farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock response for POST /farms"""
        farm_id = f"farm-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "farmId": farm_id,
            "farmName": farm_data.get("farmName", "New Farm"),
            "location": farm_data.get("location", {}),
            "area": farm_data.get("area", 100),
            "areaUnit": farm_data.get("areaUnit", "hectare"),
            "createdAt": datetime.now().isoformat() + "Z",
            "status": "active",
            "message": "Farm created successfully"
        }

    @staticmethod
    def deleted_farm() -> Dict[str, Any]:
        """Mock response for DELETE /farms/{farmId}"""
        return {
            "success": True,
            "message": "Farm deleted successfully"
        }

    @staticmethod
    def error_response(
        status_code: int,
        message: str,
        error_code: str = "ERROR"
    ) -> Dict[str, Any]:
        """Generic error response"""
        return {
            "error": {
                "code": error_code,
                "message": message,
                "statusCode": status_code,
                "timestamp": datetime.now().isoformat() + "Z"
            }
        }

    @staticmethod
    def validation_error(field: str, message: str) -> Dict[str, Any]:
        """Validation error response"""
        return {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": [
                    {
                        "field": field,
                        "message": message
                    }
                ]
            }
        }


class MockFactory:
    """
    Factory for creating customized mock responses
    """

    @staticmethod
    def create_farms(count: int, name_prefix: str = "Farm") -> List[Dict]:
        """Create multiple mock farms"""
        farms = []
        for i in range(count):
            farms.append({
                "farmId": f"farm-{i+1:03d}",
                "farmName": f"{name_prefix} {i+1}",
                "area": 100 + i * 10,
                "status": "active"
            })
        return farms

    @staticmethod
    def create_farm_with_devices(farm_id: str, device_count: int = 3) -> Dict:
        """Create a mock farm with embedded devices"""
        devices = []
        for i in range(device_count):
            devices.append({
                "deviceId": f"device-{farm_id}-{i+1:03d}",
                "deviceName": f"Device {i+1}",
                "deviceType": "sensor",
                "status": "online"
            })
        return {
            "farmId": farm_id,
            "farmName": f"Farm {farm_id}",
            "area": 100,
            "status": "active",
            "devices": devices,
        }
