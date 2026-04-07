from config.qa1_config import CSAPIConfig


class StagCSAPIConfig(CSAPIConfig):
    BASE_URL = "https://csapi-stag.k8s.growsphere.netafim.com"


class StagCropServiceConfig(CSAPIConfig):
    BASE_URL = "https://cropservice-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
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


class StagDataAPIConfig(CSAPIConfig):
    BASE_URL = "https://dataapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb14911",
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


class StagLookupServiceConfig(CSAPIConfig):
    # Azure-hosted stag instance (per Swagger environments)
    BASE_URL = "https://stag-netbeatvx-lookup-app-weu.azurewebsites.net"
    # k8s-hosted stag instance (newer, used by the frontend)
    K8S_BASE_URL = "https://lookup-stag.k8s.growsphere.netafim.com"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "irrigationMethodId": 1,
        "uomId": 1,
        "countryIsoSymbol": "US",
        "unitSystem": "Metric",
        "includeInactive": False,
        "field": None,
    })


class StagFieldIOConfig(CSAPIConfig):
    BASE_URL = "https://fieldio-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
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


class StagMobileConfig(CSAPIConfig):
    BASE_URL = "https://mobilebff-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
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


class StagIrrigationConfig(CSAPIConfig):
    BASE_URL = "https://irrigation-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
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


class StagIrrigationManagerConfig(CSAPIConfig):
    BASE_URL = "https://irrigationmanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
        "unitSystem": "SI",
        "farmTimezone": "Israel Standard Time",
    })


class StagCommandsManagerConfig(CSAPIConfig):
    BASE_URL = "https://commandsmanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
        "deviceId": "E7-00-5D-80",
        "referenceId": None,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class StagDeviceStateManagerConfig(CSAPIConfig):
    BASE_URL = "https://devicestatemanager-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceId": "E7-00-5D-80",
        "deviceUuid": None,
        "farmId": "qa1-nb10047",
        "systemType": 1,
        "fromDateTimeUtc": "2024-01-01T00:00:00Z",
        "toDateTimeUtc": "2024-01-31T23:59:59Z",
    })


class StagWeatherForecastConfig(CSAPIConfig):
    BASE_URL = "https://weatherforecast-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "avarageYears": 3,
    })


class StagReportAPIConfig(CSAPIConfig):
    BASE_URL = "https://reportapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb14911",
        "userId": "48f37eda-233e-45cd-bee7-ae204fe94d60",
    })


class StagSettingsAPIConfig(CSAPIConfig):
    BASE_URL = "https://settingsapi-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "farmId": "qa1-nb10047",
        "deviceUuid": None,
    })


class StagAccountManagementConfig(CSAPIConfig):
    BASE_URL = "https://accountmanagement-stag.k8s.growsphere.netafim.com"
    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
