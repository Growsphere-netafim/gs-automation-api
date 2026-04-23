from config.qa1_config import CSAPIConfig


class _ChinaStagBase(CSAPIConfig):
    """Base class for all China staging service configs.

    Auth details discovered from china_stag admin portal SPA + IDS discovery:
      Admin portal: https://stadminappstag.z5.web.core.chinacloudapi.cn/login
      IDS URL:      https://app-ids-stag.k8s.growsphere.netafim.cn
      Auth0 tenant: china-staging (see core/auth.py _tenant_map)
      client_id:    growsphere-adminportal
      redirect_uri: https://stadminappstag.z5.web.core.chinacloudapi.cn/login-callback

    User identity for capemek694@avastu.com (role: Manager + SuperAdmin) in China STAG:
      userId (sub):   8cb4e253-101b-40ca-98fa-1436602dfab8
      enterpriseId:   3005 (QA-TEST — the enterprise that owns stag-nb10000)
      distributorId:  a2d327a0-2028-4391-9077-74f380f0f824 (Global China Test)
      dealerId:       38f36592-4426-4a50-bec9-a9ae13825b5b (Global default dealer)
      farmId:         stag-nb10000 (Yakir china)

    Pipeline variable group: gs-automation-api-china-stag
      PASSWORD must be set to the password for capemek694@avastu.com.
    """
    ENV_NAME = "china_stag"
    IDS_URL = "https://app-ids-stag.k8s.growsphere.netafim.cn"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://stadminappstag.z5.web.core.chinacloudapi.cn/login-callback"
    SCOPES_VAL = "openid%20profile%20NbPortal%20NbPortal.w%20farms%20offline_access"
    USER_EMAIL = "capemek694@avastu.com"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3005,
        "farmId": "stag-nb10000",
        "userId": "8cb4e253-101b-40ca-98fa-1436602dfab8",
        "distributorId": "a2d327a0-2028-4391-9077-74f380f0f824",
        "dealerId": "38f36592-4426-4a50-bec9-a9ae13825b5b",
    })


class ChinaStagCSAPIConfig(_ChinaStagBase):
    BASE_URL = "https://csapi-stag.k8s.growsphere.netafim.cn"


class ChinaStagCropServiceConfig(_ChinaStagBase):
    BASE_URL = "https://cropservice-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
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
        "irrigationBlockId": None,
    })


class ChinaStagDataAPIConfig(_ChinaStagBase):
    BASE_URL = "https://dataapi-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "cropProtocolId": 10,
        "cropUnitId": "5d58e0e5-d539-4588-8d13-feac52c1b917",
        "deviceId": None,
        "deviceUuid": None,
        "irrigationBlockId": None,
        "itemGroupId": None,
        "itemId": None,
        "shapeId": None,
        "seasonId": None,
        "parameterId": 1,
        "date": "2024-01-01",
        "year": 2024,
        "month": 1,
        "day": 1,
        "include": "devices",
        "page": 1,
        "pageSize": 10,
    })


class ChinaStagLookupServiceConfig(_ChinaStagBase):
    BASE_URL = "https://app-lookup-stag-china.chinacloudsites.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "irrigationMethodId": 1,
        "uomId": 1,
        "countryIsoSymbol": "US",
        "unitSystem": "Metric",
        "includeInactive": False,
        "field": None,
    })


class ChinaStagFieldIOConfig(_ChinaStagBase):
    BASE_URL = "https://fieldio-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "deviceReferenceId": None,
        "baseId": None,
        "remoteId": None,
        "repeaterId": None,
        "ioId": None,
        "channelId": None,
        "ioGroupId": None,
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
        "farmTimezone": "China Standard Time",
    })


class ChinaStagMobileConfig(_ChinaStagBase):
    BASE_URL = "https://mobilebff-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "deviceId": None,
        "deviceUuid": None,
        "referenceId": None,
        "flowUuid": None,
        "programUuid": None,
        "irrigationProgramUuid": None,
        "deviceProgramId": None,
        "baseUuid": None,
        "userDeviceGraphId": None,
        "commandType": 1,
        "systemType": 1,
        "unitSystem": "Metric",
        "farmTimezone": "China Standard Time",
    })


class ChinaStagIrrigationConfig(_ChinaStagBase):
    BASE_URL = "https://irrigation-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "deviceUuid": None,
        "programUuid": None,
        "deviceProgramId": None,
        "mainlineId": None,
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


class ChinaStagIrrigationManagerConfig(_ChinaStagBase):
    BASE_URL = "https://irrigationmanager-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "unitSystem": "SI",
        "farmTimezone": "China Standard Time",
    })


class ChinaStagCommandsManagerConfig(_ChinaStagBase):
    BASE_URL = "https://commandsmanager-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "deviceId": None,
        "referenceId": None,
        "unitSystem": "Metric",
        "farmTimezone": "China Standard Time",
    })


class ChinaStagDeviceStateManagerConfig(_ChinaStagBase):
    BASE_URL = "https://devicestatemanager-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "stag-nb10000",
        "deviceId": None,
        "deviceUuid": None,
        "systemType": 1,
        "fromDateTimeUtc": "2024-01-01T00:00:00Z",
        "toDateTimeUtc": "2024-01-31T23:59:59Z",
    })


class ChinaStagWeatherForecastConfig(_ChinaStagBase):
    BASE_URL = "https://weatherforecast-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "avarageYears": 3,
    })


class ChinaStagReportAPIConfig(_ChinaStagBase):
    BASE_URL = "https://app-reportapi-stag-china.chinacloudsites.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "userId": "8cb4e253-101b-40ca-98fa-1436602dfab8",
    })


class ChinaStagSettingsAPIConfig(_ChinaStagBase):
    BASE_URL = "https://settingsapi-stag.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaStagBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceUuid": None,
    })
