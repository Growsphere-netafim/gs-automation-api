import allure
import pytest


@allure.epic("CS API")
@allure.feature("SignUpInvitations")
class TestSignUpInvitations:

    @pytest.mark.flaky
    @allure.story("Get Sign Up Invitation")
    def test_get_signup_invitation(self, csapi_service):
        csapi_service.get_signup_invitation().assert_ok()

    @pytest.mark.flaky
    @allure.story("Validate Sign Up Token (Anonymous)")
    def test_validate_signup_token(self, csapi_service):
        csapi_service.validate_signup_token().assert_ok()
