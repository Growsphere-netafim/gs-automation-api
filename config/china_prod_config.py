from config.qa1_config import CSAPIConfig


class _ChinaProdBase(CSAPIConfig):
    """Base class for all China production service configs.

    Auth details extracted from browser network trace against China prod admin portal:
      Admin portal: https://stadminappprod.z5.web.core.chinacloudapi.cn/login
      Auth0 domain: id.netafim.cn  (tenant: china-prod)
      IDS URL:      https://app-ids.k8s.growsphere.netafim.cn
      client_id:    growsphere-adminportal
      redirect_uri: https://stadminappprod.z5.web.core.chinacloudapi.cn/login-callback

    User identity for takego5188@huizk.com (role: SuperAdmin) in China PROD:
      userId (sub):  b189f8d5-d110-46ba-8fb3-b6c419a62e09
      enterpriseId: 3001 (Global default distributor)
      distributorId: c4704cf7-ff5e-44a9-ae2e-0af2a47c519d
      dealerId:      bfa2a998-f6b4-45f3-854f-0ba83f513d7b
      farmId:        prod-nb10006 (Alon_Test_Magal)

    SuperAdmin role has full visibility across all China PROD services
    (CSAPI, DataAPI, Mobile BFF, Irrigation, etc.).

    Pipeline variable group: gs-automation-api-china-prod
      PASSWORD must be set to the password for takego5188@huizk.com.
    """
    ENV_NAME = "china_prod"
    IDS_URL = "https://app-ids.k8s.growsphere.netafim.cn"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://stadminappprod.z5.web.core.chinacloudapi.cn/login-callback"
    SCOPES_VAL = "openid%20profile%20NbPortal%20NbPortal.w%20farms%20offline_access"
    USER_EMAIL = "takego5188@huizk.com"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3001,
        "farmId": "prod-nb10006",
        "userId": "b189f8d5-d110-46ba-8fb3-b6c419a62e09",
        "distributorId": "c4704cf7-ff5e-44a9-ae2e-0af2a47c519d",
        "dealerId": "bfa2a998-f6b4-45f3-854f-0ba83f513d7b",
    })


class ChinaProdCSAPIConfig(_ChinaProdBase):
    BASE_URL = "https://csapi.k8s.growsphere.netafim.cn"


class ChinaProdCropServiceConfig(_ChinaProdBase):
    BASE_URL = "https://cropservice.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
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


class ChinaProdDataAPIConfig(_ChinaProdBase):
    BASE_URL = "https://dataapi.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
        "cropProtocolId": 10,
        "cropUnitId": None,
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


class ChinaProdLookupServiceConfig(_ChinaProdBase):
    BASE_URL = "https://app-lookup-prod-china.chinacloudsites.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "irrigationMethodId": 1,
        "uomId": 1,
        "countryIsoSymbol": "US",
        "unitSystem": "Metric",
        "includeInactive": False,
        "field": None,
    })


class ChinaProdFieldIOConfig(_ChinaProdBase):
    BASE_URL = "https://fieldio.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
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


class ChinaProdMobileConfig(_ChinaProdBase):
    BASE_URL = "https://mobilebff.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
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


class ChinaProdIrrigationConfig(_ChinaProdBase):
    BASE_URL = "https://irrigation.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
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


class ChinaProdIrrigationManagerConfig(_ChinaProdBase):
    BASE_URL = "https://irrigationmanager.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "unitSystem": "SI",
        "farmTimezone": "China Standard Time",
    })


class ChinaProdCommandsManagerConfig(_ChinaProdBase):
    BASE_URL = "https://commandsmanager.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
        "deviceId": None,
        "referenceId": None,
        "unitSystem": "Metric",
        "farmTimezone": "China Standard Time",
    })


class ChinaProdDeviceStateManagerConfig(_ChinaProdBase):
    BASE_URL = "https://devicestatemanager.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "prod-nb10006",
        "deviceId": None,
        "deviceUuid": None,
        "systemType": 1,
        "fromDateTimeUtc": "2024-01-01T00:00:00Z",
        "toDateTimeUtc": "2024-01-31T23:59:59Z",
    })


class ChinaProdWeatherForecastConfig(_ChinaProdBase):
    BASE_URL = "https://weatherforecast.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "avarageYears": 3,
    })


class ChinaProdReportAPIConfig(_ChinaProdBase):
    BASE_URL = "https://app-reportapi-prod-china.chinacloudsites.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "userId": "b189f8d5-d110-46ba-8fb3-b6c419a62e09",
    })


class ChinaProdSettingsAPIConfig(_ChinaProdBase):
    BASE_URL = "https://settingsapi.k8s.growsphere.netafim.cn"
    TEST_DATA = _ChinaProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceUuid": None,
    })
