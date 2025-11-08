
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and preprocessing of patient reviews."""
    
    def __init__(self, file_path: str):
        """
        Initialize the data loader.
        
        Args:
            file_path: Path to the CSV file containing reviews
        """
        self.file_path = Path(file_path)
        self._df = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load patient reviews from CSV file.
        
        Returns:
            DataFrame containing the reviews
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
        """
        if self._df is not None:
            return self._df
            
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        self._df = pd.read_csv(self.file_path)
        if self._df.empty:
            raise pd.errors.EmptyDataError("The CSV file is empty")
        
        if 'Comment' not in self._df.columns:
            raise ValueError("CSV file must contain a 'Comment' column")
        
        logger.info(f"Loaded {len(self._df)} rows from {self.file_path}")
        return self._df
    
    def get_reviews(self, limit: Optional[int] = None) -> List[str]:
        """
        Get a list of reviews from the loaded data.
        
        Args:
            limit: Optional limit on number of reviews to return
            
        Returns:
            List of review texts
        """
        df = self.load_data()
        reviews = df['Comment'].dropna().astype(str).tolist()
        return reviews[:limit] if limit else reviews
    
    def get_reviews_with_ground_truth(
        self, 
        limit: Optional[int] = None,
        include_empty_ground_truth: bool = False
    ) -> List[Tuple[str, str]]:
        """
        Get reviews with their ground truth ProcessedCode values.
        
        Args:
            limit: Optional limit on number of reviews to return
            include_empty_ground_truth: If True, includes reviews with NaN/empty ProcessedCode
            
        Returns:
            List of tuples: (review_text, processed_code_string)
            Only includes reviews with non-empty ProcessedCode if include_empty_ground_truth=False
        """
        df = self.load_data()
        
        if 'ProcessedCode' not in df.columns:
            raise ValueError("CSV file must contain a 'ProcessedCode' column")
        
        # Filter out rows with empty comments
        df_filtered = df[df['Comment'].notna() & (df['Comment'].astype(str).str.strip() != '')]
        
        if not include_empty_ground_truth:
   
            df_filtered = df_filtered[df_filtered['ProcessedCode'].notna()]
       
            df_filtered = df_filtered[df_filtered['ProcessedCode'].astype(str).str.strip() != '']
    
            df_filtered = df_filtered[df_filtered['ProcessedCode'].astype(str).str.lower() != 'nan']
        
        logger.info(f"Filtered to {len(df_filtered)} reviews with valid ground truth (out of {len(df)} total)")
        
        reviews_with_gt = list(zip(
            df_filtered['Comment'].astype(str).tolist(),
            df_filtered['ProcessedCode'].astype(str).tolist()
        ))
        
        return reviews_with_gt[:limit] if limit else reviews_with_gt
