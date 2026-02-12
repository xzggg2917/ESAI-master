"""
Scoring Module for ESAI
=======================

This module contains:
- Score calculation algorithms
- Dimension score aggregation
- Color mapping for scores
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize

from esai.config import ColorConfig, WeightConfig


@dataclass
class PrincipleScore:
    """Score data for a single assessment principle."""
    id: int
    score: float = 0.0
    color_value: float = 0.0
    pdf_text: str = ""
    
    def reset(self, default_text: str = ""):
        """Reset the score to default values."""
        self.score = 0.0
        self.color_value = 0.0
        self.pdf_text = default_text


@dataclass
class DimensionScore:
    """Aggregated score for a dimension."""
    name: str
    short_label: str
    weight: float
    principles: List[int]  # List of principle IDs in this dimension
    
    _score: float = 0.0
    
    @property
    def score(self) -> float:
        return self._score
    
    @score.setter
    def score(self, value: float):
        self._score = round(value, 2)


class ScoreCalculator:
    """
    Calculator for ESAI scores.
    
    Manages 27 assessment principles organized into 8 dimensions:
    - SC (Sample Collection): Principles 1-4
    - SP (Sample Preparation): Principles 5-10
    - AT (Analysis Technique): Principles 11-16
    - Economy: Principle 17
    - Method: Principles 18-19
    - Operator Safety: Principle 20
    - Reagent: Principles 21-25
    - Waste/Environment: Principles 26-27
    """
    
    # Mapping of dimensions to their principle IDs
    DIMENSION_PRINCIPLES = {
        'SC': [1, 2, 3, 4],
        'SP': [5, 6, 7, 8, 9, 10],
        'AT': [11, 12, 13, 14, 15, 16],
        'Economy': [17],
        'Method': [18, 19],
        'Operator': [20],
        'Reagent': [21, 22, 23, 24, 25],
        'Waste': [26, 27]
    }
    
    # Default PDF text for each principle
    DEFAULT_PDF_TEXTS = {
        1: 'Ex situ',
        2: '0 g/ml',
        3: '≤1 sample per hour',
        4: '>1 kWh per sample',
        5: '1',
        6: '<1 g/mL',
        7: '>10 g or 10 mL per sample',
        8: '≤2 steps / Fully automatic',
        9: '>1 kWh per sample',
        10: '>100 g or 100 mL',
        11: 'High-energy consumption instrument',
        12: '>1 mL',
        13: '≤1 sample per hour',
        14: '>10 g or 10 mL per sample',
        15: 'Manual',
        16: '>1 kWh per sample',
        17: '0 yuan',
        18: 'Qualitative',
        19: 'Single target per analysis',
        20: '0',
        21: '>6',
        22: '>10 mL',
        23: 'Acute toxicity',
        24: '> 100 mL',
        25: '0-25%',
        26: 'Yes',
        27: '0-25%'
    }
    
    def __init__(self, weights: Optional[WeightConfig] = None, 
                 colors: Optional[ColorConfig] = None):
        """
        Initialize the score calculator.
        
        Args:
            weights: Weight configuration for dimensions
            colors: Color configuration for score mapping
        """
        self.weights = weights or WeightConfig()
        self.colors = colors or ColorConfig()
        
        # Initialize 27 principle scores
        self.principles: Dict[int, PrincipleScore] = {}
        for i in range(1, 28):
            self.principles[i] = PrincipleScore(
                id=i, 
                pdf_text=self.DEFAULT_PDF_TEXTS.get(i, "")
            )
        
        # Initialize colormap
        self._update_colormap()
        
        # Dimension scores
        self.dimension_scores: Dict[str, float] = {
            'SC': 0.0, 'SP': 0.0, 'AT': 0.0, 'Economy': 0.0,
            'Method': 0.0, 'Operator': 0.0, 'Reagent': 0.0, 'Waste': 0.0
        }
        
        # Total score
        self.total_score: float = 0.0
    
    def _update_colormap(self):
        """Update the colormap based on color configuration."""
        self.colormap = mcolors.LinearSegmentedColormap(
            'ESAI_ColorMap', 
            self.colors.color_dict
        )
    
    def set_principle_score(self, principle_id: int, score: float, 
                           color_value: float = None, pdf_text: str = None):
        """
        Set the score for a specific principle.
        
        Args:
            principle_id: Principle number (1-27)
            score: Score value (0-100)
            color_value: Color mapping value (0-1), defaults to score/100
            pdf_text: Text description for PDF report
        """
        if principle_id not in self.principles:
            raise ValueError(f"Invalid principle ID: {principle_id}")
        
        principle = self.principles[principle_id]
        principle.score = score
        principle.color_value = color_value if color_value is not None else score / 100
        if pdf_text is not None:
            principle.pdf_text = pdf_text
    
    def get_principle_score(self, principle_id: int) -> PrincipleScore:
        """Get the score data for a specific principle."""
        return self.principles.get(principle_id)
    
    def calculate_dimension_scores(self) -> Dict[str, float]:
        """
        Calculate scores for each dimension based on principle scores and weights.
        
        Returns:
            Dictionary mapping dimension names to their scores
        """
        weights = self.weights
        
        # SC: Principles 1-4
        sc_sum = sum(self.principles[i].score for i in [1, 2, 3, 4])
        self.dimension_scores['SC'] = round(sc_sum * weights.w1, 2)
        
        # SP: Principles 5-10
        sp_sum = sum(self.principles[i].score for i in [5, 6, 7, 8, 9, 10])
        self.dimension_scores['SP'] = round(sp_sum * weights.w2, 2)
        
        # AT: Principles 11-16
        at_sum = sum(self.principles[i].score for i in [11, 12, 13, 14, 15, 16])
        self.dimension_scores['AT'] = round(at_sum * weights.w3, 2)
        
        # Economy: Principle 17
        self.dimension_scores['Economy'] = round(
            self.principles[17].score * weights.w4, 2
        )
        
        # Method: Principles 18-19
        method_sum = sum(self.principles[i].score for i in [18, 19])
        self.dimension_scores['Method'] = round(method_sum * weights.w5, 2)
        
        # Operator: Principle 20
        self.dimension_scores['Operator'] = round(
            self.principles[20].score * weights.w6, 2
        )
        
        # Reagent: Principles 21-25
        reagent_sum = sum(self.principles[i].score for i in [21, 22, 23, 24, 25])
        self.dimension_scores['Reagent'] = round(reagent_sum * weights.w7, 2)
        
        # Waste: Principles 26-27
        waste_sum = sum(self.principles[i].score for i in [26, 27])
        self.dimension_scores['Waste'] = round(waste_sum * weights.w8, 2)
        
        return self.dimension_scores
    
    def calculate_total_score(self) -> float:
        """
        Calculate the total ESAI score.
        
        Returns:
            Total score (sum of all dimension scores)
        """
        self.calculate_dimension_scores()
        self.total_score = round(sum(self.dimension_scores.values()), 2)
        return self.total_score
    
    def get_dimension_color(self, dimension: str) -> Tuple[float, float, float]:
        """
        Get the RGB color for a dimension based on its score.
        
        Args:
            dimension: Dimension name
            
        Returns:
            RGB tuple (0-1 range)
        """
        score = self.dimension_scores.get(dimension, 0)
        weight = getattr(self.weights, f'w{list(self.dimension_scores.keys()).index(dimension) + 1}', 0.1)
        
        max_score = 100 * weight
        norm = Normalize(vmin=0, vmax=max_score)
        
        return mcolors.to_rgb(self.colormap(norm(score)))
    
    def get_principle_color(self, principle_id: int) -> Tuple[float, float, float]:
        """
        Get the RGB color for a principle based on its color value.
        
        Args:
            principle_id: Principle number (1-27)
            
        Returns:
            RGB tuple (0-1 range)
        """
        color_value = self.principles[principle_id].color_value
        return mcolors.to_rgb(self.colormap(color_value))
    
    def get_total_color(self) -> Tuple[float, float, float]:
        """
        Get the RGB color for the total score.
        
        Returns:
            RGB tuple (0-1 range)
        """
        norm = Normalize(vmin=0, vmax=100)
        return mcolors.to_rgb(self.colormap(norm(self.total_score)))
    
    def reset_all(self):
        """Reset all scores to default values."""
        for i, principle in self.principles.items():
            principle.reset(self.DEFAULT_PDF_TEXTS.get(i, ""))
        
        for dimension in self.dimension_scores:
            self.dimension_scores[dimension] = 0.0
        
        self.total_score = 0.0
    
    def get_report_data(self) -> Dict:
        """
        Get all data needed for report generation.
        
        Returns:
            Dictionary containing all scores and texts for reporting
        """
        return {
            'principles': {
                i: {
                    'score': p.score,
                    'color_value': p.color_value,
                    'pdf_text': p.pdf_text
                }
                for i, p in self.principles.items()
            },
            'dimensions': self.dimension_scores.copy(),
            'total': self.total_score,
            'weights': self.weights.as_dict()
        }


def create_score_calculator(weights: WeightConfig = None, 
                           colors: ColorConfig = None) -> ScoreCalculator:
    """
    Factory function to create a ScoreCalculator instance.
    
    Args:
        weights: Optional weight configuration
        colors: Optional color configuration
        
    Returns:
        Configured ScoreCalculator instance
    """
    return ScoreCalculator(weights=weights, colors=colors)
