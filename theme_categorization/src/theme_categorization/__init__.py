import logging

from .settings import Settings
from .llm_clients import HuggingFaceClient, LLMClient
from .prompt_engineer import ThemeCategorizationPrompt
from .pipeline import ThemeCategorizationPipeline
from .constants import KEY_THEMES
from .data_loader import DataLoader
from .evaluator import (
    parse_ground_truth,
    parse_llm_themes,
    evaluate_predictions,
    calculate_metrics,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__version__ = "0.1.0"

__all__ = [
    "Settings",
    "HuggingFaceClient",
    "LLMClient",
    "ThemeCategorizationPrompt",
    "ThemeCategorizationPipeline",
    "DataLoader",
    "KEY_THEMES",
    "parse_ground_truth",
    "parse_llm_themes",
    "evaluate_predictions",
    "calculate_metrics",
]
