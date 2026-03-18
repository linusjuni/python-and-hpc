from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # General settings
    RANDOM_SEED: int = Field(default=69)

    # Paths
    DATA_DIR: Path = Path("/dtu/projects/02613_2025/data/modified_swiss_dwellings")
    RESULTS_DIR: Path = Path("results")


settings = Settings()