import ast
import logging
from typing import Dict, Any, List, Set, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def parse_ground_truth(processed_code: str) -> Set[str]:
    """
    Parse ground truth themes from ProcessedCode column.
    
    Args:
        processed_code: String like "{'theme1', 'theme2'}" or NaN
        
    Returns:
        Set of theme names (empty set if NaN or invalid)
    """
    if pd.isna(processed_code) or processed_code == '':
        return set()
    
    try:
        themes_set = ast.literal_eval(processed_code)
        if isinstance(themes_set, set):
            return themes_set
        elif isinstance(themes_set, (list, tuple)):
            return set(themes_set)
        else:
            return set()
    except (ValueError, SyntaxError) as e:
        logger.warning(f"Failed to parse ground truth: {processed_code}, error: {e}")
        return set()


def parse_llm_themes(llm_result: Dict[str, Any]) -> Set[str]:
    """
    Extract theme names from LLM result.
    
    Args:
        llm_result: Dict with format {"themes": [{"theme": str, "description": str}]}
        
    Returns:
        Set of theme names
    """
    themes = set()
    if isinstance(llm_result, dict) and "themes" in llm_result:
        for theme_obj in llm_result["themes"]:
            if isinstance(theme_obj, dict) and "theme" in theme_obj:
                theme_name = theme_obj["theme"].strip()
                if theme_name and theme_name.lower() != "unknown":
                    themes.add(theme_name)
    return themes


def calculate_metrics(
    ground_truth_themes: Set[str],
    predicted_themes: Set[str]
) -> Dict[str, float]:
    """
    Calculate evaluation metrics for a single review.
    
    Args:
        ground_truth_themes: Set of ground truth theme names
        predicted_themes: Set of predicted theme names
        
    Returns:
        Dict with metrics: identified_count, novel_count, total_ground_truth, total_predicted
    """
    identified = ground_truth_themes & predicted_themes
    
    novel = predicted_themes - ground_truth_themes
    
    return {
        "identified_count": len(identified),
        "novel_count": len(novel),
        "total_ground_truth": len(ground_truth_themes),
        "total_predicted": len(predicted_themes),
        "identified_themes": identified,
        "novel_themes": novel,
        "missed_themes": ground_truth_themes - predicted_themes,
    }


def evaluate_predictions(
    ground_truth_list: List[Set[str]],
    predicted_list: List[Set[str]]
) -> Dict[str, Any]:
    """
    Calculate aggregate evaluation metrics across all reviews.
    
    Args:
        ground_truth_list: List of ground truth theme sets
        predicted_list: List of predicted theme sets
        
    Returns:
        Dict with aggregate metrics including:
        - theme_identification_rate: % of ground truth themes identified
        - novel_themes_percentage: % of predicted themes that are novel
        - average_themes_per_review: Average number of themes per review
    """
    if len(ground_truth_list) != len(predicted_list):
        raise ValueError("Ground truth and predictions must have same length")
    
    total_ground_truth_themes = 0
    total_predicted_themes = 0
    total_identified = 0
    total_novel = 0
    
    for gt_themes, pred_themes in zip(ground_truth_list, predicted_list):
        metrics = calculate_metrics(gt_themes, pred_themes)
        total_ground_truth_themes += metrics["total_ground_truth"]
        total_predicted_themes += metrics["total_predicted"]
        total_identified += metrics["identified_count"]
        total_novel += metrics["novel_count"]
    
    theme_identification_rate = (
        total_identified / total_ground_truth_themes * 100
        if total_ground_truth_themes > 0
        else 0.0
    )
    
    novel_themes_percentage = (
        total_novel / total_predicted_themes * 100
        if total_predicted_themes > 0
        else 0.0
    )
    
    avg_themes_per_review = (
        total_predicted_themes / len(predicted_list)
        if len(predicted_list) > 0
        else 0.0
    )
    
    return {
        "theme_identification_rate": theme_identification_rate,
        "novel_themes_percentage": novel_themes_percentage,
        "total_reviews": len(ground_truth_list),
        "total_ground_truth_themes": total_ground_truth_themes,
        "total_predicted_themes": total_predicted_themes,
        "total_identified": total_identified,
        "total_novel": total_novel,
        "average_themes_per_review": avg_themes_per_review,
    }

