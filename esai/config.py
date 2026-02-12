"""
Configuration Module for ESAI
=============================

This module contains:
- Application configuration and constants
- Resource path management
- Locale configuration
- Font configuration for matplotlib
"""

import locale
import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import matplotlib
import matplotlib.font_manager as fm


# ============================================================================
# Resource Path Management
# ============================================================================

def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource files (images, icons, etc.).
    Works correctly regardless of the current working directory.
    
    Args:
        relative_path: Relative path to the resource file
        
    Returns:
        Absolute path to the resource file
        
    This function ensures that resource files can be found even when:
    - Running from different working directories
    - Running as a script vs. frozen executable (PyInstaller, etc.)
    - Importing as a module
    """
    try:
        # Get the directory where this script is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable (PyInstaller)
            base_path = Path(sys.executable).parent
        else:
            # Running as normal Python script - go up one level from esai/
            base_path = Path(__file__).parent.parent.resolve()
        
        # Construct absolute path to resource
        resource_path = base_path / relative_path
        
        # Verify the file exists
        if not resource_path.exists():
            raise FileNotFoundError(
                f"Resource file not found: {resource_path}\n"
                f"Looking in directory: {base_path}\n"
                f"Please ensure the file exists in the application directory."
            )
        
        return str(resource_path)
        
    except Exception as e:
        print(f"Error locating resource '{relative_path}': {e}")
        print(f"Current working directory: {os.getcwd()}")
        raise


# ============================================================================
# Locale Configuration
# ============================================================================

def configure_locale():
    """
    Configure locale settings for cross-platform compatibility.
    
    This prevents crashes on systems with non-standard locale settings
    (common in Docker containers, minimal Linux installations, and 
    various Windows configurations).
    """
    try:
        if os.name == 'nt':  # Windows
            try:
                locale.setlocale(locale.LC_ALL, 'C')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                except locale.Error:
                    pass
        else:  # Unix-like systems
            os.environ['LC_ALL'] = 'C'
            os.environ['LANG'] = 'C'
    except Exception as e:
        print(f"Warning: Could not set locale: {e}")


# ============================================================================
# Font Configuration
# ============================================================================

def configure_matplotlib_fonts() -> List[str]:
    """
    Configure matplotlib to use appropriate fonts with intelligent fallback.
    
    Returns:
        List of available font names that were configured
    """
    # List of fonts to try, in order of preference
    font_candidates = [
        # Chinese fonts (for proper Chinese character display)
        'SimHei',           # Windows simplified Chinese
        'Microsoft YaHei',  # Windows modern Chinese
        'STHeiti',          # macOS Chinese
        'WenQuanYi Micro Hei',  # Linux Chinese
        'Noto Sans CJK SC', # Google Noto (cross-platform)
        'Source Han Sans CN',  # Adobe Source Han
        'PingFang SC',      # macOS modern Chinese
        'Hiragino Sans GB', # macOS Japanese/Chinese
        # Universal fallbacks
        'DejaVu Sans',      # Common on Linux
        'Arial',            # Common on Windows/Mac
        'Helvetica',        # macOS default
        'sans-serif'        # System default
    ]
    
    # Get list of available fonts on the system
    available_fonts = set(f.name for f in fm.fontManager.ttflist)
    
    # Find which fonts from our list are actually available
    available_candidates = [font for font in font_candidates if font in available_fonts]
    
    if available_candidates:
        matplotlib.rcParams['font.sans-serif'] = available_candidates
        print(f"Matplotlib configured with fonts: {', '.join(available_candidates[:3])}")
    else:
        print("Warning: Using system default fonts. Text display may vary.")
    
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['axes.unicode_minus'] = False
    
    return available_candidates


# ============================================================================
# Application Configuration
# ============================================================================

@dataclass
class ColorConfig:
    """Color configuration for the application."""
    start_color_hex: str = 'C5161B'  # Red (low score)
    end_color_hex: str = '#008843'   # Green (high score)
    
    def get_rgb(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to RGB tuple (0-1 range)."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    
    @property
    def start_rgb(self) -> Tuple[float, float, float]:
        return self.get_rgb(self.start_color_hex)
    
    @property
    def end_rgb(self) -> Tuple[float, float, float]:
        return self.get_rgb(self.end_color_hex)
    
    @property
    def color_dict(self) -> dict:
        """Get matplotlib colormap dictionary."""
        start = self.start_rgb
        end = self.end_rgb
        return {
            'red': ((0.0, start[0], start[0]),
                    (0.5, 1.0, 1.0),
                    (1.0, end[0], end[0])),
            'green': ((0.0, start[1], start[1]),
                      (0.5, 1.0, 1.0),
                      (1.0, end[1], end[1])),
            'blue': ((0.0, start[2], start[2]),
                     (0.5, 1.0, 1.0),
                     (1.0, end[2], end[2]))
        }


@dataclass
class WindowConfig:
    """Window configuration."""
    width: int = 1000
    height: int = 510
    title: str = "Environmental suitability assessment index"
    font_style: Tuple[str, int] = ("Times New Roman", 12)
    
    def get_centered_position(self, screen_width: int, screen_height: int) -> Tuple[int, int]:
        """Calculate centered window position."""
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        return x, y
    
    def get_dialog_position(self, screen_width: int, screen_height: int) -> Tuple[int, int]:
        """Calculate dialog/popup position."""
        x = (screen_width - self.width) // 2 + 200
        y = (screen_height - self.height) // 2 + 150
        return x, y


@dataclass
class WeightConfig:
    """Weight configuration for scoring dimensions."""
    # Default weights
    w1: float = 0.1   # SC - Sample Collection
    w2: float = 0.2   # SP - Sample Preparation
    w3: float = 0.2   # AT - Analysis Technique
    w4: float = 0.05  # Economy
    w5: float = 0.05  # Method
    w6: float = 0.1   # Operator Safety
    w7: float = 0.1   # Reagent
    w8: float = 0.2   # Waste/Environment
    
    # Preset weight configurations
    PRESETS: dict = field(default_factory=lambda: {
        1: (0.2, 0.2, 0.1, 0.05, 0.05, 0.05, 0.15, 0.2),
        2: (0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05, 0.2),
        3: (0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2),
        4: (0.2, 0.2, 0.05, 0.05, 0.05, 0.05, 0.2, 0.2),
        5: (0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.2, 0.05),
        6: (0.2, 0.2, 0.2, 0.1, 0.05, 0.1, 0.1, 0.05),
        7: (0.1, 0.2, 0.2, 0.05, 0.05, 0.1, 0.1, 0.2),  # Default
    })
    
    def set_preset(self, preset_id: int):
        """Set weights from a preset configuration."""
        if preset_id in self.PRESETS:
            weights = self.PRESETS[preset_id]
            self.w1, self.w2, self.w3, self.w4 = weights[:4]
            self.w5, self.w6, self.w7, self.w8 = weights[4:]
    
    def set_custom(self, w1: float, w2: float, w3: float, w4: float,
                   w5: float, w6: float, w7: float, w8: float) -> bool:
        """
        Set custom weights. Returns True if valid (sum == 1.0).
        """
        total = round(w1 + w2 + w3 + w4 + w5 + w6 + w7 + w8, 2)
        if total == 1.0:
            self.w1, self.w2, self.w3, self.w4 = w1, w2, w3, w4
            self.w5, self.w6, self.w7, self.w8 = w5, w6, w7, w8
            return True
        return False
    
    def as_tuple(self) -> Tuple[float, ...]:
        """Return weights as tuple."""
        return (self.w1, self.w2, self.w3, self.w4, 
                self.w5, self.w6, self.w7, self.w8)
    
    def as_dict(self) -> dict:
        """Return weights as dictionary."""
        return {
            'SC': self.w1, 'SP': self.w2, 'AT': self.w3, 'Economy': self.w4,
            'Method': self.w5, 'Operator': self.w6, 'Reagent': self.w7, 'Waste': self.w8
        }


@dataclass
class AppConfig:
    """Main application configuration."""
    window: WindowConfig = field(default_factory=WindowConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)
    weights: WeightConfig = field(default_factory=WeightConfig)
    
    # Dimension labels
    DIMENSION_LABELS: Tuple[str, ...] = ('Sample collection', 'Sample preparation', 'Analytical techniques', 'Economy', 
                                          'Method', 'Operator', 'Reagent', 'Waste')
    
    # Short labels for radar chart
    DIMENSION_SHORT_LABELS: Tuple[str, ...] = ('C', 'P', 'A', 'E', 'M', 'O', 'R', 'W')
    
    # Number of assessment principles
    NUM_PRINCIPLES: int = 27
    
    # Number of dimensions
    NUM_DIMENSIONS: int = 8


# Global configuration instance
config = AppConfig()


# ============================================================================
# Initialization
# ============================================================================

def initialize():
    """Initialize the application configuration."""
    configure_locale()
    configure_matplotlib_fonts()
    return config
