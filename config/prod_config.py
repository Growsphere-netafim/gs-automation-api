from config.qa1_config import CSAPIConfig


class _ProdBase(CSAPIConfig):
    """Base class for all production service configs.

    Auth details extracted from browser network trace against prod admin portal:
      IDS:          https://prod-netbeatvx-ids-app-weu.azurewebsites.net/
      Auth0 tenant: netafim  (id.netafim.com)
      client_id:    growsphere-adminportal
      redirect_uri: https://prodnetbeatvxadminst.z6.web.core.windows.net/login-callback

    User identity for yakir.moshe@netafim.com in PROD:
      userId:       fc0d5d86-f765-48cc-8741-548cdb7d38c1
      enterpriseId: 3497  (name: "Qqq")
      distributorId: d662300e-01ef-476d-8437-19ebb80d6e33  (IL)
      dealerId:     88ea3d84-57dd-4d5d-9d1b-1c21c97cb2c8  (Israel)
      farms (enterprise 3497): prod-nb10525, prod-nb10704, prod-nb10705, ...
      farmId used for FieldIO/DataAPI/Mobile/Irrigation: prod-nb10704  (eYehudit — has FieldIO devices)
    """
    ENV_NAME = "prod"
    IDS_URL = "https://prod-netbeatvx-ids-app-weu.azurewebsites.net/"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://prodnetbeatvxadminst.z6.web.core.windows.net/login-callback"
    SCOPES_VAL = "openid%20profile%20NbPortal%20NbPortal.w%20farms%20offline_access"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3497,
        "farmId": "prod-nb10525",   # enterprise 3497 farm — used by CSAPI tests
        "userId": "fc0d5d86-f765-48cc-8741-548cdb7d38c1",
        "distributorId": "d662300e-01ef-476d-8437-19ebb80d6e33",
        "dealerId": "88ea3d84-57dd-4d5d-9d1b-1c21c97cb2c8",
    })


class ProdCSAPIConfig(_ProdBase):
    BASE_URL = "https://csapi.k8s.growsphere.netafim.com"


class ProdCropServiceConfig(_ProdBase):
    BASE_URL = "https://cropservice.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
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
        "irrigationBlockId": None,   # no IrrigationBlocks in PROD for this user
    })


class ProdDataAPIConfig(_ProdBase):
    BASE_URL = "https://dataapi.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        # prod-nb10704 is the farm with FieldIO devices
        "farmId": "prod-nb10704",
        "cropProtocolId": 10,
        "cropUnitId": None,          # no CropUnits exist in PROD for this user
        "deviceId": "18766562-e4c3-4a2d-b302-0ac3bb6775c3",   # A0PM5052-R-ETHL2200000248
        "deviceUuid": "18766562-e4c3-4a2d-b302-0ac3bb6775c3",
        "irrigationBlockId": None,   # no IrrigationBlocks in PROD for this user
        "itemGroupId": None,         # no ItemGroups in PROD for this user
        "itemId": None,              # no Items in PROD for this user
        "shapeId": None,             # no Shapes in PROD for this user
        "seasonId": None,
        "parameterId": 1,
        "date": "2024-01-01",
        "year": 2024,
        "month": 1,
        "day": 1,
        "include": "devices",
    })


class ProdLookupServiceConfig(_ProdBase):
    BASE_URL = "https://prod-netbeatvx-lookup-app-weu.azurewebsites.net"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "irrigationMethodId": 1,
        "uomId": 1,
        "countryIsoSymbol": "US",
        "unitSystem": "Metric",
        "includeInactive": False,
        "field": None,
    })


class ProdFieldIOConfig(_ProdBase):
    BASE_URL = "https://fieldio.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        # prod-nb10704 is the farm with actual FieldIO devices/bases
        "farmId": "prod-nb10704",
        "deviceReferenceId": "A0PM5052-R-ETHL2200000248",
        "baseId": "8fdf46b2-2733-41c4-8201-0716cc837812",    # E7-00-53-C5 base
        "remoteId": "4783a3e1-fbaf-4747-861c-ffbf85f125fe",
        "repeaterId": None,
        "ioId": "744c1bd6-1fb7-44c4-2ae6-08da5aa6f94f",
        "channelId": "1-1-1-0",
        "ioGroupId": "a01bd4a6-820d-490b-a077-08da5aa6f94c",
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


class ProdMobileConfig(_ProdBase):
    BASE_URL = "https://mobilebff.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        # prod-nb10704 is the farm with mobile devices
        "farmId": "prod-nb10704",
        "deviceId": "E7-00-53-C5",
        "deviceUuid": "8fdf46b2-2733-41c4-8201-0716cc837812",
        "referenceId": None,
        "flowUuid": None,
        "programUuid": None,              # no irrigation programs in PROD for this user/farm
        "irrigationProgramUuid": None,    # no irrigation programs in PROD for this user/farm
        "deviceProgramId": None,
        "baseUuid": "8fdf46b2-2733-41c4-8201-0716cc837812",   # E7-00-53-C5
        "userDeviceGraphId": None,
        "commandType": 1,
        "systemType": 1,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class ProdIrrigationConfig(_ProdBase):
    BASE_URL = "https://irrigation.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        # prod-nb10704 + A0PM5052-R-ETHL2200000248 device
        "farmId": "prod-nb10704",
        "deviceUuid": "18766562-e4c3-4a2d-b302-0ac3bb6775c3",  # A0PM5052-R-ETHL2200000248
        "programUuid": None,           # no program schemes in PROD for this user/farm
        "deviceProgramId": None,
        "mainlineId": None,            # no mainlines in PROD for this user/farm
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


class ProdIrrigationManagerConfig(_ProdBase):
    BASE_URL = "https://irrigationmanager.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "unitSystem": "SI",
        "farmTimezone": "Israel Standard Time",
    })


class ProdCommandsManagerConfig(_ProdBase):
    BASE_URL = "https://commandsmanager.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10704",
        "deviceId": "E7-00-53-C5",
        "referenceId": None,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class ProdDeviceStateManagerConfig(_ProdBase):
    BASE_URL = "https://devicestatemanager.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10704",
        "deviceId": "E7-00-53-C5",
        "deviceUuid": "8fdf46b2-2733-41c4-8201-0716cc837812",
        "systemType": 1,
        "fromDateTimeUtc": "2024-01-01T00:00:00Z",
        "toDateTimeUtc": "2024-01-31T23:59:59Z",
    })


class ProdWeatherForecastConfig(_ProdBase):
    BASE_URL = "https://weatherforecast.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "avarageYears": 3,
    })


class ProdReportAPIConfig(_ProdBase):
    # NOTE: reportapi.k8s.growsphere.netafim.com does not resolve in DNS —
    # this service may not yet be deployed in the PROD k8s cluster.
    BASE_URL = "https://reportapi.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "userId": "fc0d5d86-f765-48cc-8741-548cdb7d38c1",   # yakir.moshe@netafim.com prod userId
    })


class ProdSettingsAPIConfig(_ProdBase):
    BASE_URL = "https://settingsapi.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceUuid": None,
    })


class ProdAccountManagementConfig(_ProdBase):
    BASE_URL = "https://accountmanagement.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
