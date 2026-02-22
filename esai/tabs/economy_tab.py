"""
Economy Tab for ESAI
====================

This module contains the Economy assessment tab.
Principle 17 belongs to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Entry, Button, StringVar, DoubleVar, messagebox
from tkinter import ttk
from typing import Callable, Tuple

from esai.tabs.base_tab import BaseTab


class EconomyTab(BaseTab):
    """
    Economy assessment tab.
    
    Contains 1 principle:
    17. The cost of analysis for each sample
    """
    
    PRINCIPLES = [17]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' Economy ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Economy tab content."""
        self._create_principle_17()
    
    def _create_principle_17(self):
        """Create Principle 17: Cost of analysis."""
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
            badge_label = Label(badge_frame, text="Q17", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = 'The cost of analysis for each sample'
        if self.theme:
            title_label = Label(card, text=title_text, 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        else:
            title_label = Label(card, text='17. ' + title_text, 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(17, '0 yuan')
        
        # Input area
        input_frame = Frame(card, bg=bg_card)
        input_frame.pack(fill='x', pady=(5, 5))
        
        # Entry field with placeholder
        placeholder_text = 'Unit: USD'
        entry_var = StringVar(value="")
        
        def validate_entry_text(text):
            if not text:
                return True
            try:
                float(text)
                return True
            except ValueError:
                return False
        
        validation = self.register(validate_entry_text)
        
        entry_row = Frame(input_frame, bg=bg_card)
        entry_row.pack(fill='x', padx=5)
        
        if self.theme:
            entry = Entry(entry_row, textvariable=entry_var, validate="key",
                         validatecommand=(validation, "%P"),
                         justify='center', font=self.small_font,
                         bg=bg_card,
                         fg=self.theme.colors.text_primary,
                         relief='solid', borderwidth=1,
                         highlightbackground=self.theme.colors.border,
                         highlightcolor=self.theme.colors.primary,
                         highlightthickness=1,
                         width=20)
        else:
            entry = Entry(entry_row, textvariable=entry_var, validate="key",
                         validatecommand=(validation, "%P"),
                         justify='center', font=self.small_font, width=20)
        entry.pack(pady=5)
        
        # Add placeholder functionality
        placeholder_color = self.theme.colors.text_secondary if self.theme else 'gray'
        normal_color = self.theme.colors.text_primary if self.theme else 'black'
        
        def on_focus_in(event):
            if entry_var.get() == placeholder_text:
                entry_var.set('')
                entry.config(fg=normal_color)
        
        def on_focus_out(event):
            if entry_var.get() == '':
                entry_var.set(placeholder_text)
                entry.config(fg=placeholder_color)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Set initial placeholder
        if not entry_var.get():
            entry_var.set(placeholder_text)
            entry.config(fg=placeholder_color)
        
        def handle_value():
            text = entry_var.get()
            # Ignore placeholder text
            if text == placeholder_text:
                text = ''
            if text == '':
                value = 0
            else:
                try:
                    value = float(text)
                except ValueError:
                    value = 0
            
            # Check for negative values
            if value < 0:
                messagebox.showwarning(
                    "Invalid Input",
                    "Please enter a value greater than 0.\nThe value has been reset to 0."
                )
                value = 0
                entry_var.set('0')
            
            self.pdf_texts[17].set(f'{value} RMB')
            
            if value > 1000:
                self.scores[17].set(0.0)
                self.colors[17].set(0.0)
            elif value < 10:
                self.colors[17].set(1.0)
                self.scores[17].set(100.0)
            else:  # 10 <= value <= 1000
                calc_value = -1/99 * value + 1000/99
                if calc_value < 0:
                    self.colors[17].set(0.0)
                    self.scores[17].set(0.0)
                else:
                    self.colors[17].set(round(calc_value, 2) / 10)
                    self.scores[17].set(round(round(calc_value, 2) * 10, 2))
            
            self._trigger_update()
        
        if self.theme:
            button = Button(card, text="✓ Confirm", command=handle_value, 
                           font=self.small_font,
                           bg=self.theme.colors.primary,
                           fg=self.theme.colors.text_light,
                           activebackground=self.theme.colors.primary_dark,
                           activeforeground=self.theme.colors.text_light,
                           relief='flat', cursor='hand2',
                           borderwidth=0,
                           highlightthickness=0,
                           padx=20, pady=5)
        else:
            button = Button(card, text="Confirm", command=handle_value, font=self.small_font)
        button.pack(pady=(5, 0))
        
        # Add Enter key binding
        entry.bind('<Return>', lambda e: handle_value())
        
        card.grid(row=0, column=0, sticky='new', pady=5, padx=5, columnspan=2)
    
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
