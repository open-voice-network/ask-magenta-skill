from pydantic import BaseSettings


class Settings(BaseSettings):
    """Magenta Voice Platform client settings"""

    # OAuth2 connect:
    oauth_token_url: str = "https://get-us/tokens"
    oauth_client_id: str = "client-id"
    oauth_scope: str = "scope"

    tenant: str = "tenant"
    api_key: str = "api-key"

    testing_secret: str = "testing-secret"

    base_url: str = "https://get-us/api"
    user_api: str = "/user"
    invoke_text: str = "/text"

    class Config:
        env_file = ".env"


settings = Settings()
