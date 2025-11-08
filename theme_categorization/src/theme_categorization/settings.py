"""
Settings and configuration management for theme categorization.
Automatically loads environment variables from .env file if present.
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    import logging
    logger = logging.getLogger(__name__)
    
    # Load .env file from project root (parent of src directory)
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        # Also try current directory
        if load_dotenv():
            logger.info("Loaded environment variables from .env file in current directory")
except ImportError:
    # python-dotenv not installed, skip .env loading
    pass


@dataclass
class Settings:
    """Configuration settings for theme categorization system."""
    
    # HuggingFace Configuration
    hf_token: str = os.getenv("HF_TOKEN", "dummy_token")
    hf_model_name: str = os.getenv("HF_MODEL_NAME", "meta-llama/Llama-3.2-3B-Instruct")
    hf_timeout: int = int(os.getenv("HF_TIMEOUT", "120"))  # Increased default to 60s for HuggingFace Router
    
    # vLLM Configuration (local deployment)
    vllm_base_url: str = os.getenv("VLLM_BASE_URL", "http://localhost:8001/v1")
    
    # HuggingFace Inference Router Configuration
    hf_router_url: str = os.getenv("HF_ROUTER_URL", "https://router.huggingface.co/v1")
    
    # LLM Parameters
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))
    
    # Rate Limiting
    rate_limit_delay: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def base_url(self) -> str:
        """Determine base URL based on token configuration."""
        if self.hf_token == "dummy_token":
            return self.vllm_base_url
        return self.hf_router_url
    
    @property
    def api_key(self) -> str:
        """Get API key based on configuration."""
        if self.hf_token == "dummy_token":
            return "EMPTY"
        return self.hf_token
    
    def __post_init__(self):
        """Validate settings after initialization."""
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature must be between 0 and 2")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if self.hf_timeout < 1:
            raise ValueError("hf_timeout must be at least 1 second")

