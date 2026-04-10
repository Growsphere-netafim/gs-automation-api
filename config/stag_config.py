from config.qa1_config import CSAPIConfig


class _StagBase(CSAPIConfig):
    """Base class for all staging service configs.

    Auth details extracted from browser network trace against stag admin portal:
      IDS:          https://stag-netbeatvx-ids-app-weu.azurewebsites.net/
      Auth0 tenant: netafim-test  (id-test.netafim.com)
      client_id:    growsphere-adminportal
      redirect_uri: https://stagnetbeatvxadminst.z6.web.core.windows.net/login-callback

    User identity for yakir.moshe@netafim.com in STAG:
      userId:       5438128e-20d2-4464-b9c6-2f12b4a69fa1
      enterpriseId: 3131  (name: "Dvir")
      distributorId: 09b8ee97-416f-43b9-864e-316dc31e32ce  (Global default distributor)
      dealerId:     37e468af-28ec-4c4f-89b3-2eea54257afe  (Global default dealer)
      farms (enterprise 3131): stag-nb10324, stag-nb10361, stag-nb10573, stag-nb10775, stag-nb10893
      farmId used for FieldIO/DataAPI data: stag-nb10574  (overridden per service below)
    """
    ENV_NAME = "stag"
    IDS_URL = "https://stag-netbeatvx-ids-app-weu.azurewebsites.net/"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://stagnetbeatvxadminst.z6.web.core.windows.net/login-callback"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3131,
        "farmId": "stag-nb10324",   # enterprise 3131 farm — used by CSAPI tests
        "userId": "5438128e-20d2-4464-b9c6-2f12b4a69fa1",
        "distributorId": "09b8ee97-416f-43b9-864e-316dc31e32ce",
        "dealerId": "37e468af-28ec-4c4f-89b3-2eea54257afe",
    })


class StagCSAPIConfig(_StagBase):
    BASE_URL = "https://csapi-stag.k8s.growsphere.netafim.com"


class StagCropServiceConfig(_StagBase):
    BASE_URL = "https://cropservice-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "cropFamilyId": 1,
        "cropId": 1,
        "nutrientId": 1,
        "parameterAspectId": 1,
        "parameterTypeId": 1,
        "phenologicStageId": 1,
        "protocolStrategyId": 1,
        "soilTypeId": 1,
        "varietyId": 1,
        "protocolId": 1,
        "irrigationBlockId": "a217e28d-7aa1-43dc-9ae9-1996d1037395",
    })


class StagDataAPIConfig(_StagBase):
    BASE_URL = "https://dataapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        # stag-nb10574 is the farm with actual CropUnits and IrrigationBlocks data
        "farmId": "stag-nb10574",
        "cropProtocolId": 10,
        "cropUnitId": "10af6b5f-8d8f-4ba3-a844-01d5d8d3a5c5",
        "deviceId": "7527bfef-22bc-4ff6-b1b7-3ee8d007c0e5",
        "deviceUuid": "7527bfef-22bc-4ff6-b1b7-3ee8d007c0e5",
        "itemGroupId": None,             # no ItemGroups exist in stag-nb10574
        "itemId": None,                  # no Items exist in stag-nb10574
        "irrigationBlockId": "70929175-d2a6-420e-b5ab-069d76ab05a3",
        "seasonId": None,
        "parameterId": 1,
        "shapeId": None,                 # no Shapes exist in STAG for this user
        "date": "2024-01-01",
        "year": 2024,
        "month": 1,
        "day": 1,
        "include": "devices",
    })


class StagLookupServiceConfig(_StagBase):
    # Azure-hosted stag instance (per Swagger environments)
    BASE_URL = "https://stag-netbeatvx-lookup-app-weu.azurewebsites.net"
    # k8s-hosted stag instance (newer, used by the frontend — CORS bug was here)
    K8S_BASE_URL = "https://lookup-stag.k8s.growsphere.netafim.com"

    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "irrigationMethodId": 1,
        "uomId": 1,
        "countryIsoSymbol": "US",
        "unitSystem": "Metric",
        "includeInactive": False,
        "field": None,
    })


