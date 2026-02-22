"""
Operator Safety Tab for ESAI
============================

This module contains the Operator Safety assessment tab.
Principle 20 belongs to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, StringVar
from tkinter import ttk
from typing import Callable, Tuple

from esai.tabs.base_tab import BaseTab


class OperatorTab(BaseTab):
    """
    Operator Safety assessment tab.
    
    Contains 1 principle:
    20. The number of safety factors involved in the experiment
    """
    
    PRINCIPLES = [20]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' Operator ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Operator Safety tab content."""
        self._create_principle_20()
    
    def _create_principle_20(self):
        """Create Principle 20: Safety factors."""
        # Get theme colors
        if self.theme:
            bg_card = self.theme.colors.bg_card
            bg_main = self.theme.colors.bg_main
            border_color = self.theme.colors.border
        else:
            bg_card = 'white'
            bg_main = None
            border_color = '#E0E0E0'
        
        # Info card for safety factors list
        info_card = Frame(self.content_frame, bg=bg_card,
                         highlightbackground=border_color,
                         highlightthickness=1,
                         padx=12, pady=10)
        
        if self.theme:
            info_badge = Frame(info_card, bg='#FF9800', padx=8, pady=3)
            info_label = Label(info_badge, text="ℹ Info", 
                             font=(self.theme.fonts.family, 9, 'bold'),
                             bg='#FF9800',
                             fg='white')
            info_label.pack()
            info_badge.pack(anchor='w', pady=(0, 8))
        
        # Safety factors header
        header_text = 'Safety factors involved in the experiment'
        if self.theme:
            header_label = Label(info_card, text=header_text,
                               font=self.title_font,
                               fg=self.theme.colors.text_primary,
                               bg=bg_card)
        else:
            header_label = Label(info_card, text=header_text,
                               font=self.font_style,
                               bg=bg_card)
        header_label.pack(anchor='w', pady=(0, 10))
        
        # Safety factors list
        factors = [
            'Bio-accumulation potential',
            'Persistence',
            'Flammability',
            'Oxidazability',
            'Explosiveness',
            'Corrosiveness',
            'Radiation',
            'Carcinogenicity',
            'Teratogenicity'
        ]
        
        factors_frame = Frame(info_card, bg=bg_card)
        factors_frame.pack(fill='x', padx=10)
        
        # Bold font for safety factors
        if self.theme:
            bold_font = (self.theme.fonts.family, self.theme.fonts.size_small, 'bold')
        else:
            bold_font = ('Segoe UI', 10, 'bold')
        
        for factor in factors:
            if self.theme:
                bullet = Label(factors_frame, text='• ' + factor,
                             font=bold_font,
                             fg=self.theme.colors.text_secondary,
                             bg=bg_card,
                             anchor='w')
            else:
                bullet = Label(factors_frame, text='• ' + factor,
                             font=bold_font,
                             bg=bg_card,
                             anchor='w')
            bullet.pack(anchor='w', pady=1)
        
        info_card.grid(row=0, column=0, sticky='new', pady=5, padx=5, columnspan=2)
        
        # Question card
        question_card = Frame(self.content_frame, bg=bg_card,
                            highlightbackground=border_color,
                            highlightthickness=1,
                            padx=12, pady=10)
        
        # Question number badge
        if self.theme:
            badge_frame = Frame(question_card, bg=self.theme.colors.primary, padx=8, pady=3)
            badge_label = Label(badge_frame, text="Q20", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Question title
        title_text = 'The number of safety factors involved in the experiment'
        if self.theme:
            title_label = Label(question_card, text=title_text,
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        else:
            title_label = Label(question_card, text='20. ' + title_text,
                              font=self.font_style,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(20, '≥3')
        
        # Options container
        options_frame = Frame(question_card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('0', 100, 1.0),
            ('1', 50, 0.66),
            ('2', 25, 0.33),
            ('≥3', 0, 0.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            # Option row
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[20],
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
                    variable=self.selected_vars[20],
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
                    self.scores[20].set(s)
                    self.colors[20].set(c)
                    self.pdf_texts[20].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        question_card.grid(row=1, column=0, sticky='new', pady=5, padx=5, columnspan=2)
    
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
