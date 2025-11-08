import logging
from typing import List
from .constants import KEY_THEMES

logger = logging.getLogger(__name__)


class ThemeCategorizationPrompt:
    """Handles the creation and management of prompts for theme categorization."""
    
    def __init__(self, themes: List[str] = None):
        """
        Initialize the prompt engineer.
        
        Args:
            themes: List of themes to use. If None, uses default KEY_THEMES.
        """
        self.themes = themes or KEY_THEMES
        logger.info(f"Initialized prompt engineer with {len(self.themes)} themes")
    
    def create_prompt(self, patient_review: str) -> str:
        """
        Create a prompt-wrapped review for key theme extraction.
        
        This wraps the patient review with a structured prompt that instructs
        the LLM to identify key themes from the predefined list.
        
        Args:
            patient_review: The patient review text to analyze.
            
        Returns:
            str: The formatted prompt for the LLM.
        """
        themes_list = ', '.join(self.themes)
        
        prompt = (
            "You are analyzing a patient review to identify key themes or areas discussed in the text. "
            "Key themes are specific topics, concerns, or aspects of the healthcare experience that the patient "
            "mentions or talks about in their review.\n\n"
            "Analyze the following patient review and identify all key themes from this list: " +
            f"{themes_list}.\n\n" +
            "Instructions:\n" +
            "- Identify themes that represent topics, concerns, or areas explicitly mentioned or discussed in the review\n" +
            "- A single review may contain multiple themes\n" +
            "- Match themes based on the content and context of what the patient is describing\n" +
            "- If no theme from the list matches the content, use 'unknown'\n" +
            "- For each identified theme, provide a brief description explaining why this theme applies\n\n" +
            f"Patient Review:\n{patient_review}\n\n" +
            "Respond with a JSON object containing a list of identified themes in the format below:\n" +
            "{\n" +
            "  \"themes\": [\n" +
            "    {\n" +
            "      \"theme\": \"\",\n" +
            "      \"description\": \"\"\n" +
            "    }\n" +
            "  ]\n" +
            "}"
        )
        
        return prompt
    
    def get_themes(self) -> List[str]:
        """
        Get the list of available themes.
        
        Returns:
            List of theme names
        """
        return self.themes.copy()