class StagFieldIOConfig(_StagBase):
    BASE_URL = "https://fieldio-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        # stag-nb10574 is the farm that has actual FieldIO devices/bases
        "farmId": "stag-nb10574",
        "deviceReferenceId": "A0PM5052-R-ETHL2200000242",
        "baseId": "f4e12747-ae0f-455e-9d69-359c9f630e74",    # E7-00-53-C2 base
        "remoteId": "854426a1-bd36-446a-8e6b-093b72e9589c",
        "repeaterId": None,
        "ioId": None,
        "channelId": "1-1-1-0",
        "ioGroupId": "15f5781f-94cd-43a2-cecf-08da6b0df4dc",
        "thresholdId": None,
        "ioDeviceTypeId": 1,
        "ioTypeId": 4,
        "systemTypeId": 1,
        "iconId": None,
        "includeDeleted": False,
        "includeInactive": False,
        "onlyActiveDevices": True,
        "from": "2024-01-01",
        "to": "2024-12-31",
        "page": 1,
        "pageSize": 10,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class StagMobileConfig(_StagBase):
    BASE_URL = "https://mobilebff-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        # stag-nb10574 is the farm with mobile devices
        "farmId": "stag-nb10574",
        "deviceId": "E7-00-53-C2",
        "deviceUuid": "f4e12747-ae0f-455e-9d69-359c9f630e74",
        "referenceId": None,
        "flowUuid": None,
        "programUuid": None,             # no irrigation programs in STAG for this user/farm
        "irrigationProgramUuid": None,   # no irrigation programs in STAG for this user/farm
        "deviceProgramId": None,
        "baseUuid": "f4e12747-ae0f-455e-9d69-359c9f630e74",  # E7-00-53-C2
        "userDeviceGraphId": None,
        "commandType": 1,
        "systemType": 1,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class StagIrrigationConfig(_StagBase):
    BASE_URL = "https://irrigation-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        # stag-nb10574 + A0PM5052-R-ETHL2200000242 device has mainlines
        "farmId": "stag-nb10574",
        "deviceUuid": "7527bfef-22bc-4ff6-b1b7-3ee8d007c0e5",  # A0PM5052-R-ETHL2200000242
        "programUuid": None,             # no program schemes in STAG for this user/farm
        "deviceProgramId": None,
        "mainlineId": 1,
        "recipeId": None,
        "ioId": None,
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "date": "2024-01-01",
        "daysBack": 7,
        "systemType": "Flex",
        "updatedDateUtc": "2024-01-01T00:00:00Z",
        "timestamp": "2024-01-01T00:00:00Z",
    })


class StagIrrigationManagerConfig(_StagBase):
    BASE_URL = "https://irrigationmanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "unitSystem": "SI",
        "farmTimezone": "Israel Standard Time",
    })


class StagCommandsManagerConfig(_StagBase):
    BASE_URL = "https://commandsmanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceId": "E7-00-5D-80",
        "referenceId": None,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class StagDeviceStateManagerConfig(_StagBase):
    BASE_URL = "https://devicestatemanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceId": "E7-00-5D-80",
        "deviceUuid": None,
        "systemType": 1,
        "fromDateTimeUtc": "2024-01-01T00:00:00Z",
        "toDateTimeUtc": "2024-01-31T23:59:59Z",
    })


class StagWeatherForecastConfig(_StagBase):
    BASE_URL = "https://weatherforecast-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "avarageYears": 3,
    })


class StagReportAPIConfig(_StagBase):
    BASE_URL = "https://reportapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()


class StagSettingsAPIConfig(_StagBase):
    BASE_URL = "https://settingsapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceUuid": None,
    })


class StagAccountManagementConfig(_StagBase):
    BASE_URL = "https://accountmanagement-stag.k8s.growsphere.netafim.com"
    TEST_DATA = _StagBase.TEST_DATA.copy()
