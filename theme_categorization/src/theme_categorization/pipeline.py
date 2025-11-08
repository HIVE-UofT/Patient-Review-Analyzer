import logging
import time
from typing import List, Dict, Any, Optional
from tqdm import tqdm

from .llm_clients import LLMClient
from .prompt_engineer import ThemeCategorizationPrompt
from .settings import Settings

logger = logging.getLogger(__name__)


class ThemeCategorizationPipeline:
    """
    Main pipeline for processing reviews and categorizing themes.
    
    Flow: Patient Reviews → Prompt Wrapped Review → Key Theme Extraction
    """
    
    def __init__(
        self, 
        llm_client: LLMClient, 
        prompt_engineer: ThemeCategorizationPrompt,
        settings: Optional[Settings] = None
    ):
        """
        Initialize the pipeline.
        
        Args:
            llm_client: LLM client instance
            prompt_engineer: Prompt engineer instance
            settings: Optional settings instance (for rate limiting)
        """
        self.llm_client = llm_client
        self.prompt_engineer = prompt_engineer
        self.settings = settings or Settings()
        
        self.metrics = {
            "total_reviews": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_themes_extracted": 0,
        }
        
        logger.info("Initialized ThemeCategorizationPipeline")
    
    def process_review(self, review: str) -> Dict[str, Any]:
        """
        Process a single review through the pipeline.
        
        Steps:
        1. Wrap review with prompt
        2. Extract key themes using LLM
        
        Args:
            review: The review text to process
            
        Returns:
            Dict containing the extracted themes in format: {"themes": [{"theme": str, "description": str}]}
        """
        self.metrics["total_reviews"] += 1
        
        try:
            prompt = self.prompt_engineer.create_prompt(review)
            logger.debug(f"Created prompt for review (length: {len(review)} chars)")
            
            result = self.llm_client.extract_themes(prompt)

            if result.get("themes"):
                self.metrics["successful_extractions"] += 1
                self.metrics["total_themes_extracted"] += len(result["themes"])
            else:
                self.metrics["failed_extractions"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing review: {e}", exc_info=True)
            self.metrics["failed_extractions"] += 1
            return {"themes": []}
    
    def process_batch(
        self, 
        reviews: List[str], 
        show_progress: bool = True,
        rate_limit: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Process a batch of reviews.
        
        Args:
            reviews: List of review texts to process
            show_progress: Whether to show progress bar
            rate_limit: Whether to apply rate limiting between requests
            
        Returns:
            List of dicts containing extracted themes
        """
        logger.info(f"Processing batch of {len(reviews)} reviews")
        
        results = []
        iterator = tqdm(reviews, desc="Processing reviews") if show_progress else reviews
        
        for review in iterator:
            result = self.process_review(review)
            results.append(result)
            
            if rate_limit and self.settings.rate_limit_delay > 0:
                time.sleep(self.settings.rate_limit_delay)
        
        logger.info(f"Completed batch processing. Success rate: "
                   f"{self.metrics['successful_extractions']}/{self.metrics['total_reviews']}")
        
        return results
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current pipeline metrics.
        
        Returns:
            Dict containing metrics
        """
        success_rate = (
            self.metrics["successful_extractions"] / self.metrics["total_reviews"]
            if self.metrics["total_reviews"] > 0
            else 0.0
        )
        
        avg_themes_per_review = (
            self.metrics["total_themes_extracted"] / self.metrics["successful_extractions"]
            if self.metrics["successful_extractions"] > 0
            else 0.0
        )
        
        return {
            **self.metrics,
            "success_rate": success_rate,
            "avg_themes_per_review": avg_themes_per_review,
        }
    
    def reset_metrics(self):
        """Reset pipeline metrics."""
        self.metrics = {
            "total_reviews": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "total_themes_extracted": 0,
        }
        logger.info("Metrics reset")
