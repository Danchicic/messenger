import os
from pathlib import Path

from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseModel):
    """
    base config for jwt information
    """
    public_key_path: str
    private_key_path: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    token_type_field: str


class Config(BaseModel):
    verification_code_time_expiration: int
    project_host: str
    jwt: AuthJWT

    @field_validator("project_host")
    def validate_host(cls, value):
        if value.endswith("/"):
            raise Exception("Config: project_host should be without /")
        return value


def load_config() -> Config:
    """
    return config in modules that requires settings
    :return: config with all parameters
    """
    return Config(
        verification_code_time_expiration=60 * 5,
        project_host="http://localhost:8000",
        jwt=AuthJWT(
            public_key_path=Path(os.path.join(BASE_DIR.parent, "certs", "jwt-public.pem")).read_text(),
            private_key_path=Path(os.path.join(BASE_DIR.parent, "certs", "jwt-private.pem")).read_text(),
            algorithm="RS256",
            access_token_expire_minutes=5,
            refresh_token_expire_days=10,
            token_type_field="token_type"
        ),
    )
