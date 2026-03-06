"""API endpoint clients and URL builders"""
from .farms import FarmsAPI
from .users import UsersAPI
from .crops import CropsAPI
from .irrigation import IrrigationAPI

__all__ = ['FarmsAPI', 'UsersAPI', 'CropsAPI', 'IrrigationAPI']
