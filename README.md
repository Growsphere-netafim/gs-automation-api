# gs-automation-api

This project focuses on automation tests for the GrowSphere API services.
The tests are designed using the **pytest** framework to validate API functionality across multiple services including crop management, irrigation, field I/O, device state, and more.

---

## Getting Started (MacOS Environment)

### Prerequisites

- Python 3.9+

---

## Installation

**1. Clone the repository.**

```bash
git clone https://netafimdf.visualstudio.com/NetbeatVx/_git/gs-automation-api
cd gs-automation-api
```

**2. Create and activate a virtual environment.**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install project dependencies.**

```bash
pip install -r requirements.txt
```

**4. Set up the environment configuration.**

Copy `.env.example` to `.env` and fill in the required values.
You can get all secrets from the Azure DevOps pipeline library.

```bash
cp .env.example .env
```

Key variables to configure:

| Variable | Description |
|---|---|
| `ENV_NAME` | Target environment (`qa1`) |
| `USER_EMAIL` | Test user email |
| `PASSWORD` | Test user password |
| `OIDC_CLIENT_ID` | OAuth2 client ID |
| `IDS_URL` | Identity Server URL |

---

## Usage

Run tests using the `run_tests.py` script with your venv Python:

### Run integration tests

```bash
.venv/bin/python run_tests.py --integration
```

### Run mock tests

```bash
.venv/bin/python run_tests.py --mock
```

### Run all tests

```bash
.venv/bin/python run_tests.py --all
```

### Run a specific test file

```bash
.venv/bin/python run_tests.py tests/integration/test_cropservice_get_api.py
```

### Run in parallel

```bash
.venv/bin/python run_tests.py --all --parallel
```

---

## Reporting

### Allure report

```bash
.venv/bin/python run_tests.py --all --allure
# Results saved to: ./reports/allure-results/
```

---

## Troubleshooting

**Problem: `ModuleNotFoundError: No module named 'config'`**

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
