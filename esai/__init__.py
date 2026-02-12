"""
ESAI - Environmental Suitability Assessment Index
=================================================

A comprehensive tool for evaluating the environmental suitability of analytical methods.

Modules:
    - config: Configuration, constants, and utility functions
    - scoring: Score calculation algorithms
    - visualization: Radar chart visualization
    - report: PDF report generation
    - ui: User interface components
    - tabs: Assessment tab modules
"""

__version__ = "2.0.0"
__author__ = "ESAI Development Team"

from esai.config import AppConfig, get_resource_path
from esai.scoring import ScoreCalculator
from esai.visualization import RadarChart
from esai.report import PDFReporter
