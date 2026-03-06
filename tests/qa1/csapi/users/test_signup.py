import allure
import pytest


@allure.epic("CS API")
@allure.feature("SignUpInvitations")
class TestSignUpInvitations:

    @pytest.mark.flaky
    # TODO: invitationId is ephemeral — requires a pending signup invitation in QA1.
    # To fix: trigger a signup invitation and capture the ID before running this test.
    @allure.story("Get Sign Up Invitation")
    def test_get_signup_invitation(self, csapi_service):
        csapi_service.get_signup_invitation().assert_ok()

    @pytest.mark.flaky
    # TODO: signupToken is ephemeral — requires a valid signup token from a QA1 invitation.
    # To fix: trigger a signup flow and capture the token before running this test.
    @allure.story("Validate Sign Up Token (Anonymous)")
    def test_validate_signup_token(self, csapi_service):
        csapi_service.validate_signup_token().assert_ok()
