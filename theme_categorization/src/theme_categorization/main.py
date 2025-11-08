"""
Main script demonstrating the usage of the theme categorization package.
"""
import os
import logging
from typing import Dict, Any

from .data_loader import DataLoader
from .prompt_engineer import ThemeCategorizationPrompt
from .llm_clients import HuggingFaceClient
from .pipeline import ThemeCategorizationPipeline
from .settings import Settings

logger = logging.getLogger(__name__)


def setup_environment():
    """Set up environment variables for configuration."""
    logger.info("Setting up environment...")


def main():
    """Main function demonstrating the usage of the theme categorization package."""
    # Set up environment
    setup_environment()
    
    # Initialize settings
    settings = Settings()
    logger.info(f"Using base URL: {settings.base_url}")
    logger.info(f"Using model: {settings.hf_model_name}")
    
    # Initialize components
    try:
        data_loader = DataLoader("patient_reviews.csv")
        prompt_engineer = ThemeCategorizationPrompt()

        llm_client = HuggingFaceClient(settings)
        
        pipeline = ThemeCategorizationPipeline(llm_client, prompt_engineer, settings)
        
        reviews = data_loader.get_reviews(limit=5) 
        
        logger.info(f"Processing {len(reviews)} reviews...")
        results = pipeline.process_batch(reviews)

        for i, (review, result) in enumerate(zip(reviews, results)):
            print(f"\n{'='*60}")
            print(f"Review {i+1}:")
            print(f"{'='*60}")
            print(f"Review text: {review[:200]}...")
            print(f"\nExtracted themes ({len(result.get('themes', []))}):")
            for theme in result.get('themes', []):
                print(f"  - {theme.get('theme', 'unknown')}: {theme.get('description', '')}")
        
        # Display metrics
        metrics = pipeline.get_metrics()
        print(f"\n{'='*60}")
        print("Pipeline Metrics:")
        print(f"{'='*60}")
        print(f"Total reviews processed: {metrics['total_reviews']}")
        print(f"Successful extractions: {metrics['successful_extractions']}")
        print(f"Failed extractions: {metrics['failed_extractions']}")
        print(f"Success rate: {metrics['success_rate']:.2%}")
        print(f"Total themes extracted: {metrics['total_themes_extracted']}")
        print(f"Average themes per review: {metrics['avg_themes_per_review']:.2f}")
        
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        print("Please ensure 'patient_reviews.csv' exists in the current directory.")
    except Exception as e:
        logger.error(f"Error processing reviews: {e}", exc_info=True)
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
