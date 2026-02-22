"""
Sample Preparation (SP) Tab for ESAI
====================================

This module contains the Sample Preparation assessment tab.
Principles 5-10 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, Entry, Button, StringVar, DoubleVar
from tkinter import ttk
from typing import Callable, Tuple
import numpy as np

from esai.tabs.base_tab import BaseTab, QuestionConfig, RadioChoice


class SPTab(BaseTab):
    """
    Sample Preparation (SP) assessment tab.
    
    Contains 6 principles:
    5. Method of sample preparation
    6. Throughput of sample preparation
    7. Amounts of wastes generated during sample preparation
    8. Number of steps and degree of automation
    9. Energy consumption for sample preparation
    10. Volume consumed for sample preparation
    """
    
    PRINCIPLES = [5, 6, 7, 8, 9, 10]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' SP (5-10) ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Sample Preparation tab content."""
        # Principle 5: Method of sample preparation
        self._create_principle_5()
        
        # Principle 6: Throughput of sample preparation
        self._create_principle_6()
        
        # Principle 7: Amounts of wastes generated
        self._create_principle_7()
        
        # Principle 8: Steps and automation
        self._create_principle_8()
        
        # Principle 9: Energy consumption
        self._create_principle_9()
        
        # Principle 10: Volume consumed
        self._create_principle_10()
    
    def _create_principle_5(self):
        """Create Principle 5: Method of sample preparation (dropdown)."""
        config = QuestionConfig(
            id=5,
            title='Method of sample preparation',
            question_type='radio',
            choices=[
                RadioChoice('Not required sample preparation', 30, 1.0),
                RadioChoice('High-greenness (SFE, SPME, enzymatic, membrane)', 20, 0.66),
                RadioChoice('Medium-greenness (ASE, PSE, PPT)', 10, 0.33),
                RadioChoice('Low-greenness (LLE, SPE, Acid-base)', 0, 0.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=0, column=0)
    
    def _create_principle_6(self):
        """Create Principle 6: Throughput of sample preparation."""
        config = QuestionConfig(
            id=6,
            title='Throughput of sample preparation',
            choices=[
                RadioChoice('≤1 sample per hour', 2.5, 0.0),
                RadioChoice('2-10 samples per hour', 8, 0.33),
                RadioChoice('10-60 samples per hour', 7.5, 0.66),
                RadioChoice('>60 samples per hour', 10, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=0, column=1)
    
    def _create_principle_7(self):
        """Create Principle 7: Amounts of wastes generated."""
        config = QuestionConfig(
            id=7,
            title='The amounts of wastes generated during sample preparation',
            question_type='radio',
            choices=[
                RadioChoice('<1 g or 1 mL per sample', 20, 1.0),
                RadioChoice('1-10 g or 1-10 mL per sample', 10, 0.5),
                RadioChoice('>10 g or 10 mL per sample', 0, 0.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=1, column=0)
    
    def _create_principle_8(self):
        """Create Principle 8: Steps and automation (combined question)."""
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
            badge_label = Label(badge_frame, text="Q8", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = 'The number of steps and degree of automation in sample preparation'
        if self.theme:
            title_label = Label(card, text=title_text, 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=600,
                              justify='left')
        else:
            title_label = Label(card, text='8. ' + title_text, 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(8, '≤2 steps + Fully automatic')
        
        # Separate vars for step and automation
        step_var = StringVar(value='0')
        auto_var = StringVar(value='0')
        
        # Store these for combined calculation
        self._step_var = step_var
        self._auto_var = auto_var
        self._step_score = 10
        self._auto_score = 10
        self._step_color = 0.5
        self._auto_color = 0.5
        self._step_text = '≤2 steps'
        self._auto_text = 'Fully automatic'
        
        # Create horizontal layout container for both sections
        horizontal_container = Frame(card, bg=bg_card)
        horizontal_container.pack(fill='x', pady=(5, 0))
        
        # Left side: Steps section
        left_section = Frame(horizontal_container, bg=bg_card)
        left_section.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        if self.theme:
            steps_label = Label(left_section, text='Number of steps:',
                              font=self.small_font,
                              fg=self.theme.colors.text_secondary,
                              bg=bg_card)
        else:
            steps_label = Label(left_section, text='Number of steps:',
                              font=self.small_font,
                              bg=bg_card)
        steps_label.pack(anchor='w', pady=(0, 5))
        
        steps_frame = Frame(left_section, bg=bg_card)
        steps_frame.pack(fill='x')
        
        # Step options
        step_choices = [
            ('≤2 steps', 10, 0.5),
            ('3-5 steps', 5, 0.25),
            ('≥6 steps', 0, 0.0),
        ]
        
        for i, (text, score, color) in enumerate(step_choices):
            option_row = Frame(steps_frame, bg=bg_card)
            option_row.pack(fill='x')
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=step_var,
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=1
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=step_var,
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=1
                )
            btn.pack(side='left', anchor='w', padx=(10, 0))
            
            def make_step_callback(s=score, c=color, t=text):
                def callback():
                    self._step_score = s
                    self._step_color = c
                    self._step_text = t
                    self._update_principle_8()
                return callback
            
            btn.config(command=make_step_callback())
        
        # Right side: Automation section
        right_section = Frame(horizontal_container, bg=bg_card)
        right_section.pack(side='left', fill='both', expand=True)
        
        if self.theme:
            auto_label = Label(right_section, text='Degree of automation:',
                             font=self.small_font,
                             fg=self.theme.colors.text_secondary,
                             bg=bg_card)
        else:
            auto_label = Label(right_section, text='Degree of automation:',
                             font=self.small_font,
                             bg=bg_card)
        auto_label.pack(anchor='w', pady=(0, 5))
        
        auto_frame = Frame(right_section, bg=bg_card)
        auto_frame.pack(fill='x')
        
        # Automation options
        auto_choices = [
            ('Fully automatic', 10, 0.5),
            ('Semi-automatic', 5, 0.25),
            ('Manual', 0, 0.0),
        ]
        
        for i, (text, score, color) in enumerate(auto_choices):
            option_row = Frame(auto_frame, bg=bg_card)
            option_row.pack(fill='x')
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=auto_var,
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    selectcolor=bg_card,
                    highlightthickness=0,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=1
                )
            else:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=auto_var,
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_card,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0,
                    padx=5,
                    pady=1
                )
            btn.pack(side='left', anchor='w', padx=(10, 0))
            
            def make_auto_callback(s=score, c=color, t=text):
                def callback():
                    self._auto_score = s
                    self._auto_color = c
                    self._auto_text = t
                    self._update_principle_8()
                return callback
            
            btn.config(command=make_auto_callback())
        
        card.grid(row=2, column=0, sticky='new', pady=5, padx=5, columnspan=2)
    
    def _update_principle_8(self):
        """Update principle 8 score from step and automation."""
        total_score = self._step_score + self._auto_score
        total_color = self._step_color + self._auto_color
        self.scores[8].set(total_score)
        self.colors[8].set(total_color)
        self.pdf_texts[8].set(f'{self._step_text} + {self._auto_text}')
        self._trigger_update()
    
    def _create_principle_9(self):
        """Create Principle 9: Energy consumption for sample preparation."""
        config = QuestionConfig(
            id=9,
            title='Energy consumption for sample preparation',
            question_type='radio',
            choices=[
                RadioChoice('>1 kWh per sample', 0, 0.0),
                RadioChoice('0.1-1 kWh per sample', 5, 0.5),
                RadioChoice('<0.1 kWh per sample', 10, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=3, column=0)
    
    def _create_principle_10(self):
        """Create Principle 10: Volume consumed for sample preparation."""
        config = QuestionConfig(
            id=10,
            title='Volume consumed for sample preparation ( mg or µL, per sample )',
            question_type='entry',
            entry_unit='mg or µL',
            entry_default=''
        )
        
        def calculate_score(value):
            if value > 100000:
                return 0.0, 0.0
            elif value < 10:
                return 10.0, 1.0
            else:  # 10 <= value <= 100000
                color = round((-0.067 * np.log(value) ** 1.432 + 2.22), 2) / 2
                score = round(-0.067 * np.log(value) ** 1.432 + 2.22, 2) * 5
                return score, color
        
        self.create_entry_question(self.content_frame, config, row=3, column=1, 
                                   calculate_func=calculate_score)
    
    def get_dimension_score(self, weight: float) -> float:
        """
        Calculate the weighted dimension score.
        
        Args:
            weight: Weight for this dimension (w2)
            
        Returns:
            Weighted sum of principle scores
        """
        total = sum(self.scores[p].get() for p in self.PRINCIPLES)
        return round(total * weight, 2)
