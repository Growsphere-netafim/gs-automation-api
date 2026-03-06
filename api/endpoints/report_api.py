class ReportAPIEndpoints:
    @staticmethod
    def configuration(user_id: str) -> str:
        return f"api/Configuration/{user_id}"

    @staticmethod
    def reports_preferences(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/reportsPreferences"
