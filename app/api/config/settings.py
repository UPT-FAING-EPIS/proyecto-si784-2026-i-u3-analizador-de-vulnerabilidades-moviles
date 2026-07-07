import os

from dotenv import load_dotenv

load_dotenv()


class ApiSettings:
    app_name = "AnzenCore API"
    api_prefix = "/api/v1"
    supabase_url = os.getenv("SUPABASE_URL", "")
    supabase_key = os.getenv("SUPABASE_KEY", "")
    cors_origins = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "*").split(",")
        if origin.strip()
    ]
    anzen_external_url = os.getenv(
        "ANZEN_EXTERNAL_URL", "https://anestatico.onrender.com/api/analysis/external/github"
    )
