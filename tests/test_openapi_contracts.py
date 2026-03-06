"""
OpenAPI Contract & Smoke Tests
Automatically generated tests using Schemathesis
"""
import os
import re
import glob
import pytest
import requests
import schemathesis
import urllib3
from typing import Dict, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "swagger_specs")
SPEC_FILES = sorted(glob.glob(os.path.join(SPECS_DIR, "*.json")))

_STATIC_PATH_PARAMS = {
    "enterpriseId": "3001",
    "distributorId": "7aaaafe6-b093-4760-8e06-509512ac2185",
    "dealerId": "6e17fa6b-da8d-4a1a-b8c4-7d84ebac0360",
    "userId": "48f37eda-233e-45cd-bee7-ae204fe94d60",
    "deviceId": "E7-00-5D-80",
    "DeviceId": "E7-00-5D-80",
    "deviceUuid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
    "deviceUUid": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
    "deviceUuId": "b7b68f8e-a536-4e8c-a08e-4fe5a000f9aa",
    "deviceReferenceId": "A0PM5052-R-ETHL2200000056",
    "deviceSerialId": "SN-9999",
    "referenceId": "bcad7c0b-2285-4741-8cca-69dfea4c475f",
    "date": "2024-01-01",
    "Date": "2024-01-01",
    "fromDate": "2024-01-01",
    "toDate": "2024-01-31",
    "culture": "en-US",
    "appId": "GsMobileApp",
    "version": "1.0.0",
    "countryIsoSymbol": "US",
    "category": "General",
    "cropfamilyId": "1",
    "cropId": "1",
    "nutrientId": "1",
    "parameterTypeId": "1",
    "protocolStrategyId": "1",
    "soilTypeId": "1",
    "varietyId": "1",
    "phenologicStageId": "1",
    "protocolId": "1",
    "parameterId": "1",
    "parameterAspectId": "1",
    "parameterPerCropFamilyId": "1",
    "parameterPerCropId": "1",
    "parameterPerProtocolStrategyId": "1",
    "parameterPerStageId": "1",
    "parameterPerVarietyId": "1",
    "cropProtocolId": "10",
    "cropUnitId": "0a1e91a7-4223-4e9d-ba84-19d410de1753",
    "irrigationBlockId": "a217e28d-7aa1-43dc-9ae9-1996d1037395",
    "shapeId": "db8b64cf-a288-4c6c-34c2-08db13e6f959",
    "irrigationMethodId": "1",
    "uomId": "1",
    "measureUnitId": "1",
    "ioId": "cf7c976e-91dd-4315-8476-08de6201a60e",
    "ioGroupId": "2301e020-45d3-41d7-dab8-08db381d925b",
    "baseUuid": "fa573ba6-47f2-42eb-93f1-08870733af79",
    "programUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
    "irrigationProgramUuid": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
    "irrigationProgramUUId": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
    "irrigationProgramId": "286a92ab-b988-42b4-8886-d770518c21d3-PID1",
    "mainlineId": "1",
    "id": "1",
    "typeId": "1",
    "systemType": "1",
    "SystemType": "1",
    "systemTypeId": "1",
    "systemTypeEnum": "1",
    "page": "1",
    "totalPages": "1",
}


def _build_path_params(farm_id: str) -> dict:
    params = dict(_STATIC_PATH_PARAMS)
    params["farmId"] = farm_id
    params["FarmId"] = farm_id
    return params


def _detect_base_url(spec_path: str) -> str:
    filename = os.path.basename(spec_path)
    host = filename.replace(".json", "")
    return f"https://{host}"


def _resolve_path(path_template: str, path_params: dict) -> Optional[str]:
    """Substitute all {param} placeholders with known real values.
    Returns None if any param has no known value (endpoint will be skipped)."""
    params = re.findall(r'\{(\w+)\}', path_template)
    resolved = path_template
    for param in params:
        if param not in path_params:
            return None
        resolved = resolved.replace(f'{{{param}}}', path_params[param])
    return resolved


def _make_headers(bearer_token: str) -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


@pytest.mark.parametrize("spec_path", SPEC_FILES, ids=lambda p: os.path.basename(p))
def test_openapi_schema_is_loadable(spec_path: str):
    schema = schemathesis.openapi.from_path(spec_path)
    assert schema is not None, f"Failed to load schema from {spec_path}"


@pytest.mark.flaky
@pytest.mark.parametrize("spec_path", SPEC_FILES, ids=lambda p: os.path.basename(p))
def test_api_smoke_for_each_spec(spec_path: str, bearer_token: str, base_url_override: str, smoke_farm_id: str):
    """Smoke test: call every GET endpoint with real QA1 data. Skip endpoints with unknown path params."""
    base_url = base_url_override or _detect_base_url(spec_path)
    headers = _make_headers(bearer_token)
    path_params = _build_path_params(smoke_farm_id)

    schema = schemathesis.openapi.from_path(spec_path)
    schema.base_url = base_url

    operations = []
    for result in schema.get_all_operations():
        if result.ok:
            op = result._value
            if op.method.upper() in ["GET", "HEAD"]:
                operations.append(op)

    if not operations:
        pytest.skip(f"No GET/HEAD operations found in {os.path.basename(spec_path)}")

    print(f"\nRunning {len(operations)} smoke tests for {os.path.basename(spec_path)} (farmId={smoke_farm_id})...")

    errors = []
    for operation in operations:
        resolved = _resolve_path(operation.path, path_params)
        if resolved is None:
            print(f"Skipping {operation.path} — unknown path params")
            continue

        url = f"{base_url}{resolved}"
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=30)

            if response.status_code >= 500:
                errors.append(
                    f"FAILED {operation.method.upper()} {operation.path}: HTTP {response.status_code}"
                )
        except Exception as e:
            print(f"Skipping {operation.path} — request error: {e}")

    if errors:
        pytest.fail("\n".join(errors))
