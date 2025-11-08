import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from openai import OpenAI

from .settings import Settings
from .constants import KEY_THEMES

# Try to import connection error types from common libraries
try:
    from requests.exceptions import ConnectionError as RequestsConnectionError
except ImportError:
    RequestsConnectionError = None

try:
    from httpx import ConnectError as HttpxConnectError
except ImportError:
    HttpxConnectError = None

# Import OpenAI exceptions (handle different versions)
try:
    from openai import APIError, APITimeoutError, RateLimitError
except ImportError:
    # Fallback for older versions
    try:
        from openai.error import APIError, TimeoutError as APITimeoutError, RateLimitError
    except ImportError:
        # Generic fallback
        APIError = Exception
        APITimeoutError = TimeoutError
        RateLimitError = Exception

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    
    def __init__(self, settings: Settings):
        """
        Initialize the LLM client.
        
        Args:
            settings: Configuration settings instance
        """
        self.settings = settings
        logger.info(f"Initializing LLM client...")
        logger.info(f"  Base URL: {settings.base_url}")
        logger.info(f"  API Key: {'***SET***' if settings.api_key != 'EMPTY' else 'EMPTY (vLLM mode)'}")
        logger.info(f"  Timeout: {settings.hf_timeout}s")
        
        try:
            self.client = OpenAI(
                base_url=settings.base_url,
                api_key=settings.api_key,
                timeout=settings.hf_timeout,
            )
            logger.info(f"Successfully initialized LLM client")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}", exc_info=True)
            raise
    
    @abstractmethod
    def extract_themes(self, patient_review: str) -> Dict[str, Any]:
        """
        Extract themes from a patient review.
        
        Args:
            patient_review: The patient review text to analyze
            
        Returns:
            Dict containing extracted themes in format: {"themes": [{"theme": str, "description": str}]}
        """
        pass


