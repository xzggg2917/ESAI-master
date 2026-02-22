"""
Waste Tab for ESAI
==================

This module contains the Waste assessment tab.
Principles 26-27 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, StringVar
from tkinter import ttk
from typing import Callable, Tuple

from esai.tabs.base_tab import BaseTab


class WasteTab(BaseTab):
    """
    Waste assessment tab.
    
    Contains 2 principles:
    26. Emissions of greenhouse gases or toxic gases
    27. Waste disposal (Liquid or Solid)
    """
    
    PRINCIPLES = [26, 27]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' Waste ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Waste tab content."""
        self._create_principle_26()
        self._create_principle_27()
    
    def _create_principle_26(self):
        """Create Principle 26: Emissions of greenhouse gases."""
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
            badge_label = Label(badge_frame, text="Q26", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Emissions of greenhouse gases or toxic gases', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='26. Emissions of greenhouse gases or toxic gases', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(26, 'Emissions of toxic gases')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('Emissions of toxic gases', 0, 0.0),
            ('Significant emissions of greenhouse gases', 12.5, 0.33),
            ('Minor or controlled emissions of greenhouse gases', 25, 0.66),
            ('No direct emissions of greenhouse or toxic gases', 50, 1.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[26],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[26],
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
                    self.scores[26].set(s)
                    self.colors[26].set(c)
                    self.pdf_texts[26].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=0, column=0, sticky='new', pady=5, padx=5)
    
    def _create_principle_27(self):
        """Create Principle 27: Waste disposal."""
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
            badge_label = Label(badge_frame, text="Q27", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Waste disposal (Liquid or Solid)', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        else:
            title_label = Label(card, text='27. Waste disposal (Liquid or Solid)', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(27, '0-25%')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('0-25%', 0, 0.0),
            ('25-50%', 12.5, 0.33),
            ('50-75%', 25, 0.66),
            ('75-100%', 50, 1.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[27],
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=2
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[27],
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
                    self.scores[27].set(s)
                    self.colors[27].set(c)
                    self.pdf_texts[27].set(t)
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
