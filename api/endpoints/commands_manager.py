class CommandsManagerEndpoints:
    @staticmethod
    def command_status(reference_id: str) -> str:
        return f"api/Commands/{reference_id}"

    @staticmethod
    def latest_statuses_farm(farm_id: str) -> str:
        return f"api/farms/{farm_id}/Commands/Statuses/Latest"

    @staticmethod
    def latest_statuses_global() -> str:
        return "api/Commands/Statuses/Latest"

    @staticmethod
    def device_request_latest(device_id: str, request_id: str) -> str:
        return f"api/Devices/{device_id}/Requests/{request_id}/Latest"

    @staticmethod
    def odata_commands_global() -> str:
        return "api/ODataCommands"

    @staticmethod
    def odata_commands_farm(farm_id: str) -> str:
        return f"api/farms/{farm_id}/ODataCommands"
