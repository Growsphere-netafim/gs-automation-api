from config.qa1_config import CSAPIConfig


class _StagBase(CSAPIConfig):
    """Base class for all staging service configs.

    Auth details extracted from browser network trace against stag admin portal:
      IDS:          https://stag-netbeatvx-ids-app-weu.azurewebsites.net/
      Auth0 tenant: netafim-test  (id-test.netafim.com)
      client_id:    growsphere-adminportal
      redirect_uri: https://stagnetbeatvxadminst.z6.web.core.windows.net/login-callback

    User identity decoded from stag JWT (yalowe.gibte@netafim.com):
      userId:       46e97dab-0f0e-4c2a-b641-ff1c0b76e8e6
      enterpriseId: 3205
      distributorId: 37e468af-28ec-4c4f-89b3-2eea54257afe
      farms: stag-nb10574, stag-nb10789, stag-nb10878, stag-nb10884,
             stag-nb10898, stag-nb10944, stag-nb10945, stag-nb10988,
             stag-nb10991, stag-nb10998, stag-nb11003, stag-nb11012,
             stag-nb11017, stag-nb11027, stag-nb11045, stag-nb11049,
             stag-nb11070
    """
    ENV_NAME = "stag"
    IDS_URL = "https://stag-netbeatvx-ids-app-weu.azurewebsites.net/"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://stagnetbeatvxadminst.z6.web.core.windows.net/login-callback"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3205,
        "farmId": "stag-nb10574",
        "userId": "46e97dab-0f0e-4c2a-b641-ff1c0b76e8e6",
        "distributorId": "37e468af-28ec-4c4f-89b3-2eea54257afe",
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
        "cropProtocolId": 10,
        "cropUnitId": "0a1e91a7-4223-4e9d-ba84-19d410de1753",
        "deviceId": "48d0ee51-fa56-479f-8e77-3266d9a3ba59",
        "deviceUuid": "48d0ee51-fa56-479f-8e77-3266d9a3ba59",
        "itemGroupId": "96947182-5e88-4f27-30cc-08ddb17af458",
        "itemId": "4c005c8a-ecde-4cc8-35be-08ddb17af481",
        "irrigationBlockId": "f95c0b5d-a470-40fc-9ed1-0f2c2f329950",
        "seasonId": None,
        "parameterId": 1,
        "shapeId": "db8b64cf-a288-4c6c-34c2-08db13e6f959",
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
        "deviceReferenceId": "A0PM5052-R-ETHL2200000211",
        "baseId": "fa573ba6-47f2-42eb-93f1-08870733af79",
        "remoteId": "b5910bd5-914a-42ce-9547-021b8575385a",
        "repeaterId": None,
        "ioId": None,
        "channelId": "1-1-1-0",
        "ioGroupId": "2301e020-45d3-41d7-dab8-08db381d925b",
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
        "deviceId": "E7-00-5D-80",
        "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
        "referenceId": None,
        "flowUuid": None,
        "programUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "irrigationProgramUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "deviceProgramId": 1,
        "baseUuid": "fa573ba6-47f2-42eb-93f1-08870733af79",
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
        "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
        "programUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "deviceProgramId": 1,
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
