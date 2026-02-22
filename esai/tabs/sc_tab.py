"""
Sample Collection (SC) Tab for ESAI
===================================

This module contains the Sample Collection assessment tab.
Principles 1-4 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, Entry, Button, StringVar, DoubleVar
from tkinter import ttk
from typing import Callable, Tuple
import numpy as np

from esai.tabs.base_tab import BaseTab, QuestionConfig, RadioChoice


class SCTab(BaseTab):
    """
    Sample Collection (SC) assessment tab.
    
    Contains 4 principles:
    1. Sample collection site
    2. Volume of sample collection
    3. Throughput of sample collection
    4. Energy consumption for sample collection
    """
    
    PRINCIPLES = [1, 2, 3, 4]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' SC ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Sample Collection tab content."""
        # Principle 1: Sample collection site
        self._create_principle_1()
        
        # Principle 2: Volume of sample collection
        self._create_principle_2()
        
        # Principle 3: Throughput of sample collection
        self._create_principle_3()
        
        # Principle 4: Energy consumption
        self._create_principle_4()
    
    def _create_principle_1(self):
        """Create Principle 1: Sample collection site."""
        config = QuestionConfig(
            id=1,
            title='Sample collection site',
            question_type='radio',
            choices=[
                RadioChoice('Ex situ', 10, 0.0, 'Ex situ'),
                RadioChoice('On site', 20, 0.33, 'On site'),
                RadioChoice('On-line', 30, 0.66, 'On-line'),
                RadioChoice('In-line', 40, 1.0, 'In-line'),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=0, column=0)
    
    def _create_principle_2(self):
        """Create Principle 2: Volume of sample collection."""
        config = QuestionConfig(
            id=2,
            title='Volume of sample collection (mg or µL)',
            question_type='entry',
            entry_unit='mg or µL',
            entry_default=''
        )
        
        def calculate_score(value):
            if value > 100000:
                return 0.0, 0.0
            elif value < 10:
                return 20.0, 1.0
            else:  # 10 <= value <= 100000
                color = round(-0.215 * np.log(value) + 2.48, 2) / 2
                score = round(-0.215 * np.log(value) + 2.48, 2) * 10
                return score, color
        
        self.create_entry_question(self.content_frame, config, row=0, column=1, 
                                   calculate_func=calculate_score)
    
    def _create_principle_3(self):
        """Create Principle 3: Throughput of sample collection."""
        config = QuestionConfig(
            id=3,
            title='Throughtput of sample collection',
            question_type='radio',
            choices=[
                RadioChoice('≤1 sample per hour', 0, 0.0, '≤1 sample per hour'),
                RadioChoice('2-10 samples per hour', 10, 0.33, '2-10 samples per hour'),
                RadioChoice('10-60 samples per hour', 15, 0.66, '10-60 samples per hour'),
                RadioChoice('>60 samples per hour', 20, 1.0, '>60 samples per hour'),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=1, column=0)
    
    def _create_principle_4(self):
        """Create Principle 4: Energy consumption for sample collection."""
        config = QuestionConfig(
            id=4,
            title='Energy consumption for sample collection',
            question_type='radio',
            choices=[
                RadioChoice('>1 kWh per sample', 0, 0.0, '>1 kWh per sample'),
                RadioChoice('0.1-1 kWh per sample', 10, 0.5, '0.1-1 kWh per sample'),
                RadioChoice('<0.1 kWh per sample', 20, 1.0, '<0.1 kWh per sample'),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=1, column=1)
    
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
