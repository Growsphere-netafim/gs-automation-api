class FieldIOEndpoints:
    # Bases
    @staticmethod
    def bases() -> str:
        return "api/bases"

    @staticmethod
    def bases_address() -> str:
        return "api/bases/address"

    @staticmethod
    def base(base_id: str) -> str:
        return f"api/bases/{base_id}"

    @staticmethod
    def base_address(base_id: str) -> str:
        return f"api/bases/{base_id}/address"

    @staticmethod
    def bases_by_system_type() -> str:
        return "api/bases/system-type-id"

    # Connections
    @staticmethod
    def davis_ws_connections() -> str:
        return "api/Connections/davisWS"

    # Devices
    @staticmethod
    def devices() -> str:
        return "api/devices"

    @staticmethod
    def device(device_id: str) -> str:
        return f"api/devices/{device_id}"

    @staticmethod
    def device_address(device_id: str) -> str:
        return f"api/devices/{device_id}/address"

    # Icons
    @staticmethod
    def icons() -> str:
        return "api/Icons"

    # IO
    @staticmethod
    def io(io_id: str) -> str:
        return f"api/io/{io_id}"

    @staticmethod
    def ios() -> str:
        return "api/io"

    # IoDeviceTypes
    @staticmethod
    def io_device_types() -> str:
        return "api/IoDeviceTypes"

    @staticmethod
    def io_device_type(io_device_type_id) -> str:
        return f"api/IoDeviceTypes/{io_device_type_id}"

    # IoGroups
    @staticmethod
    def io_group(io_group_id: str) -> str:
        return f"api/IoGroups/{io_group_id}"

    @staticmethod
    def io_groups() -> str:
        return "api/IoGroups"

    # IoTypes
    @staticmethod
    def io_types() -> str:
        return "api/IoTypes"

    @staticmethod
    def io_type(io_type_id) -> str:
        return f"api/IoTypes/{io_type_id}"

    # Remotes
    @staticmethod
    def remotes() -> str:
        return "api/remotes"

    @staticmethod
    def remote(remote_id: str) -> str:
        return f"api/remotes/{remote_id}"

    # Repeaters
    @staticmethod
    def repeaters() -> str:
        return "api/repeaters"

    @staticmethod
    def repeater(repeater_id: str) -> str:
        return f"api/repeaters/{repeater_id}"

    @staticmethod
    def farm_repeaters(farm_id: str) -> str:
        return f"api/farms/{farm_id}/Repeaters"

    # SystemTypes
    @staticmethod
    def system_types() -> str:
        return "api/SystemTypes"

    @staticmethod
    def system_type(system_type_id) -> str:
        return f"api/SystemTypes/{system_type_id}"

    # Thresholds
    @staticmethod
    def thresholds() -> str:
        return "api/thresholds"

    # Trees
    @staticmethod
    def base_tree(base_id: str) -> str:
        return f"api/bases/{base_id}/tree"

    @staticmethod
    def device_tree(device_id: str) -> str:
        return f"api/devices/{device_id}/tree"

    @staticmethod
    def farm_trees() -> str:
        return "api/trees"

    @staticmethod
    def device_tree_lite(device_reference_id: str) -> str:
        return f"api/devices/{device_reference_id}/tree/lite"
