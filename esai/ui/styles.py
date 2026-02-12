"""
ESAI Theme Styles
=================

Modern styling configuration for the ESAI application.
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class ThemeColors:
    """Color palette for the application."""
    # Primary colors
    primary: str = "#2196F3"        # Blue
    primary_dark: str = "#1976D2"
    primary_light: str = "#BBDEFB"
    
    # Secondary colors
    secondary: str = "#4CAF50"      # Green
    secondary_dark: str = "#388E3C"
    
    # Accent colors
    accent: str = "#FF5722"         # Deep Orange
    
    # Background colors
    bg_main: str = "#FAFAFA"        # Light gray
    bg_card: str = "#FFFFFF"        # White
    bg_sidebar: str = "#ECEFF1"     # Blue gray light
    
    # Text colors
    text_primary: str = "#212121"   # Almost black
    text_secondary: str = "#757575" # Gray
    text_light: str = "#FFFFFF"     # White
    
    # Status colors
    success: str = "#4CAF50"
    warning: str = "#FFC107"
    error: str = "#F44336"
    info: str = "#2196F3"
    
    # Border colors
    border: str = "#E0E0E0"
    border_focus: str = "#2196F3"
    
    # Score colors (gradient from red to green)
    score_low: str = "#F44336"      # Red
    score_mid: str = "#FFC107"      # Yellow
    score_high: str = "#4CAF50"     # Green


@dataclass
class ThemeFonts:
    """Font configuration."""
    family: str = "Segoe UI"
    family_alt: str = "Microsoft YaHei"
    
    size_large: int = 14
    size_normal: int = 11
    size_small: int = 10
    size_tiny: int = 9
    
    @property
    def title(self) -> Tuple[str, int, str]:
        return (self.family, self.size_large, "bold")
    
    @property
    def heading(self) -> Tuple[str, int, str]:
        return (self.family, self.size_normal, "bold")
    
    @property
    def body(self) -> Tuple[str, int]:
        return (self.family, self.size_normal)
    
    @property
    def small(self) -> Tuple[str, int]:
        return (self.family, self.size_small)
    
    @property
    def tiny(self) -> Tuple[str, int]:
        return (self.family, self.size_tiny)


@dataclass
class ThemeSpacing:
    """Spacing configuration."""
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32


class ModernTheme:
    """
    Modern theme configuration for ESAI.
    """
    
    def __init__(self):
        self.colors = ThemeColors()
        self.fonts = ThemeFonts()
        self.spacing = ThemeSpacing()
    
    def apply_to_root(self, root: tk.Tk):
        """Apply theme to root window."""
        root.configure(bg=self.colors.bg_main)
        self._configure_styles()
    
    def _configure_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        
        # Try to use a modern theme as base
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
        
        # Configure Notebook (tabs)
        style.configure('TNotebook', 
                       background=self.colors.bg_main,
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=self.colors.bg_sidebar,
                       foreground=self.colors.text_primary,
                       padding=[12, 8],
                       font=self.fonts.small)
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors.primary),
                            ('active', self.colors.primary_light)],
                 foreground=[('selected', self.colors.text_light),
                            ('active', self.colors.text_primary)],
                 expand=[('selected', [0, 0, 0, 2])])
        
        # Configure Frame
        style.configure('TFrame', background=self.colors.bg_main)
        style.configure('Card.TFrame', 
                       background=self.colors.bg_card,
                       relief='flat')
        
        # Configure Label
        style.configure('TLabel',
                       background=self.colors.bg_main,
                       foreground=self.colors.text_primary,
                       font=self.fonts.body)
        
        style.configure('Title.TLabel',
                       font=self.fonts.title,
                       foreground=self.colors.primary_dark)
        
        style.configure('Heading.TLabel',
                       font=self.fonts.heading,
                       foreground=self.colors.text_primary)
        
        style.configure('Score.TLabel',
                       font=(self.fonts.family, 16, 'bold'),
                       foreground=self.colors.primary)
        
        # Configure Button
        style.configure('TButton',
                       background=self.colors.primary,
                       foreground=self.colors.text_light,
                       font=self.fonts.body,
                       padding=[16, 8])
        
        style.map('TButton',
                 background=[('active', self.colors.primary_dark),
                            ('pressed', self.colors.primary_dark)])
        
        style.configure('Primary.TButton',
                       background=self.colors.primary,
                       foreground=self.colors.text_light)
        
        style.configure('Success.TButton',
                       background=self.colors.success,
                       foreground=self.colors.text_light)
        
        # Configure Radiobutton
        style.configure('TRadiobutton',
                       background=self.colors.bg_main,
                       foreground=self.colors.text_primary,
                       font=self.fonts.small)
        
        style.map('TRadiobutton',
                 background=[('active', self.colors.bg_main)],
                 foreground=[('active', self.colors.primary)])
        
        # Configure Entry
        style.configure('TEntry',
                       fieldbackground=self.colors.bg_card,
                       foreground=self.colors.text_primary,
                       font=self.fonts.body,
                       padding=[8, 4])
        
        # Configure LabelFrame
        style.configure('TLabelframe',
                       background=self.colors.bg_main,
                       foreground=self.colors.primary,
                       font=self.fonts.heading)
        
        style.configure('TLabelframe.Label',
                       background=self.colors.bg_main,
                       foreground=self.colors.primary_dark,
                       font=self.fonts.heading)
    
    def get_button_style(self, button_type: str = "primary") -> Dict[str, Any]:
        """Get button styling dictionary."""
        styles = {
            "primary": {
                "bg": self.colors.primary,
                "fg": self.colors.text_light,
                "activebackground": self.colors.primary_dark,
                "activeforeground": self.colors.text_light,
                "font": self.fonts.body,
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8,
                "borderwidth": 0,
            },
            "success": {
                "bg": self.colors.success,
                "fg": self.colors.text_light,
                "activebackground": self.colors.secondary_dark,
                "activeforeground": self.colors.text_light,
                "font": self.fonts.body,
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8,
                "borderwidth": 0,
            },
            "secondary": {
                "bg": self.colors.bg_sidebar,
                "fg": self.colors.text_primary,
                "activebackground": self.colors.border,
                "activeforeground": self.colors.text_primary,
                "font": self.fonts.body,
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8,
                "borderwidth": 0,
            }
        }
        return styles.get(button_type, styles["primary"])
    
    def get_card_style(self) -> Dict[str, Any]:
        """Get card container styling."""
        return {
            "bg": self.colors.bg_card,
            "highlightbackground": self.colors.border,
            "highlightthickness": 1,
            "padx": self.spacing.md,
            "pady": self.spacing.md,
        }
    
    def get_score_card_style(self) -> Dict[str, Any]:
        """Get score card styling."""
        return {
            "bg": self.colors.bg_card,
            "highlightbackground": self.colors.primary_light,
            "highlightthickness": 2,
            "padx": self.spacing.sm,
            "pady": self.spacing.sm,
        }


# Tab name configuration for shorter display
TAB_NAMES = {
    'weight': 'Settings',
    'sc': 'Sample collection (1-4)',
    'sp': 'Sample preparation (5-10)',
    'at': 'Analytical techniques (11-16)',
    'economy': 'Economy',
    'method': 'Method',
    'operator': 'Operator',
    'reagent': 'Reagent',
    'waste': 'Waste'
}


# Global theme instance
THEME = ModernTheme()