class HuggingFaceClient(LLMClient):
    """
    HuggingFace client implementation using OpenAI-compatible API.
    Supports both vLLM (local) and HuggingFace Inference Router.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the HuggingFace client.
        
        Args:
            settings: Configuration settings instance
        """
        super().__init__(settings)
        self.model_name = settings.hf_model_name
        logger.info(f"Using model: {self.model_name}")
    
    def extract_themes(self, patient_review: str, retries: int = 3) -> Dict[str, Any]:
        """
        Extract themes from a patient review using HuggingFace API.
        
        Args:
            patient_review: The patient review text to analyze
            retries: Number of retry attempts on failure
            
        Returns:
            Dict containing extracted themes in format: {"themes": [{"theme": str, "description": str}]}
        """
        # Log request details (only on first attempt to reduce verbosity)
        for attempt in range(retries):
            try:
                if attempt == 0:
                    logger.info(f"Extracting themes - Attempt {attempt + 1}/{retries}")
                    logger.debug(f"  Base URL: {self.settings.base_url}")
                    logger.debug(f"  Model: {self.model_name}")
                    logger.debug(f"  Timeout: {self.settings.hf_timeout}s")
                    logger.debug(f"  API Key: {'***SET***' if self.settings.api_key != 'EMPTY' else 'EMPTY (vLLM mode)'}")
                    logger.debug(f"  Prompt length: {len(patient_review)} characters")
                else:
                    logger.info(f"Retry attempt {attempt + 1}/{retries}")
                
                logger.debug(f"Sending request to {self.settings.base_url}")
                logger.debug(f"Request parameters: model={self.model_name}, temperature={self.settings.temperature}, max_tokens={self.settings.max_tokens}")
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": patient_review}],
                    temperature=self.settings.temperature,
                    max_tokens=self.settings.max_tokens,
                )
                
                logger.debug(f"Successfully received response from API")
                content = response.choices[0].message.content
                logger.debug(f"Raw LLM response (first 200 chars): {content[:200]}...")
                
                # Parse JSON response
                result = self._parse_response(content)
                logger.debug(f"Successfully extracted {len(result.get('themes', []))} themes")
                return result
                
            except APITimeoutError as e:
                logger.error(f"TIMEOUT ERROR on attempt {attempt + 1}/{retries}")
                logger.error(f"  Error type: {type(e).__name__}")
                logger.error(f"  Error message: {str(e)}")
                logger.error(f"  Timeout setting: {self.settings.hf_timeout}s")
                logger.error(f"  Base URL: {self.settings.base_url}")
                if hasattr(e, '__cause__') and e.__cause__:
                    logger.error(f"  Underlying error: {e.__cause__}")
                
                # Provide troubleshooting suggestions
                logger.error(f"  TROUBLESHOOTING:")
                if "handshake" in str(e.__cause__).lower() or "ssl" in str(e.__cause__).lower():
                    logger.error(f"    - SSL handshake timeout detected")
                    logger.error(f"    - This may indicate network connectivity issues")
                    logger.error(f"    - Try increasing HF_TIMEOUT in .env file (e.g., HF_TIMEOUT=120)")
                else:
                    logger.error(f"    - Request is taking longer than {self.settings.hf_timeout}s")
                    logger.error(f"    - HuggingFace Router may be slow or overloaded")
                    logger.error(f"    - Try increasing HF_TIMEOUT in .env file (e.g., HF_TIMEOUT=120)")
                    logger.error(f"    - Check your network connection")
                
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retries} attempts due to timeout")
                    logger.error(f"  SUGGESTION: Increase HF_TIMEOUT in your .env file to 120 or higher")
                    return {"themes": []}
                    
            except RateLimitError as e:
                logger.error(f"RATE LIMIT ERROR on attempt {attempt + 1}/{retries}")
                logger.error(f"  Error type: {type(e).__name__}")
                logger.error(f"  Error message: {str(e)}")
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retries} attempts due to rate limit")
                    return {"themes": []}
                    
            except APIError as e:
                logger.error(f"API ERROR on attempt {attempt + 1}/{retries}")
                logger.error(f"  Error type: {type(e).__name__}")
                logger.error(f"  Error message: {str(e)}")
                logger.error(f"  Base URL: {self.settings.base_url}")
                logger.error(f"  Model: {self.model_name}")
                if hasattr(e, 'status_code'):
                    logger.error(f"  HTTP Status: {e.status_code}")
                if hasattr(e, 'response'):
                    logger.error(f"  Response: {e.response}")
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retries} attempts")
                    return {"themes": []}
                    
            except Exception as e:
                # Catch connection errors and other exceptions
                error_type = type(e).__name__
                error_msg = str(e)
                
                # Check if it's a known connection error type
                is_connection_error = False
                if RequestsConnectionError and isinstance(e, RequestsConnectionError):
                    is_connection_error = True
                elif HttpxConnectError and isinstance(e, HttpxConnectError):
                    is_connection_error = True
                elif 'connection' in error_msg.lower() or 'connect' in error_msg.lower():
                    is_connection_error = True
                
                if is_connection_error:
                    logger.error(f"CONNECTION ERROR on attempt {attempt + 1}/{retries}")
                else:
                    logger.error(f"UNEXPECTED ERROR on attempt {attempt + 1}/{retries}")
                
                logger.error(f"  Error type: {error_type}")
                logger.error(f"  Error message: {error_msg}")
                logger.error(f"  Base URL: {self.settings.base_url}")
                logger.error(f"  Model: {self.model_name}")
                logger.error(f"  Full exception details:", exc_info=True)
                
                # Provide troubleshooting info for connection errors
                if is_connection_error:
                    logger.error(f"  TROUBLESHOOTING:")
                    if self.settings.base_url.startswith("http://localhost"):
                        logger.error(f"    - You're using vLLM (local server)")
                        logger.error(f"    - Check if vLLM server is running on {self.settings.base_url}")
                        logger.error(f"    - Start vLLM with: python -m vllm.entrypoints.openai.api_server --model {self.model_name} --port 8001")
                    else:
                        logger.error(f"    - You're using HuggingFace Inference Router")
                        logger.error(f"    - Check if your API token is valid")
                        logger.error(f"    - Check your network connection")
                        logger.error(f"    - Verify the URL is accessible: {self.settings.base_url}")
                
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {retries} attempts")
                    return {"themes": []}
        
        return {"themes": []}
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """
        Parse LLM response content into structured format.
        
        Args:
            content: Raw response content from LLM
            
        Returns:
            Dict with parsed themes
        """
        # Try to extract JSON from response
        content = content.strip()
        
        # Look for JSON object in the response
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            logger.warning("No JSON object found in response")
            return {"themes": []}
        
        json_str = content[start_idx:end_idx]
        
        try:
            parsed = json.loads(json_str)
            
            # Validate structure
            if "themes" not in parsed:
                logger.warning("Response missing 'themes' key")
                return {"themes": []}
            
            # Validate theme format
            validated_themes = []
            for theme in parsed["themes"]:
                if isinstance(theme, dict) and "theme" in theme:
                    validated_themes.append({
                        "theme": theme.get("theme", "unknown"),
                        "description": theme.get("description", "")
                    })
                else:
                    logger.warning(f"Invalid theme format: {theme}")
            
            return {"themes": validated_themes}
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"JSON string: {json_str[:500]}")
            return {"themes": []}
