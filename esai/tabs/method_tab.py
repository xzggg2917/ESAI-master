"""
Method Tab for ESAI
===================

This module contains the Method assessment tab.
Principles 18-19 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, StringVar
from tkinter import ttk
from typing import Callable, Tuple

from esai.tabs.base_tab import BaseTab, QuestionConfig, RadioChoice


class MethodTab(BaseTab):
    """
    Method assessment tab.
    
    Contains 2 principles:
    18. Type of analysis
    19. Multiple or single-element analysis
    """
    
    PRINCIPLES = [18, 19]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' Method ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Method tab content."""
        self._create_principle_18()
        self._create_principle_19()
    
    def _create_principle_18(self):
        """Create Principle 18: Type of analysis."""
        # Get theme colors
        if self.theme:
            bg_card = self.theme.colors.bg_card
            border_color = self.theme.colors.border
        else:
            bg_card = 'white'
            border_color = '#E0E0E0'
        
        # Card container
        card = Frame(self.content_frame, bg=bg_card,
                    highlightbackground=border_color,
                    highlightthickness=1,
                    padx=12, pady=10)
        
        # Question number badge
        if self.theme:
            badge_frame = Frame(card, bg=self.theme.colors.primary, padx=8, pady=3)
            badge_label = Label(badge_frame, text="Q18", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Type of analysis', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='18. Type of analysis', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(18, 'Qualitative')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('Qualitative', 0, 0.0),
            ('Qualitative and semi quantitative', 30, 0.5),
            ('Quantitative', 50, 1.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[18],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    wraplength=320,
                    justify='left',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[18],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            btn.pack(side='left', anchor='w', padx=(10, 0))
            
            def make_callback(s=score, c=color, t=text):
                def callback():
                    self.scores[18].set(s)
                    self.colors[18].set(c)
                    self.pdf_texts[18].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=0, column=0, sticky='new', pady=5, padx=5)
    
    def _create_principle_19(self):
        """Create Principle 19: Multiple or single-element analysis."""
        # Get theme colors
        if self.theme:
            bg_card = self.theme.colors.bg_card
            border_color = self.theme.colors.border
        else:
            bg_card = 'white'
            border_color = '#E0E0E0'
        
        # Card container
        card = Frame(self.content_frame, bg=bg_card,
                    highlightbackground=border_color,
                    highlightthickness=1,
                    padx=12, pady=10)
        
        # Question number badge
        if self.theme:
            badge_frame = Frame(card, bg=self.theme.colors.primary, padx=8, pady=3)
            badge_label = Label(badge_frame, text="Q19", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Multiple or single-element analysis', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        else:
            title_label = Label(card, text='19. Multiple or single-element analysis', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(19, 'Single element analysis')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('Single target per analysis', 20, 0.0),
            ('Multiple targets analysis for 2-10 compounds per analysis', 30, 0.25),
            ('Multiple targets analysis for 11-20 compounds per analysis', 40, 0.5),
            ('Multiple targets analysis for >20 compounds per analysis', 50, 1.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[19],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    wraplength=320,
                    justify='left',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[19],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            btn.pack(side='left', anchor='w', padx=(10, 0))
            
            def make_callback(s=score, c=color, t=text):
                def callback():
                    self.scores[19].set(s)
                    self.colors[19].set(c)
                    self.pdf_texts[19].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=1, column=0, sticky='new', pady=5, padx=5, columnspan=2)
    
    def get_dimension_score(self, weight: float) -> float:
        """
        Calculate the weighted dimension score.
        
        Args:
            weight: Weight for this dimension
            
        Returns:
            Sum of principle scores multiplied by weight
        """
        total = sum(self.scores[p].get() for p in self.PRINCIPLES)
        return round(total * weight, 2)
