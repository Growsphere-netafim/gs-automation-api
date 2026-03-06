class DeviceStateManagerEndpoints:
    @staticmethod
    def device_state_by_id(device_id: str) -> str:
        return f"api/DeviceStates/ById/{device_id}"

    @staticmethod
    def device_state_by_uuid(device_uuid: str) -> str:
        return f"api/DeviceStates/ByUUId/{device_uuid}"

    @staticmethod
    def device_states_by_farm(farm_id: str) -> str:
        return f"api/DeviceStates/ByFarmId/{farm_id}"

    @staticmethod
    def heartbeats() -> str:
        return "api/Heartbeats"

    @staticmethod
    def query_heartbeats() -> str:
        return "api/QueryHeartbeats"
