import os


class Settings:
    PROJECT_NAME = "Codex"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    VECTOR_DB = os.getenv("VECTOR_DB", "qdrant")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBED_MODEL = os.getenv(
        "OPENAI_EMBED_MODEL", "text-embedding-ada-002"
    )
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "assets")
    
    # MongoDB settings
    USE_MONGODB = os.getenv("USE_MONGODB", "false").lower() == "true"
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "daleel_bot")


def get_settings() -> Settings:
    return Settings()
