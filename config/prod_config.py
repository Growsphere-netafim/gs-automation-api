from config.qa1_config import CSAPIConfig


class _ProdBase(CSAPIConfig):
    """Base class for all production service configs.

    Auth details extracted from browser network trace against prod admin portal:
      IDS:          https://prod-netbeatvx-ids-app-weu.azurewebsites.net/
      Auth0 tenant: netafim  (id.netafim.com)
      client_id:    growsphere-adminportal
      redirect_uri: https://prodnetbeatvxadminst.z6.web.core.windows.net/login-callback

    User identity decoded from prod JWT (yalowe.gibte@netafim.com):
      userId:       7efe92c5-a42f-4920-917e-e91220e22c45
      enterpriseId: 3120
      distributorId: 852a1699-71af-4653-9c6e-1e4be9ccb044
      farms: prod-nb10023, prod-nb10525, prod-nb11220, prod-nb12854,
             prod-nb12859, prod-nb12860, prod-nb12867, prod-nb12888
    """
    ENV_NAME = "prod"
    IDS_URL = "https://prod-netbeatvx-ids-app-weu.azurewebsites.net/"
    OIDC_CLIENT_ID = "growsphere-adminportal"
    OIDC_REDIRECT_URI = "https://prodnetbeatvxadminst.z6.web.core.windows.net/login-callback"

    TEST_DATA = CSAPIConfig.TEST_DATA.copy()
    TEST_DATA.update({
        "enterpriseId": 3120,
        "farmId": "prod-nb10023",
        "userId": "7efe92c5-a42f-4920-917e-e91220e22c45",
        "distributorId": "852a1699-71af-4653-9c6e-1e4be9ccb044",
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
        "irrigationBlockId": "a217e28d-7aa1-43dc-9ae9-1996d1037395",
    })


class ProdDataAPIConfig(_ProdBase):
    BASE_URL = "https://dataapi.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "cropProtocolId": 10,
        "cropUnitId": "0a1e91a7-4223-4e9d-ba84-19d410de1753",
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
        "ioDeviceTypeId": 1,
        "ioTypeId": 4,
        "systemTypeId": 1,
        "includeDeleted": False,
        "includeInactive": False,
        "onlyActiveDevices": True,
        "page": 1,
        "pageSize": 10,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class ProdMobileConfig(_ProdBase):
    BASE_URL = "https://mobilebff.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceId": "E7-00-5D-80",
        "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
        "programUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "irrigationProgramUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "deviceProgramId": 1,
        "baseUuid": "fa573ba6-47f2-42eb-93f1-08870733af79",
        "commandType": 1,
        "systemType": 1,
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class ProdIrrigationConfig(_ProdBase):
    BASE_URL = "https://irrigation.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
        "programUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
        "deviceProgramId": 1,
        "mainlineId": 1,
        "startDate": "2024-01-01",
        "endDate": "2024-01-31",
        "date": "2024-01-01",
        "daysBack": 7,
        "systemType": "Flex",
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
        "deviceId": "E7-00-5D-80",
        "unitSystem": "Metric",
        "farmTimezone": "Israel Standard Time",
    })


class ProdDeviceStateManagerConfig(_ProdBase):
    BASE_URL = "https://devicestatemanager.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "deviceId": "E7-00-5D-80",
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
    BASE_URL = "https://reportapi.k8s.growsphere.netafim.com"
    TEST_DATA = _ProdBase.TEST_DATA.copy()
    TEST_DATA.update({
        "userId": "48f37eda-233e-45cd-bee7-ae204fe94d60",
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
