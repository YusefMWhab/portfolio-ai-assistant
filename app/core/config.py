from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    GEMINI_MODEL_TTS: str = "gemini-2.5-flash-preview-tts"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-2"

    class Config:
        env_file = ".env"


settings = Settings()