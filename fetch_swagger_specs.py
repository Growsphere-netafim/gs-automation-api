import asyncio
import json
import os
import re
from dataclasses import dataclass
from typing import Optional, List, Tuple

import aiohttp


# All 19 QA1 services (healthy per platform status page). Each URL points
# directly at the service's swagger.json so per-service path versions can be
# pinned (e.g. TimeSeries API is v2, everything else v1).
URLS = [
    "https://cropservice-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://lookup-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://dataapi-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://fieldio-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://weatherforecast-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://csapi-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://reportapi-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://irrigation-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://settingsapi-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://app-netbeatvx-signalr-qa1.azurewebsites.net/swagger/v1/swagger.json",
    "https://commandsmanager-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://devicestatemanager-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://irrigationmanager-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://timeseriesapi-qa1.k8s.growsphere.netafim.com/swagger/v2/swagger.json",
    "https://qa1-netbeatvx-graphapi-app-weu.azurewebsites.net/swagger/v1/swagger.json",
    "https://mobilebff-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://accountmanagement-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://apigateway-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
    "https://remotesensing-qa1.k8s.growsphere.netafim.com/swagger/v1/swagger.json",
]


OUTPUT_DIR = "swagger_specs"
TIMEOUT_SECONDS = 20
CONCURRENCY = 8


@dataclass
class FetchResult:
    url: str
    ok: bool
    status: Optional[int]
    filename: Optional[str]
    error: Optional[str]


def safe_filename_from_url(url: str) -> str:
    # Example: https://service-qa1.../swagger/v1/swagger.json -> service-qa1.k8s.growsphere.netafim.com.json
    host = re.sub(r"^https?://", "", url).split("/")[0]
    return f"{host}.json"


async def fetch_one(session: aiohttp.ClientSession, sem: asyncio.Semaphore, url: str) -> FetchResult:
    async with sem:
        try:
            async with session.get(url, ssl=False) as resp:
                status = resp.status
                text = await resp.text()

                if status != 200:
                    return FetchResult(url=url, ok=False, status=status, filename=None, error=f"HTTP {status}")

                try:
                    data = json.loads(text)
                except json.JSONDecodeError as e:
                    return FetchResult(url=url, ok=False, status=status, filename=None, error=f"Invalid JSON: {e}")

                filename = safe_filename_from_url(url)
                filepath = os.path.join(OUTPUT_DIR, filename)

                # Save pretty JSON for easy diffs
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                return FetchResult(url=url, ok=True, status=status, filename=filepath, error=None)

        except asyncio.TimeoutError:
            return FetchResult(url=url, ok=False, status=None, filename=None, error="Timeout")
        except aiohttp.ClientError as e:
            return FetchResult(url=url, ok=False, status=None, filename=None, error=f"ClientError: {e}")
        except Exception as e:
            return FetchResult(url=url, ok=False, status=None, filename=None, error=f"Unexpected: {e}")


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    sem = asyncio.Semaphore(CONCURRENCY)

    headers = {
        # "Authorization": "Bearer <TOKEN>",  # If needed, uncomment and set token
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = [fetch_one(session, sem, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    ok_results = [r for r in results if r.ok]
    fail_results = [r for r in results if not r.ok]

    print("\n=== RESULTS ===")
    print(f"OK: {len(ok_results)}")
    print(f"FAIL: {len(fail_results)}\n")

    if ok_results:
        print("---- OK ----")
        for r in ok_results:
            print(f"[OK] {r.url} -> {r.filename}")

    if fail_results:
        print("\n---- FAIL ----")
        for r in fail_results:
            status_part = f" (status={r.status})" if r.status is not None else ""
            print(f"[FAIL] {r.url}{status_part} -> {r.error}")


if __name__ == "__main__":
    asyncio.run(main())
