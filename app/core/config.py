# app/core/config.py

import os
import secrets
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # ===============================
    # DATABASE
    # ===============================
    DATABASE_URL: str
    DATABASE_SYNC_URL: str

    # ===============================
    # SECURITY
    # ===============================
    SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    MFA_TEMP_EXPIRE_MINUTES: int = 5
    SUPER_ADMIN_SECRET: str

    # ===============================
    # AWS CONFIG
    # ===============================
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str | None = None
    AWS_S3_BUCKET: str | None = None

    # ===============================
    # EMAIL (SES)
    # ===============================
    EMAIL_PROVIDER: str | None = None

    SES_HOST: str | None = None
    SES_PORT: int | None = None
    SES_USER: str | None = None
    SES_PASS: str | None = None

    EMAIL_FROM: str | None = None
    EMAIL_FROM_NAME: str | None = None
    BASE_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()


# =====================================================
# AUTO-GENERATE SECRET_KEY IF BLANK OR NULL
# =====================================================
if settings.SECRET_KEY is None or settings.SECRET_KEY.strip() == "":
    new_key = secrets.token_hex(32)

    settings.SECRET_KEY = new_key

    env_path = ".env"

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

        with open(env_path, "w") as f:
            wrote_key = False
            for line in lines:
                if line.startswith("SECRET_KEY"):
                    f.write(f"SECRET_KEY={new_key}\n")
                    wrote_key = True
                else:
                    f.write(line)

            if not wrote_key:
                f.write(f"\nSECRET_KEY={new_key}\n")
    else:
        with open(env_path, "w") as f:
            f.write(f"SECRET_KEY={new_key}\n")

    print("Generated new SECRET_KEY:", new_key)
else:
    print("Loaded SECRET_KEY from .env")


# Debug prints
print("AWS KEY:", settings.AWS_ACCESS_KEY_ID)
print("EMAIL FROM:", settings.EMAIL_FROM)
