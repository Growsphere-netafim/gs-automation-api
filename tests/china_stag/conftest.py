import os
import allure
import pytest
from tests.qa1.conftest import create_service_fixtures


@pytest.fixture(autouse=True)
def set_allure_suites(request):
    try:
        path = str(request.node.fspath)
    except Exception:
        path = ""
    parts = path.split("/tests/china_stag/")[-1].split("/") if "/tests/china_stag/" in path else []
    suite = parts[0] if parts and parts[0] else "china_stag"
    filename = os.path.basename(path) if path else ""
    name_no_ext = os.path.splitext(filename)[0] if filename else ""
    sub = parts[1] if len(parts) > 1 else name_no_ext
    allure.dynamic.parent_suite("CHINA STAG")
    allure.dynamic.suite(suite)
    if sub:
        allure.dynamic.sub_suite(sub)
