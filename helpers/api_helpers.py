import allure
import json
from requests import Response


def assert_status_code(response: Response, expected_status: int = 200):
    """
    Standard assertion with rich failure message for Allure.
    If the assertion fails, attaches a diagnosis note with the expected vs actual status.
    The full failure diagnosis is automatically attached by log_response (session hook).
    """
    actual_status = response.status_code
    if actual_status != expected_status:
        # Build a clear summary for the assertion error message
        error_msg = f"Expected HTTP {expected_status} but got {actual_status}."

        # Extract server-provided error details
        try:
            body = response.json()
            error_details = (
                body.get("error") or
                body.get("message") or
                body.get("Message") or
                body.get("errorMessage") or
                body.get("title") or
                body.get("detail")
            )

            if not error_details and "errors" in body:
                error_details = json.dumps(body["errors"])

            if error_details:
                error_msg += f"  Server says: {error_details}"
        except Exception:
            if response.text:
                error_msg += f"  Body snippet: {response.text[:300]}"

        # Attach a concise assertion note to Allure (full diagnosis already in log_response)
        allure.attach(
            error_msg,
            name=f"[ASSERT FAILED] Expected {expected_status}, got {actual_status}",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual_status == expected_status, error_msg


def validate_response_list(response: Response):
    """
    Assert that the response body is a non-empty list.
    If the list is empty, attaches an empty-response warning to Allure.
    """
    from helpers.allure_helpers import attach_empty_response_warning

    data = response.json()
    assert isinstance(data, list), (
        f"Expected list but got {type(data).__name__}. Body: {response.text[:200]}"
    )

    if len(data) == 0:
        attach_empty_response_warning(
            response,
            context_hint="validate_response_list: list was empty. Try a different farmId or device."
        )

    return data
