class IrrigationManagerEndpoints:
    @staticmethod
    def active_commands(farm_id: str) -> str:
        return f"api/v2/farms/{farm_id}/active-commands"
