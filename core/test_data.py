from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class TestData:
    # Identity / auth
    app_id: str = ""
    culture: str = ""
    unit_system: str = "Metric"
    farm_timezone: str = "UTC"

    # Org hierarchy
    distributor_id: str = ""
    dealer_id: str = ""
    enterprise_id: Any = None
    user_id: str = ""

    # Farm / device
    farm_id: str = ""
    device_id: str = ""
    device_uuid: str = ""
    device_reference_id: str = ""
    device_serial_id: str = ""
    system_type: Any = None

    # Commands / requests
    reference_id: str = ""
    request_id: str = ""
    command_type: Any = None

    # Crop service
    crop_family_id: Any = None
    crop_id: Any = None
    nutrient_id: Any = None
    parameter_aspect_id: Any = None
    parameter_type_id: Any = None
    phenologic_stage_id: Any = None
    protocol_strategy_id: Any = None
    soil_type_id: Any = None
    variety_id: Any = None
    protocol_id: Any = None
    parameter_id: Any = None

    # Data API
    crop_protocol_id: Any = None
    crop_unit_id: str = ""
    item_group_id: Optional[str] = None
    item_id: Optional[str] = None
    irrigation_block_id: str = ""
    season_id: Optional[str] = None
    shape_id: str = ""
    date: str = ""
    year: Any = None
    month: Any = None
    day: Any = None
    include: str = ""

    # Irrigation / programs
    program_uuid: str = ""
    irrigation_program_uuid: str = ""
    device_program_id: Any = None
    mainline_id: Any = None
    recipe_id: Optional[str] = None
    io_id: str = ""
    start_date: str = ""
    end_date: str = ""
    days_back: Any = None
    updated_date_utc: str = ""
    timestamp: str = ""

    # FieldIO
    base_id: str = ""
    remote_id: str = ""
    repeater_id: Optional[str] = None
    channel_id: str = ""
    io_group_id: str = ""
    threshold_id: Optional[str] = None
    io_device_type_id: Any = None
    io_type_id: Any = None
    system_type_id: Any = None
    icon_id: Optional[str] = None
    include_deleted: bool = False
    include_inactive: bool = False
    only_active_devices: bool = True
    from_date: str = ""
    to_date: str = ""
    page: int = 1
    page_size: int = 10

    # LookupService
    irrigation_method_id: Any = None
    uom_id: Any = None
    country_iso_symbol: str = ""
    field: Optional[str] = None

    # Mobile
    base_uuid: str = ""
    flow_uuid: Optional[str] = None
    user_device_graph_id: Optional[str] = None

    # Report API / Settings
    category: str = ""
    resource_key: str = ""
    ticket_id: str = ""
    provision_flow_uuid: str = ""
    invitation_id: str = ""
    signup_token: str = ""
    impersonation_token: str = ""
    version: str = ""

    # WeatherForecast
    average_years: Any = None

    # CSAPI / misc
    from_date_time_utc: str = ""
    to_date_time_utc: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "TestData":
        key_map = {
            "appId": "app_id",
            "culture": "culture",
            "unitSystem": "unit_system",
            "farmTimezone": "farm_timezone",
            "distributorId": "distributor_id",
            "dealerId": "dealer_id",
            "enterpriseId": "enterprise_id",
            "userId": "user_id",
            "farmId": "farm_id",
            "deviceId": "device_id",
            "deviceUuid": "device_uuid",
            "deviceReferenceId": "device_reference_id",
            "deviceSerialId": "device_serial_id",
            "systemType": "system_type",
            "referenceId": "reference_id",
            "requestId": "request_id",
            "commandType": "command_type",
            "cropFamilyId": "crop_family_id",
            "cropId": "crop_id",
            "nutrientId": "nutrient_id",
            "parameterAspectId": "parameter_aspect_id",
            "parameterTypeId": "parameter_type_id",
            "phenologicStageId": "phenologic_stage_id",
            "protocolStrategyId": "protocol_strategy_id",
            "soilTypeId": "soil_type_id",
            "varietyId": "variety_id",
            "protocolId": "protocol_id",
            "parameterId": "parameter_id",
            "cropProtocolId": "crop_protocol_id",
            "cropUnitId": "crop_unit_id",
            "itemGroupId": "item_group_id",
            "itemId": "item_id",
            "irrigationBlockId": "irrigation_block_id",
            "seasonId": "season_id",
            "shapeId": "shape_id",
            "date": "date",
            "year": "year",
            "month": "month",
            "day": "day",
            "include": "include",
            "programUuid": "program_uuid",
            "irrigationProgramUuid": "irrigation_program_uuid",
            "deviceProgramId": "device_program_id",
            "mainlineId": "mainline_id",
            "recipeId": "recipe_id",
            "ioId": "io_id",
            "startDate": "start_date",
            "endDate": "end_date",
            "daysBack": "days_back",
            "updatedDateUtc": "updated_date_utc",
            "timestamp": "timestamp",
            "baseId": "base_id",
            "remoteId": "remote_id",
            "repeaterId": "repeater_id",
            "channelId": "channel_id",
            "ioGroupId": "io_group_id",
            "thresholdId": "threshold_id",
            "ioDeviceTypeId": "io_device_type_id",
            "ioTypeId": "io_type_id",
            "systemTypeId": "system_type_id",
            "iconId": "icon_id",
            "includeDeleted": "include_deleted",
            "includeInactive": "include_inactive",
            "onlyActiveDevices": "only_active_devices",
            "from": "from_date",
            "to": "to_date",
            "page": "page",
            "pageSize": "page_size",
            "irrigationMethodId": "irrigation_method_id",
            "uomId": "uom_id",
            "countryIsoSymbol": "country_iso_symbol",
            "field": "field",
            "baseUuid": "base_uuid",
            "flowUuid": "flow_uuid",
            "userDeviceGraphId": "user_device_graph_id",
            "category": "category",
            "resourceKey": "resource_key",
            "ticketId": "ticket_id",
            "provisionFlowUuid": "provision_flow_uuid",
            "invitationId": "invitation_id",
            "signupToken": "signup_token",
            "impersonationToken": "impersonation_token",
            "version": "version",
            "avarageYears": "average_years",
            "fromDateTimeUtc": "from_date_time_utc",
            "toDateTimeUtc": "to_date_time_utc",
        }
        kwargs = {}
        for raw_key, attr in key_map.items():
            if raw_key in d:
                kwargs[attr] = d[raw_key]
        return cls(**kwargs)
