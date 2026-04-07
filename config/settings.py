"""
Centralized configuration using environment variables
Uses pydantic for validation and type safety
"""
import os
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Provides validation and type safety
    """
    
    # ============= Environment =============
    ENV_NAME: Literal["prod", "test", "local", "qa1", "stag"] = Field(default="test")
    
    # ============= Authentication =============
    USER_EMAIL: str = Field(default="test@example.com")
    PASSWORD: str = Field(default="")
    # Comma-separated fallback users for CI (tried in order if primary fails)
    USER_EMAIL_POOL: str = Field(default="")
    
    # OAuth2 Configuration
    OIDC_CLIENT_ID: str = Field(default="")
    OIDC_REDIRECT_URI: str = Field(default="")
    SCOPES_VAL: str = Field(default="openid profile email offline_access")
    
    # ============= API URLs =============
    # Production
    PROD_USER_PORTAL_URL: str = Field(default="")
    PROD_CSAPI_URL: str = Field(default="")
    PROD_FIELDIO_URL: str = Field(default="")
    PROD_IRRIGATION_URL: str = Field(default="")
    
    # Test/QA
    TEST_USER_PORTAL_URL: str = Field(default="")
    TEST_CSAPI_URL: str = Field(default="")
    TEST_FIELDIO_URL: str = Field(default="")
    TEST_IRRIGATION_URL: str = Field(default="")
    
    # Local
    LOCAL_URL: str = Field(default="http://localhost:3000")
    
    # Common URLs
    IDS_URL: str = Field(default="")
    ACCOUNT_MANAGEMENT_URL: str = Field(default="")
    
    # ============= IoT Hub (Mainlines) =============
    IOT_HUB_HOST: str = Field(default="")
    POLICY_NAME: str = Field(default="service")
    POLICY_KEY: str = Field(default="")
    
    # ============= Swagger/OpenAPI =============
    SWAGGER_URL: Optional[str] = Field(default=None)
    SWAGGER_FILE_PATH: Optional[str] = Field(default=None)
    
    # ============= Test Configuration =============
    REQUEST_TIMEOUT: int = Field(default=45)
    AUTH_TIMEOUT: int = Field(default=60)
    MAX_RETRIES: int = Field(default=3)
    RETRY_DELAY: int = Field(default=1)
    
    # Test data prefixes
    TEST_FARM_PREFIX: str = Field(default="TEST_FARM_")
    TEST_USER_PREFIX: str = Field(default="TEST_USER_")
    
    # ============= Mock Configuration =============
    USE_MOCKS: bool = Field(default=False)
    MOCK_DELAY: float = Field(default=0.1)
    
    # ============= Reporting =============
    ALLURE_RESULTS_DIR: str = Field(default="./reports/allure-results")
    HTML_REPORT_DIR: str = Field(default="./reports/html")
    
    # ============= Logging =============
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    LOG_FILE: str = Field(default="./logs/test_run.log")
    
    # ============= CI/CD =============
    CI: bool = Field(default=False)
    PARALLEL_WORKERS: int = Field(default=4)
    
    # ============= Feature Flags =============
    RUN_SMOKE_TESTS: bool = Field(default=True)
    RUN_INTEGRATION_TESTS: bool = Field(default=True)
    RUN_LOAD_TESTS: bool = Field(default=False)
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Allow extra fields like DEBUG without failing
    )
    
    # ============= Computed Properties =============
    
    @property
    def base_urls(self) -> dict:
        """Get base URLs based on current environment"""
        if self.ENV_NAME == "prod":
            return {
                "user_portal": self.PROD_USER_PORTAL_URL,
                "csapi_url": self.PROD_CSAPI_URL,
                "fieldio_url": self.PROD_FIELDIO_URL,
                "irrigation": self.PROD_IRRIGATION_URL,
                "ids_url": self.IDS_URL,
                "account_management": self.ACCOUNT_MANAGEMENT_URL,
            }
        elif self.ENV_NAME == "test":
            return {
                "user_portal": self.TEST_USER_PORTAL_URL,
                "csapi_url": self.TEST_CSAPI_URL,
                "fieldio_url": self.TEST_FIELDIO_URL,
                "irrigation": self.TEST_IRRIGATION_URL,
                "ids_url": self.IDS_URL,
                "account_management": self.ACCOUNT_MANAGEMENT_URL,
            }
        else:  # local
            return {
                "user_portal": self.LOCAL_URL,
                "csapi_url": self.LOCAL_URL,
                "fieldio_url": self.LOCAL_URL,
                "irrigation": self.LOCAL_URL,
                "ids_url": self.IDS_URL,
                "account_management": self.ACCOUNT_MANAGEMENT_URL,
            }
    
    @property
    def swagger_source(self) -> str:
        """Get Swagger source (URL or file path)"""
        if self.SWAGGER_URL:
            return self.SWAGGER_URL
        elif self.SWAGGER_FILE_PATH:
            return self.SWAGGER_FILE_PATH
        else:
            # Default to test environment swagger
            return f"{self.TEST_CSAPI_URL}/swagger/v1/swagger.json"
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENV_NAME == "prod"
    
    def should_cleanup(self) -> bool:
        """Determine if test data should be cleaned up"""
        # In production, always cleanup
        # In test, cleanup unless debugging
        return self.is_production() or not os.getenv("DEBUG", "").lower() == "true"


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get singleton Settings instance
    Ensures only one Settings object exists
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Convenience function
def reload_settings() -> Settings:
    """
    Reload settings from environment
    Useful for testing or runtime configuration changes
    """
    global _settings
    _settings = None
    load_dotenv(override=True)
    return get_settings()
