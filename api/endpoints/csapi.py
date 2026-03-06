class CSAPIEndpoints:
    # General
    @staticmethod
    def root() -> str:
        return "/"

    @staticmethod
    def devices_odata() -> str:
        return "api/v1/devices"

    @staticmethod
    def device_events() -> str:
        return "api/v1/deviceEvents"

    @staticmethod
    def support_ticket(ticket_id: str) -> str:
        return f"api/v1/support-tickets/{ticket_id}"

    @staticmethod
    def metadata() -> str:
        return "api/v1/$metadata"

    @staticmethod
    def service_document() -> str:
        return "api/v1"

    # Cultures
    @staticmethod
    def culture_app_ids() -> str:
        return "api/v1/cultures/collection/AppIds"

    @staticmethod
    def cultures(app_id: str) -> str:
        return f"api/v1/cultures/{app_id}"

    @staticmethod
    def culture(app_id: str, culture: str) -> str:
        return f"api/v1/cultures/{app_id}/{culture}"

    # Dealers
    @staticmethod
    def dealers_by_distributor(distributor_id: str) -> str:
        return f"api/v1/distributors/{distributor_id}/dealers"

    @staticmethod
    def dealers() -> str:
        return "api/v1/dealers"

    @staticmethod
    def country_names() -> str:
        return "api/v1/country-names"

    @staticmethod
    def dealer(dealer_id: str) -> str:
        return f"api/v1/dealers/{dealer_id}"

    # Devices
    @staticmethod
    def device(device_reference_id: str) -> str:
        return f"api/v1/devices/{device_reference_id}"

    @staticmethod
    def devices_by_enterprise(enterprise_id) -> str:
        return f"api/v1/devices/enterprise/{enterprise_id}"

    @staticmethod
    def device_by_serial(device_serial_id: str) -> str:
        return f"api/v1/devices/serial/{device_serial_id}"

    @staticmethod
    def device_cert(device_reference_id: str) -> str:
        return f"api/v1/devices/{device_reference_id}/cert"

    @staticmethod
    def device_prkey(device_reference_id: str) -> str:
        return f"api/v1/devices/{device_reference_id}/prkey"

    @staticmethod
    def device_assignable(device_reference_id: str) -> str:
        return f"api/v1/devices/{device_reference_id}/assignable"

    @staticmethod
    def device_hex_support(device_reference_id: str) -> str:
        return f"api/v1/devices/{device_reference_id}/hex-support"

    # Distributors
    @staticmethod
    def distributors() -> str:
        return "api/v1/distributors"

    @staticmethod
    def distributor_names() -> str:
        return "api/v1/distributors/names"

    @staticmethod
    def distributor(distributor_id: str) -> str:
        return f"api/v1/distributors/{distributor_id}"

    @staticmethod
    def search_distributors() -> str:
        return "api/v1/distributors/search/distributors/search"

    @staticmethod
    def search_dealers_in_distributor(distributor_id: str) -> str:
        return f"api/v1/distributors/{distributor_id}/search/dealers/search"

    @staticmethod
    def search_all_dealers() -> str:
        return "api/v1/distributors/search/dealers/search"

    # Enterprises
    @staticmethod
    def enterprises() -> str:
        return "api/v1/enterprises"

    @staticmethod
    def enterprise(enterprise_id) -> str:
        return f"api/v1/enterprises/{enterprise_id}"

    @staticmethod
    def enterprise_ids(enterprise_id) -> str:
        return f"api/v1/enterprises/{enterprise_id}/ids"

    @staticmethod
    def enterprise_name_availability() -> str:
        return "api/v1/enterprises/name-availability"

    @staticmethod
    def enterprise_farms(enterprise_id) -> str:
        return f"api/v1/enterprises/{enterprise_id}/farms"

    @staticmethod
    def enterprise_users_details(enterprise_id) -> str:
        return f"api/v1/enterprises/{enterprise_id}/users/details"

    @staticmethod
    def enterprise_hierarchy(enterprise_id) -> str:
        return f"api/v1/enterprises/hierarchy/company/{enterprise_id}"

    @staticmethod
    def dealer_hierarchy(dealer_id: str) -> str:
        return f"api/v1/enterprises/hierarchy/dealer/{dealer_id}"

    @staticmethod
    def distributor_hierarchy(distributor_id: str) -> str:
        return f"api/v1/enterprises/hierarchy/distributor/{distributor_id}"

    # Farms
    @staticmethod
    def farms() -> str:
        return "api/v1/farms"

    @staticmethod
    def farms_by_enterprise(enterprise_id) -> str:
        return f"api/v1/farms/enterprise/{enterprise_id}"

    @staticmethod
    def farm(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}"

    @staticmethod
    def farm_users_details(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/users/details"

    @staticmethod
    def farm_roles() -> str:
        return "api/v1/farms/roles"

    @staticmethod
    def farm_enterprise_category(farm_id: str) -> str:
        return f"api/v1/farms/{farm_id}/enterprise/category"

    # Provisioning
    @staticmethod
    def provisioning_device(device_id: str) -> str:
        return f"api/v1/Provisioning/devices/{device_id}"

    @staticmethod
    def provisioning_steps() -> str:
        return "api/v1/Provisioning/steps"

    @staticmethod
    def provisioning_farm(farm_id: str) -> str:
        return f"api/v1/Provisioning/farms/{farm_id}"

    @staticmethod
    def provisioning_flow(flow_uuid: str) -> str:
        return f"api/v1/Provisioning/{flow_uuid}"

    @staticmethod
    def provisioning_topology(flow_uuid: str) -> str:
        return f"api/v1/Provisioning/{flow_uuid}/topology"

    @staticmethod
    def provisioning_error_codes() -> str:
        return "api/v1/Provisioning/error-codes"

    # TechToolbox
    @staticmethod
    def techtoolbox_dashboard_filters() -> str:
        return "api/v1/techtoolbox/Filters/Dashboard"

    @staticmethod
    def techtoolbox_stats_alert_type() -> str:
        return "api/v1/techtoolbox/statistics/AlertType"

    @staticmethod
    def techtoolbox_stats_alert_device_type() -> str:
        return "api/v1/techtoolbox/statistics/AlertDeviceType"

    @staticmethod
    def techtoolbox_stats_total_alert_type() -> str:
        return "api/v1/techtoolbox/statistics/TotalAlertType"

    @staticmethod
    def techtoolbox_stats_total_overall() -> str:
        return "api/v1/techtoolbox/statistics/TotalOverall"

    @staticmethod
    def techtoolbox_stats_alerts_by_distributors() -> str:
        return "api/v1/techtoolbox/statistics/AlertsByDistributors"

    @staticmethod
    def techtoolbox_stats_alerts_by_dealers() -> str:
        return "api/v1/techtoolbox/statistics/AlertsByDealers"

    @staticmethod
    def techtoolbox_stats_alerts_by_companies() -> str:
        return "api/v1/techtoolbox/statistics/AlertsByCompanies"

    @staticmethod
    def techtoolbox_stats_alerts_by_farms() -> str:
        return "api/v1/techtoolbox/statistics/AlertsByFarms"

    @staticmethod
    def techtoolbox_alerted_devices() -> str:
        return "api/v1/techtoolbox/alerted-devices"

    # Text Resources
    @staticmethod
    def text_resource_app_ids() -> str:
        return "api/v1/textresources/collection/AppIds"

    @staticmethod
    def text_resources(app_id: str) -> str:
        return f"api/v1/textresources/{app_id}"

    @staticmethod
    def text_resources_by_category(app_id: str, category: str) -> str:
        return f"api/v1/textresources/{app_id}/category/{category}"

    @staticmethod
    def text_resources_by_key(app_id: str) -> str:
        return f"api/v1/textresources/{app_id}/bykey"

    @staticmethod
    def text_resources_by_key_and_category(app_id: str, category: str) -> str:
        return f"api/v1/textresources/{app_id}/category/{category}/bykey"

    @staticmethod
    def text_resources_grouped(app_id: str) -> str:
        return f"api/v1/textresources/{app_id}/grouped"

    @staticmethod
    def text_resources_grouped_by_category(app_id: str, category: str) -> str:
        return f"api/v1/textresources/{app_id}/category/{category}/grouped"

    # SignUp / Invitations
    @staticmethod
    def signup_invitation(invitation_id: str) -> str:
        return f"api/v1/invitations/signup/{invitation_id}"

    @staticmethod
    def signup_token(token: str) -> str:
        return f"api/v1/invitations/signup/token/{token}"

    # Users
    @staticmethod
    def users() -> str:
        return "api/v1/users"

    @staticmethod
    def user(user_id: str) -> str:
        return f"api/v1/users/{user_id}"

    @staticmethod
    def user_roles() -> str:
        return "api/v1/users/roles"

    @staticmethod
    def user_farms(user_id: str) -> str:
        return f"api/v1/users/{user_id}/farms"

    @staticmethod
    def impersonation_token(token: str) -> str:
        return f"api/v1/users/impersonation/token/{token}"

    # Versions
    @staticmethod
    def versions() -> str:
        return "api/v1/Versions"

    @staticmethod
    def version(version: str) -> str:
        return f"api/v1/Versions/{version}"

    @staticmethod
    def version_details(system_type, version: str) -> str:
        return f"api/v1/systemtypes/{system_type}/VersionDetails/{version}"

    @staticmethod
    def version_file(system_type, version: str) -> str:
        return f"api/v1/systemtypes/{system_type}/versions/{version}"
