"""
Data generators for testing
Uses Faker to generate realistic test data
"""
from faker import Faker
from typing import Dict, Any
import random


fake = Faker()


class DataGenerator:
    """
    Generate realistic test data for API testing
    """

    @staticmethod
    def farm_name(prefix: str = "") -> str:
        """Generate realistic farm name"""
        farm_types = [
            "Valley", "Ridge", "Creek", "Hills", "Meadow",
            "Grove", "Ranch", "Estate", "Plantation", "Field"
        ]
        return f"{prefix}{fake.last_name()} {random.choice(farm_types)}"

    @staticmethod
    def farm_data(
        name_prefix: str = "",
        area_range: tuple = (50, 500),
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate complete farm data

        Args:
            name_prefix: Prefix for farm name
            area_range: Min and max area (hectares)
            **kwargs: Override specific fields
        """
        data = {
            "farmName": DataGenerator.farm_name(name_prefix),
            "area": random.randint(*area_range),
            "areaUnit": random.choice(["hectare", "acre", "dunam"]),
            "location": {
                "latitude": float(fake.latitude()),
                "longitude": float(fake.longitude()),
                "address": fake.address()
            },
            "cropType": random.choice([
                "vegetables", "fruits", "grains", "flowers",
                "citrus", "olives", "grapes", "mixed"
            ]),
            "irrigationSystem": random.choice([
                "drip", "sprinkler", "pivot", "surface", "subsurface"
            ]),
            "soilType": random.choice([
                "clay", "sandy", "loam", "silt", "peat", "chalk"
            ])
        }

        data.update(kwargs)
        return data


def generate_farm_data(name_prefix: str = "", **kwargs) -> Dict:
    """Shortcut to generate farm data"""
    return DataGenerator.farm_data(name_prefix, **kwargs)
