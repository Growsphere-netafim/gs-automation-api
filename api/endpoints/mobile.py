class MobileEndpoints:
    # Bases
    @staticmethod
    def base_topology() -> str:
        return "api/Mobile/base-topology"

    @staticmethod
    def base_tree(base_uuid: str) -> str:
        return f"api/Mobile/bases/{base_uuid}/tree"

    # Commands
    @staticmethod
    def command(reference_id: str) -> str:
        return f"api/Mobile/Commands/{reference_id}"

    @staticmethod
    def commands_by_farm_device(farm_id: str, device_id: str) -> str:
        return f"api/Commands/{farm_id}/{device_id}"

    @staticmethod
    def commands_list_for_device(device_id: str) -> str:
        return f"api/Commands/list/{device_id}"

    @staticmethod
    def request_command(command_type, system_type, device_id: str) -> str:
        return f"api/Mobile/request/{command_type}/systemType/{system_type}/device/{device_id}"

    # Devices
    @staticmethod
    def device_state(farm_id: str, device_id: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Devices/{device_id}/device-state"

    @staticmethod
    def device_assignable(device_reference_id: str) -> str:
        return f"api/Mobile/Devices/{device_reference_id}/assignable"

    @staticmethod
    def general_settings(device_uuid: str) -> str:
        return f"api/Mobile/{device_uuid}/general-settings"

    @staticmethod
    def alert_settings(device_id: str) -> str:
        return f"api/Mobile/{device_id}/alert-settings"

    @staticmethod
    def delay_settings(device_uuid: str) -> str:
        return f"api/Mobile/{device_uuid}/delay-settings"

    @staticmethod
    def device_states_by_farm(farm_id: str) -> str:
        return f"api/Mobile/DeviceStates/ByFarmId/{farm_id}"

    @staticmethod
    def device_connection_status(farm_id: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Devices/connection-status"

    @staticmethod
    def device_tree(device_id: str) -> str:
        return f"api/Mobile/devices/{device_id}/tree"

    @staticmethod
    def device_details() -> str:
        return "api/Mobile/deviceDetails"

    @staticmethod
    def device_recipes(farm_id: str, device_uuid: str) -> str:
        return f"api/Mobile/farms/{farm_id}/devices/{device_uuid}/recipes"

    @staticmethod
    def device_recipes_with_usage(farm_id: str, device_uuid: str) -> str:
        return f"api/Mobile/farms/{farm_id}/devices/{device_uuid}/recipes/with-usage"

    @staticmethod
    def user_device_graphs(farm_id: str, device_id: str) -> str:
        return f"api/Mobile/farms/{farm_id}/devices/{device_id}/user-device-graphs"

    @staticmethod
    def user_device_graph(farm_id: str, device_id: str, graph_id: str) -> str:
        return f"api/Mobile/farms/{farm_id}/devices/{device_id}/user-device-graphs/{graph_id}"

    # Farms
    @staticmethod
    def io_list(farm_id: str) -> str:
        return f"api/Mobile/farms/{farm_id}/io-list"

    @staticmethod
    def trees() -> str:
        return "api/Mobile/trees"

    @staticmethod
    def dashboard_data(farm_id: str) -> str:
        return f"api/Mobile/Dashboard/data/farm/{farm_id}"

    @staticmethod
    def homepage_devices(farm_id: str) -> str:
        return f"api/Mobile/HomePage/Farms/{farm_id}/Devices"

    # General
    @staticmethod
    def notes() -> str:
        return "api/Notes"

    @staticmethod
    def system_types() -> str:
        return "api/fieldio/system-types"

    # Irrigation
    @staticmethod
    def farm_program_schemes(farm_id: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Irrigation/program-schemes"

    @staticmethod
    def device_program_schemes(farm_id: str, device_uuid: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Devices/{device_uuid}/program-schemes"

    @staticmethod
    def program_scheme(farm_id: str, program_uuid: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/program-schemes/{program_uuid}"

    @staticmethod
    def program_scheme_status(farm_id: str, program_uuid: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Program-Schemes/{program_uuid}/Status"

    @staticmethod
    def device_program_schemes_statuses(farm_id: str, device_uuid: str) -> str:
        return f"api/Mobile/Farms/{farm_id}/Devices/{device_uuid}/program-schemes/statuses"

    @staticmethod
    def irrigation_programs(device_id: str) -> str:
        return f"api/Mobile/{device_id}/irrigationPrograms"

    @staticmethod
    def irrigation_programs_daily(device_id: str) -> str:
        return f"api/Mobile/{device_id}/irrigationPrograms/daily"

    @staticmethod
    def last_irrigation(program_uuid: str) -> str:
        return f"api/Mobile/program/{program_uuid}/lastIrrigation"

    @staticmethod
    def device_irrigation_blocks(device_id: str) -> str:
        return f"api/Mobile/devices/{device_id}/irrigationBlocks"

    @staticmethod
    def irrigation_blocks() -> str:
        return "api/Mobile/irrigationBlocks"

    @staticmethod
    def max_program_overview(program_uuid: str) -> str:
        return f"api/Mobile/maxProgramOverview/{program_uuid}"

    @staticmethod
    def program_progress(program_uuid: str) -> str:
        return f"api/Mobile/programProgress/{program_uuid}"

    # Provisioning
    @staticmethod
    def provisioning_farm(farm_id: str) -> str:
        return f"api/Mobile/Provisioning/Farms/{farm_id}"

    @staticmethod
    def provisioning_status(flow_uuid: str) -> str:
        return f"api/Mobile/Provisioning/{flow_uuid}"

    # Reports
    @staticmethod
    def last_eco_daily_program_report(farm_id: str) -> str:
        return f"api/Mobile/farms/{farm_id}/LastEcoDailyProgramReport"

    @staticmethod
    def daily_report(device_id: str, date: str) -> str:
        return f"api/Reports/dailyReport/{device_id}/{date}"

    @staticmethod
    def irrigation_logs(farm_id: str, device_id: str, date: str) -> str:
        return f"api/Reports/irrigationLogs/{farm_id}/{device_id}/{date}"

    # Users
    @staticmethod
    def user_details() -> str:
        return "api/Mobile/userDetails"

    @staticmethod
    def user_graphs() -> str:
        return "api/Mobile/user-graphs"
