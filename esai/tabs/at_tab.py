"""
Analytical Technique (AT) Tab for ESAI
======================================

This module contains the Analytical Technique assessment tab.
Principles 11-16 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, Entry, Button, StringVar, DoubleVar
from tkinter import ttk
from typing import Callable, Tuple
import numpy as np

from esai.tabs.base_tab import BaseTab, QuestionConfig, RadioChoice


class ATTab(BaseTab):
    """
    Analytical Technique (AT) assessment tab.
    
    Contains 6 principles:
    11. Instrument
    12. Volume of injection
    13. Throughput of analysis
    14. Amounts of wastes generated during analysis
    15. Degree of automation for analysis
    16. Consumption of energy during analysis
    """
    
    PRINCIPLES = [11, 12, 13, 14, 15, 16]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' AT ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Analytical Technique tab content."""
        # Principle 11: Instrument
        self._create_principle_11()
        
        # Principle 12: Volume of injection
        self._create_principle_12()
        
        # Principle 13: Throughput of analysis
        self._create_principle_13()
        
        # Principle 14: Amounts of wastes generated
        self._create_principle_14()
        
        # Principle 15: Degree of automation
        self._create_principle_15()
        
        # Principle 16: Energy consumption
        self._create_principle_16()
    
    def _create_principle_11(self):
        """Create Principle 11: Instrument."""
        config = QuestionConfig(
            id=11,
            title='Instrument',
            question_type='radio',
            choices=[
                RadioChoice('High-energy consumption instrument (such as HPLC, GC, UHPLC, LC-MS, 2D-LC, GC-MS, 2D-GC, XRD, XRF, etc.)', 5, 0.0),
                RadioChoice('Medium-energy consumption instrument (such as UV-Vis, fluorescence spectrophotometer, atomic absorption spectrometer, Mini mass spectrometer, etc.)', 10, 0.5),
                RadioChoice('Low-energy consumption instrument (such as portable analyzer, handheld Raman spectrometer, etc.)', 20, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=0, column=0)
    
    def _create_principle_12(self):
        """Create Principle 12: Volume of injection."""
        config = QuestionConfig(
            id=12,
            title='Volume of injection ( mg or µL )',
            question_type='entry',
            entry_unit='mg/µL',
            entry_default=''
        )
        
        def calculate_score(value):
            if value > 1000:
                return 0.0, 0.0
            elif value < 1:
                return 10.0, 1.0
            else:  # 1 <= value <= 1000
                color = round((-0.289 * np.log(value) + 2), 2) / 2
                score = round(-0.289 * np.log(value) + 2, 2) * 5
                return score, color
        
        self.create_entry_question(self.content_frame, config, row=0, column=1,
                                   calculate_func=calculate_score)
    
    def _create_principle_13(self):
        """Create Principle 13: Throughput of analysis."""
        config = QuestionConfig(
            id=13,
            title='Throughput of analysis',
            question_type='radio',
            choices=[
                RadioChoice('≤1 sample per hour', 5, 0.0),
                RadioChoice('2-10 samples per hour', 10, 0.33),
                RadioChoice('10-90 samples per hour', 15, 0.66),
                RadioChoice('>90 samples per hour', 20, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=1, column=0)
    
    def _create_principle_14(self):
        """Create Principle 14: Amounts of wastes generated."""
        config = QuestionConfig(
            id=14,
            title='The amounts of wastes generated during analysis',
            question_type='radio',
            choices=[
                RadioChoice('>10 g or 10 mL per sample', 0, 0.0),
                RadioChoice('1-10 g or 1-10 mL per sample', 10, 0.5),
                RadioChoice('<1 g or 1 mL per sample', 20, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=1, column=1)
    
    def _create_principle_15(self):
        """Create Principle 15: Degree of automation."""
        config = QuestionConfig(
            id=15,
            title='The degree of automation for analysis',
            question_type='radio',
            choices=[
                RadioChoice('Manual', 0, 0.0),
                RadioChoice('Semi-automatic', 5, 0.5),
                RadioChoice('Fully automatic', 10, 1.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=2, column=0)
    
    def _create_principle_16(self):
        """Create Principle 16: Energy consumption."""
        config = QuestionConfig(
            id=16,
            title='Consumption of energy during analysis',
            question_type='radio',
            choices=[
                RadioChoice('<0.1 kWh per sample', 20, 1.0),
                RadioChoice('0.1-1 kWh per sample', 10, 0.5),
                RadioChoice('>1 kWh per sample', 0, 0.0),
            ]
        )
        self.create_radio_question(self.content_frame, config, row=2, column=1)
    
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
