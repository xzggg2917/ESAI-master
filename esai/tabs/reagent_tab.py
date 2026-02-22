"""
Reagent Tab for ESAI
====================

This module contains the Reagent assessment tab.
Principles 21-25 belong to this dimension.
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, Entry, Button, StringVar, DoubleVar, messagebox
from tkinter import ttk
from typing import Callable, Tuple
import numpy as np

from esai.tabs.base_tab import BaseTab


class ReagentTab(BaseTab):
    """
    Reagent assessment tab.
    
    Contains 5 principles:
    21. Number of types of reagents used
    22. Amounts of reagents used during analytical procedures
    23. Toxicity of reagents
    24. Dosage of toxic reagents
    25. Sustainable and renewable reagents
    """
    
    PRINCIPLES = [21, 22, 23, 24, 25]
    
    def __init__(self, parent, notebook: ttk.Notebook,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        super().__init__(parent, notebook, ' Reagent ', on_update, font_style, theme)
    
    def _setup_content(self):
        """Setup the Reagent tab content."""
        self._create_principle_21()
        self._create_principle_22()
        self._create_principle_23()
        self._create_principle_24()
        self._create_principle_25()
    
    def _create_principle_21(self):
        """Create Principle 21: Number of types of reagents."""
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
            badge_label = Label(badge_frame, text="Q21", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = 'Number of types of reagents used in analysis process'
        if self.theme:
            title_label = Label(card, text=title_text, 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='21. ' + title_text, 
                              font=self.font_style,
                              bg=bg_card,
                              wraplength=280)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(21, '>6')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('>6', 0, 0.0),
            ('3-6', 5, 0.5),
            ('<3', 10, 1.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[21],
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
                    variable=self.selected_vars[21],
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
                    self.scores[21].set(s)
                    self.colors[21].set(c)
                    self.pdf_texts[21].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=0, column=0, sticky='new', pady=5, padx=5)
    
    def _create_principle_22(self):
        """Create Principle 22: Amount of reagents."""
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
            badge_label = Label(badge_frame, text="Q22", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = 'The amounts of reagents used during analytical procedures (mL)'
        if self.theme:
            title_label = Label(card, text=title_text, 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='22. ' + title_text, 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(22, '0 mL')
        
        # Input area
        input_frame = Frame(card, bg=bg_card)
        input_frame.pack(fill='x', pady=(5, 5))
        
        # Entry field with placeholder
        placeholder_text = 'Unit: mL'
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
            
            self.pdf_texts[22].set(f'{value} mL')
            
            if value > 10:
                self.scores[22].set(0.0)
                self.colors[22].set(0.0)
            elif value < 1:
                self.colors[22].set(1.0)
                self.scores[22].set(10.0)
            else:  # 1 <= value <= 10
                calc_value = -1/9 * value + 10/9
                if calc_value < 0:
                    self.colors[22].set(0.0)
                    self.scores[22].set(0.0)
                else:
                    self.colors[22].set(round(calc_value, 2))
                    self.scores[22].set(round(calc_value, 2) * 10)
            
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
        
        card.grid(row=0, column=1, sticky='new', pady=5, padx=5)
    
    def _create_principle_23(self):
        """Create Principle 23: Toxicity of reagents."""
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
            badge_label = Label(badge_frame, text="Q23", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Toxicity of reagents', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=500,
                              justify='left')
        else:
            title_label = Label(card, text='23. Toxicity of reagents', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(23, 'Chronic toxicity')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('Non-toxic', 30, 1.0),
            ('Chronic toxicity: (e.g. carcinogenicity, neurotoxicity, teratogenicity, and reproductive toxicity associated with the reagent)', 15, 0.5),
            ('Acute toxicity: (e.g. irritation and corrosiveness to the eyes, skin, and respiratory tract)', 0, 0.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[23],
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
                    variable=self.selected_vars[23],
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
                    self.scores[23].set(s)
                    self.colors[23].set(c)
                    self.pdf_texts[23].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=1, column=0, sticky='new', pady=5, padx=5, columnspan=2)
    
    def _create_principle_24(self):
        """Create Principle 24: Dosage of toxic reagents."""
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
            badge_label = Label(badge_frame, text="Q24", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = 'Enter the dosage of toxic reagents (mg or µL)'
        if self.theme:
            title_label = Label(card, text=title_text, 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='24. ' + title_text, 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(24, '0 mg/µL')
        
        # Input area
        input_frame = Frame(card, bg=bg_card)
        input_frame.pack(fill='x', pady=(5, 5))
        
        # Entry field with placeholder
        placeholder_text = 'Unit: mg or µL'
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
            
            self.pdf_texts[24].set(f'{value} mg/µL')
            
            if value > 100000:
                self.scores[24].set(0.0)
                self.colors[24].set(0.0)
            elif value < 10:
                self.colors[24].set(1.0)
                self.scores[24].set(20.0)
            else:  # 10 <= value <= 100000
                color = round(np.log(1/value) * 0.217 + 2.5, 2) / 2
                score = round(np.log(1/value) * 0.217 + 2.5, 2) * 10
                self.colors[24].set(color)
                self.scores[24].set(score)
            
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
        
        card.grid(row=2, column=0, sticky='new', pady=5, padx=5)
    
    def _create_principle_25(self):
        """Create Principle 25: Sustainable and renewable reagents."""
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
            badge_label = Label(badge_frame, text="Q25", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        if self.theme:
            title_label = Label(card, text='Sustainable and renewable reagents', 
                              font=self.title_font,
                              fg=self.theme.colors.text_primary,
                              bg=bg_card,
                              wraplength=280,
                              justify='left')
        else:
            title_label = Label(card, text='25. Sustainable and renewable reagents', 
                              font=self.font_style,
                              bg=bg_card)
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(25, '0-25%')
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        choices = [
            ('75-100%', 30, 1.0),
            ('50-75%', 15, 0.66),
            ('25-50%', 10, 0.33),
            ('0-25%', 0, 0.0),
        ]
        
        for i, (text, score, color) in enumerate(choices):
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=text,
                    variable=self.selected_vars[25],
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
                    variable=self.selected_vars[25],
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
                    self.scores[25].set(s)
                    self.colors[25].set(c)
                    self.pdf_texts[25].set(t)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
        
        card.grid(row=2, column=1, sticky='new', pady=5, padx=5)
    
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
