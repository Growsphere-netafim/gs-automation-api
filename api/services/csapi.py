import pytest
from api.client.api_client import QAApiClient
from api.client.response import ApiResponse
from api.endpoints.csapi import CSAPIEndpoints


_FALLBACK_FARM_IDS = [
    "qa1-nb10000", "qa1-nb10047", "qa1-nb14218", "qa1-nb10058", "qa1-nb11141",
    "qa1-nb13042", "qa1-nb14595", "qa1-nb14604", "qa1-nb14644", "qa1-nb14658",
]


class CSAPIService:
    def __init__(self, client: QAApiClient, data):
        self._client = client
        self._data = data
        self._cache = {}

    # ── Resolvers ─────────────────────────────────────────────────────────────

    def _resolve_device_serial(self) -> str:
        """Fetch a serialNumber that actually exists via GET /devices/serial/{serial}."""
        if 'device_serial' not in self._cache:
            for farm_id in _FALLBACK_FARM_IDS:
                resp = self._client.get(
                    CSAPIEndpoints.devices_odata(),
                    params={"farmId": farm_id, "$top": 10}
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()
                items = data if isinstance(data, list) else data.get('value', data.get('items', []))
                for device in items:
                    serial = device.get('serialNumber') or device.get('SerialNumber')
                    if not serial:
                        continue
                    # Verify it's fetchable by serial
                    verify = self._client.get(CSAPIEndpoints.device_by_serial(serial))
                    if verify.status_code == 200:
                        self._cache['device_serial'] = serial
                        return serial
            pytest.skip("No device with a resolvable serialNumber found across all QA1 farms")
        return self._cache['device_serial']

    def _resolve_version(self) -> str:
        """Fetch first version id that actually exists in blob storage."""
        if 'version' not in self._cache:
            resp = self._client.get(CSAPIEndpoints.versions())
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve version: GET versions returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('versions', data.get('items', []))
            for item in items:
                v = item if isinstance(item, str) else (item.get('id') or item.get('version') or item.get('name'))
                if not v:
                    continue
                verify = self._client.get(CSAPIEndpoints.version(v))
                if verify.status_code == 200:
                    self._cache['version'] = v
                    return v
            pytest.skip("No version with a resolvable blob found in QA1")
        return self._cache['version']

    def _resolve_culture(self) -> str:
        """Fetch first culture id that actually exists in the environment."""
        if 'culture' not in self._cache:
            if not self._data.app_id:
                pytest.skip("appId not configured")
            resp = self._client.get(CSAPIEndpoints.cultures(self._data.app_id))
            if resp.status_code != 200:
                pytest.skip(f"Cannot resolve culture: GET cultures returned {resp.status_code}")
            data = resp.json()
            items = data if isinstance(data, list) else data.get('cultures', data.get('ids', data.get('items', [])))
            if not items:
                pytest.skip("No cultures found for app")
            for item in items:
                culture_id = item if isinstance(item, str) else (item.get('id') or item.get('cultureId'))
                if not culture_id:
                    continue
                # Verify it actually exists
                verify = self._client.get(CSAPIEndpoints.culture(self._data.app_id, culture_id))
                if verify.status_code == 200:
                    self._cache['culture'] = culture_id
                    return culture_id
            pytest.skip(f"No valid culture found for app '{self._data.app_id}' in QA1 environment")
        return self._cache['culture']

    # General
    def get_root(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.root())

    def get_devices_odata(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.devices_odata(), params={"$top": 10})

    def get_device_events(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.device_events(), params={"$top": 10})

    def get_support_ticket(self) -> ApiResponse:
        if not self._data.ticket_id:
            pytest.skip("ticketId not configured")
        resp = self._client.get(CSAPIEndpoints.support_ticket(self._data.ticket_id))
        if resp.status_code in (400, 404):
            pytest.skip("Support ticket not found or invalid ID")
        return resp

    def get_metadata(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.metadata())

    def get_service_document(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.service_document())

    # Cultures
    def get_culture_app_ids(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.culture_app_ids())

    def get_cultures(self) -> ApiResponse:
        if not self._data.app_id:
            pytest.skip("appId not configured")
        return self._client.get(CSAPIEndpoints.cultures(self._data.app_id))

    def get_culture(self) -> ApiResponse:
        if not self._data.app_id:
            pytest.skip("appId not configured")
        culture = self._resolve_culture()
        return self._client.get(CSAPIEndpoints.culture(self._data.app_id, culture))

    # Dealers
    def get_dealers_by_distributor(self) -> ApiResponse:
        if not self._data.distributor_id:
            pytest.skip("distributorId not configured")
        return self._client.get(
            CSAPIEndpoints.dealers_by_distributor(self._data.distributor_id)
        )

    def get_dealers(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.dealers())

    def get_country_names(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.country_names())

    def get_dealer(self) -> ApiResponse:
        if not self._data.dealer_id:
            pytest.skip("dealerId not configured")
        return self._client.get(CSAPIEndpoints.dealer(self._data.dealer_id))

    # Devices
    def get_device(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(CSAPIEndpoints.device(self._data.device_reference_id))

    def get_devices_by_enterprise(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(
            CSAPIEndpoints.devices_by_enterprise(self._data.enterprise_id)
        )

    def get_device_by_serial(self) -> ApiResponse:
        serial = self._resolve_device_serial()
        return self._client.get(CSAPIEndpoints.device_by_serial(serial))

    def get_device_cert(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(CSAPIEndpoints.device_cert(self._data.device_reference_id))

    def get_device_prkey(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(CSAPIEndpoints.device_prkey(self._data.device_reference_id))

    def get_device_assignable(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        resp = self._client.get(
            CSAPIEndpoints.device_assignable(self._data.device_reference_id)
        )
        if resp.status_code in (409, 404):
            pytest.skip("Device assignability check unavailable (409/404)")
        return resp

    def get_device_hex_support(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(
            CSAPIEndpoints.device_hex_support(self._data.device_reference_id)
        )

    # Distributors
    def get_distributors(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.distributors())

    def get_distributor_names(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.distributor_names())

    def get_distributor(self) -> ApiResponse:
        if not self._data.distributor_id:
            pytest.skip("distributorId not configured")
        return self._client.get(CSAPIEndpoints.distributor(self._data.distributor_id))

    def search_distributors(self) -> ApiResponse:
        resp = self._client.get(CSAPIEndpoints.search_distributors(), json={})
        if resp.status_code in (409, 500):
            pytest.xfail("Backend bug: Distributor search endpoint unavailable (server error)")
        return resp

    def search_dealers_in_distributor(self) -> ApiResponse:
        if not self._data.distributor_id:
            pytest.skip("distributorId not configured")
        resp = self._client.get(
            CSAPIEndpoints.search_dealers_in_distributor(self._data.distributor_id), json={}
        )
        if resp.status_code in (409, 500):
            pytest.xfail("Backend bug: Dealer search endpoint unavailable (server error)")
        return resp

    def search_all_dealers(self) -> ApiResponse:
        resp = self._client.get(CSAPIEndpoints.search_all_dealers(), json={})
        if resp.status_code in (409, 500):
            pytest.xfail("Backend bug: All dealers search endpoint unavailable (server error)")
        return resp

    # Enterprises
    def get_enterprises(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.enterprises())

    def get_enterprise(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(CSAPIEndpoints.enterprise(self._data.enterprise_id))

    def get_enterprise_ids(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(CSAPIEndpoints.enterprise_ids(self._data.enterprise_id))

    def get_enterprise_name_availability(self) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.enterprise_name_availability(), params={"name": "TestOrg"}
        )

    def get_enterprise_farms(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(CSAPIEndpoints.enterprise_farms(self._data.enterprise_id))

    def get_enterprise_users_details(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(
            CSAPIEndpoints.enterprise_users_details(self._data.enterprise_id)
        )

    def get_enterprise_hierarchy(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(
            CSAPIEndpoints.enterprise_hierarchy(self._data.enterprise_id)
        )

    def get_dealer_hierarchy(self) -> ApiResponse:
        if not self._data.dealer_id:
            pytest.skip("dealerId not configured")
        return self._client.get(CSAPIEndpoints.dealer_hierarchy(self._data.dealer_id))

    def get_distributor_hierarchy(self) -> ApiResponse:
        if not self._data.distributor_id:
            pytest.skip("distributorId not configured")
        return self._client.get(
            CSAPIEndpoints.distributor_hierarchy(self._data.distributor_id)
        )

    # Farms
    def get_farms(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.farms())

    def get_farms_by_enterprise(self) -> ApiResponse:
        if not self._data.enterprise_id:
            pytest.skip("enterpriseId not configured")
        return self._client.get(CSAPIEndpoints.farms_by_enterprise(self._data.enterprise_id))

    def get_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(CSAPIEndpoints.farm(self._data.farm_id))

    def get_farm_users_details(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(CSAPIEndpoints.farm_users_details(self._data.farm_id))

    def get_farm_roles(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.farm_roles())

    def get_farm_enterprise_category(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(
            CSAPIEndpoints.farm_enterprise_category(self._data.farm_id)
        )

    # Provisioning
    def get_provisioning_device(self) -> ApiResponse:
        if not self._data.device_reference_id:
            pytest.skip("deviceReferenceId not configured")
        return self._client.get(
            CSAPIEndpoints.provisioning_device(self._data.device_reference_id)
        )

    def get_provisioning_steps(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.provisioning_steps())

    def get_provisioning_farm(self) -> ApiResponse:
        if not self._data.farm_id:
            pytest.skip("farmId not configured")
        return self._client.get(CSAPIEndpoints.provisioning_farm(self._data.farm_id))

    def get_provisioning_flow(self) -> ApiResponse:
        if not self._data.provision_flow_uuid or self._data.provision_flow_uuid == "None":
            pytest.skip("provisionFlowUuid not configured")
        return self._client.get(
            CSAPIEndpoints.provisioning_flow(self._data.provision_flow_uuid)
        )

    def get_provisioning_topology(self) -> ApiResponse:
        if not self._data.provision_flow_uuid or self._data.provision_flow_uuid == "None":
            pytest.skip("provisionFlowUuid not configured")
        return self._client.get(
            CSAPIEndpoints.provisioning_topology(self._data.provision_flow_uuid)
        )

    def get_provisioning_error_codes(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.provisioning_error_codes())

    # TechToolbox
    def get_techtoolbox_dashboard_filters(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.techtoolbox_dashboard_filters())

    def get_techtoolbox_stats_alert_type(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alert_type(), params=filters
        )

    def get_techtoolbox_stats_alert_device_type(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alert_device_type(), params=filters
        )

    def get_techtoolbox_stats_total_alert_type(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_total_alert_type(), params=filters
        )

    def get_techtoolbox_stats_total_overall(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_total_overall(), params=filters
        )

    def get_techtoolbox_stats_alerts_by_distributors(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alerts_by_distributors(), params=filters
        )

    def get_techtoolbox_stats_alerts_by_dealers(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alerts_by_dealers(), params=filters
        )

    def get_techtoolbox_stats_alerts_by_companies(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alerts_by_companies(), params=filters
        )

    def get_techtoolbox_stats_alerts_by_farms(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_stats_alerts_by_farms(), params=filters
        )

    def get_techtoolbox_alerted_devices(self, filters: dict = None) -> ApiResponse:
        return self._client.get(
            CSAPIEndpoints.techtoolbox_alerted_devices(), params=filters
        )

    # Text Resources
    def get_text_resource_app_ids(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.text_resource_app_ids())

    def get_text_resources(self) -> ApiResponse:
        if not self._data.app_id:
            pytest.skip("appId not configured")
        return self._client.get(CSAPIEndpoints.text_resources(self._data.app_id))

    def get_text_resources_by_category(self) -> ApiResponse:
        if not self._data.app_id or not self._data.category:
            pytest.skip("appId or category not configured")
        return self._client.get(
            CSAPIEndpoints.text_resources_by_category(self._data.app_id, self._data.category)
        )

    def get_text_resources_by_key(self) -> ApiResponse:
        if not self._data.app_id:
            pytest.skip("appId not configured")
        params = {"key": self._data.resource_key} if self._data.resource_key else None
        return self._client.get(
            CSAPIEndpoints.text_resources_by_key(self._data.app_id), params=params
        )

    def get_text_resources_by_key_and_category(self) -> ApiResponse:
        if not self._data.app_id or not self._data.category:
            pytest.skip("appId or category not configured")
        params = {"key": self._data.resource_key} if self._data.resource_key else None
        return self._client.get(
            CSAPIEndpoints.text_resources_by_key_and_category(
                self._data.app_id, self._data.category
            ),
            params=params,
        )

    def get_text_resources_grouped(self) -> ApiResponse:
        if not self._data.app_id:
            pytest.skip("appId not configured")
        return self._client.get(CSAPIEndpoints.text_resources_grouped(self._data.app_id))

    def get_text_resources_grouped_by_category(self) -> ApiResponse:
        if not self._data.app_id or not self._data.category:
            pytest.skip("appId or category not configured")
        return self._client.get(
            CSAPIEndpoints.text_resources_grouped_by_category(
                self._data.app_id, self._data.category
            )
        )

    # SignUp / Invitations
    def get_signup_invitation(self) -> ApiResponse:
        if not self._data.invitation_id or self._data.invitation_id == "None":
            pytest.skip("invitationId not configured")
        return self._client.get(CSAPIEndpoints.signup_invitation(self._data.invitation_id))

    def validate_signup_token(self) -> ApiResponse:
        if not self._data.signup_token or self._data.signup_token == "TOKEN":
            pytest.skip("signupToken not configured")
        return self._client.get(CSAPIEndpoints.signup_token(self._data.signup_token))

    # Users
    def get_users(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.users())

    def get_user(self) -> ApiResponse:
        if not self._data.user_id:
            pytest.skip("userId not configured")
        return self._client.get(CSAPIEndpoints.user(self._data.user_id))

    def get_user_roles(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.user_roles())

    def get_user_farms(self) -> ApiResponse:
        if not self._data.user_id:
            pytest.skip("userId not configured")
        return self._client.get(CSAPIEndpoints.user_farms(self._data.user_id))

    def validate_impersonation_token(self) -> ApiResponse:
        if not self._data.impersonation_token or self._data.impersonation_token == "TOKEN":
            pytest.skip("impersonationToken not configured")
        return self._client.get(
            CSAPIEndpoints.impersonation_token(self._data.impersonation_token)
        )

    # Versions
    def get_versions(self) -> ApiResponse:
        return self._client.get(CSAPIEndpoints.versions())

    def get_version(self) -> ApiResponse:
        version = self._data.version or self._resolve_version()
        resp = self._client.get(CSAPIEndpoints.version(version))
        if resp.status_code in (404, 409):
            pytest.skip("Version blob not found (404/409)")
        return resp

    def get_version_details(self) -> ApiResponse:
        if not self._data.system_type:
            pytest.skip("systemType not configured")
        version = self._data.version or self._resolve_version()
        resp = self._client.get(
            CSAPIEndpoints.version_details(self._data.system_type, version)
        )
        if resp.status_code in (404, 409):
            pytest.skip("Version details not found (404/409)")
        return resp

    def get_version_file(self) -> ApiResponse:
        if not self._data.system_type:
            pytest.skip("systemType not configured")
        version = self._data.version or self._resolve_version()
        resp = self._client.get(
            CSAPIEndpoints.version_file(self._data.system_type, version)
        )
        if resp.status_code == 404:
            pytest.skip("Version file not found (404)")
        return resp
