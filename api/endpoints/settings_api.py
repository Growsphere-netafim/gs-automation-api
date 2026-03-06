class SettingsAPIEndpoints:
    @staticmethod
    def alert_settings(farm_id: str, device_uuid: str) -> str:
        return f"api/v1/farms/{farm_id}/AlertSettings/{device_uuid}"
