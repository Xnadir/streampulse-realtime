"""
Configuration management for StreamPulse.
Loads settings from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    STREAM_INTERVAL: float = float(os.getenv("STREAM_INTERVAL", "2.0"))
    MAX_CLIENTS: int = int(os.getenv("MAX_CLIENTS", "50"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
