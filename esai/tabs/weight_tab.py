"""
Weight Tab for ESAI
===================

This module contains the weight configuration tab (Set).
"""

import tkinter as tk
from tkinter import Frame, Label, Radiobutton, Entry, Button, StringVar, messagebox
from typing import Callable, Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class WeightPreset:
    """Configuration for a weight preset."""
    name: str
    weights: Dict[str, float]  # w1-w8 values


# Predefined weight configurations
WEIGHT_PRESETS = [
    WeightPreset(
        name="Default_weights: SC (w1) =0.1, SP (w2) =0.2, AT (w3)=0.2, Economy (w4) =0.05, Method\n(w5) =0.05, Safety of operator (w6) =0.1, Reagent (w7) =0.1, Waste (w8) =0.2                 ",
        weights={'w1': 0.1, 'w2': 0.2, 'w3': 0.2, 'w4': 0.05, 'w5': 0.05, 'w6': 0.1, 'w7': 0.1, 'w8': 0.2}
    ),
    WeightPreset(
        name="w1=0.2, w2=0.2, w3=0.1, w4=0.05, w5=0.05, w6=0.05, w7=0.15, w8=0.2",
        weights={'w1': 0.2, 'w2': 0.2, 'w3': 0.1, 'w4': 0.05, 'w5': 0.05, 'w6': 0.05, 'w7': 0.15, 'w8': 0.2}
    ),
    WeightPreset(
        name="w1=0.2, w2=0.2, w3=0.2, w4=0.05, w5=0.05, w6=0.05, w7=0.05, w8=0.2",
        weights={'w1': 0.2, 'w2': 0.2, 'w3': 0.2, 'w4': 0.05, 'w5': 0.05, 'w6': 0.05, 'w7': 0.05, 'w8': 0.2}
    ),
    WeightPreset(
        name="w1=0.1, w2=0.2, w3=0.1, w4=0.1, w5=0.1, w6=0.1, w7=0.1, w8=0.2",
        weights={'w1': 0.1, 'w2': 0.2, 'w3': 0.1, 'w4': 0.1, 'w5': 0.1, 'w6': 0.1, 'w7': 0.1, 'w8': 0.2}
    ),
    WeightPreset(
        name="w1=0.2, w2=0.2, w3=0.05, w4=0.05, w5=0.05, w6=0.05, w7=0.2, w8=0.2",
        weights={'w1': 0.2, 'w2': 0.2, 'w3': 0.05, 'w4': 0.05, 'w5': 0.05, 'w6': 0.05, 'w7': 0.2, 'w8': 0.2}
    ),
    WeightPreset(
        name="w1=0.2, w2=0.2, w3=0.2, w4=0.05, w5=0.05, w6=0.05, w7=0.2, w8=0.05",
        weights={'w1': 0.2, 'w2': 0.2, 'w3': 0.2, 'w4': 0.05, 'w5': 0.05, 'w6': 0.05, 'w7': 0.2, 'w8': 0.05}
    ),
    WeightPreset(
        name="w1=0.2, w2=0.2, w3=0.2, w4=0.1, w5=0.05, w6=0.1, w7=0.1, w8=0.05",
        weights={'w1': 0.2, 'w2': 0.2, 'w3': 0.2, 'w4': 0.1, 'w5': 0.05, 'w6': 0.1, 'w7': 0.1, 'w8': 0.05}
    ),
]


class WeightTab(Frame):
    """
    Tab for configuring dimension weights.
    """
    
    # Weight labels matching dimensions
    WEIGHT_LABELS = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8']
    
    def __init__(self, parent, notebook, on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        """
        Initialize the weight tab.
        
        Args:
            parent: Parent widget
            notebook: Notebook to add tab to
            on_update: Callback when weights change
            font_style: Font configuration
            theme: Theme configuration
        """
        super().__init__(parent)
        self.notebook = notebook
        self.on_update = on_update
        self.theme = theme
        
        # Apply theme
        if theme:
            self.configure(bg=theme.colors.bg_main)
            self.font_style = theme.fonts.body
            self.small_font = theme.fonts.small
            self.title_font = theme.fonts.heading
        else:
            self.font_style = font_style
            self.small_font = ('Segoe UI', 10)
            self.title_font = ('Segoe UI', 12, 'bold')
        
        # Current weights
        self.weights = {
            'w1': 0.1,  # SC
            'w2': 0.2,  # SP
            'w3': 0.2,  # AT
            'w4': 0.05, # Economy
            'w5': 0.05, # Method
            'w6': 0.1,  # Operator
            'w7': 0.1,  # Reagent
            'w8': 0.2,  # Waste
        }
        
        # Entry widgets
        self.entries: Dict[str, Entry] = {}
        
        # Selected preset
        self.selected_preset = StringVar(value='0')
        
        # Add to notebook
        notebook.add(self, text=' ⚙ Settings ')
        
        # Setup content
        self._setup_content()
    
    def _setup_content(self):
        """Setup the tab content."""
        bg_color = self.theme.colors.bg_main if self.theme else None
        
        # Title with modern style
        if self.theme:
            title_label = Label(
                self,
                text='📊 Select Weight Configuration',
                font=self.title_font,
                fg=self.theme.colors.primary_dark,
                bg=bg_color
            )
        else:
            title_label = Label(
                self,
                text='Please select the appropriate weights',
                font=self.font_style
            )
        title_label.pack(pady=(10, 5))
        
        # Preset radio buttons
        self._create_preset_options()
        
        # Manual entry section
        self._create_manual_entry()
    
    def _create_preset_options(self):
        """Create preset weight radio buttons."""
        bg_color = self.theme.colors.bg_main if self.theme else None
        
        for i, preset in enumerate(WEIGHT_PRESETS):
            if self.theme:
                btn = Radiobutton(
                    self, text=preset.name,
                    variable=self.selected_preset,
                    value=str(i + 1),
                    font=self.small_font,
                    bg=bg_color,
                    selectcolor=self.theme.colors.bg_card,
                    highlightthickness=0,
                    anchor='w',
                    cursor='hand2',
                    takefocus=0
                )
            else:
                if i == 0:
                    btn = Radiobutton(
                        self, text=preset.name,
                        variable=self.selected_preset,
                        value=str(i + 1),
                        activeforeground='green',
                        font=self.small_font,
                        anchor='w',
                        cursor='hand2',
                        takefocus=0
                    )
                else:
                    btn = Radiobutton(
                        self, text=preset.name,
                        variable=self.selected_preset,
                        value=str(i + 1),
                        activeforeground='green',
                        font=self.small_font,
                        cursor='hand2',
                        takefocus=0
                    )
            
            btn.config(command=lambda p=preset: self._apply_preset(p))
            btn.pack(anchor='w', padx=15, pady=1)
    
    def _apply_preset(self, preset: WeightPreset):
        """Apply a weight preset."""
        self.weights.update(preset.weights)
        self._trigger_update()
    
    def _create_manual_entry(self):
        """Create manual weight entry section."""
        bg_color = self.theme.colors.bg_main if self.theme else None
        
        input_frame = Frame(self, bg=bg_color) if bg_color else Frame(self)
        input_frame.pack(pady=10)
        
        # Instructions with styled appearance
        if self.theme:
            Label(
                input_frame,
                text="Custom weights (sum must equal 1.0):",
                font=self.small_font,
                fg=self.theme.colors.text_secondary,
                bg=bg_color
            ).grid(row=0, column=0, columnspan=8, pady=(10, 5))
        else:
            Label(
                input_frame,
                text="If no suitable weights found above,\n"
                     "please enter them below. \n"
                     "Make sure all the weights sum to 1.",
                bd=1, font=self.font_style
            ).grid(row=0, column=0, columnspan=8, pady=10)
        
        # Weight entry fields with better styling
        def validate_entry_text(text):
            if not text:
                return True
            try:
                float(text)
                return True
            except ValueError:
                return False
        
        validation = self.register(validate_entry_text)
        
        for i, label in enumerate(self.WEIGHT_LABELS):
            if self.theme:
                lbl = Label(input_frame, text=label, width=5, font=self.small_font, bg=bg_color)
            else:
                lbl = Label(input_frame, text=label, width=5, font=self.small_font)
            lbl.grid(row=1, column=i, padx=2)
            
            entry = Entry(input_frame, validate="focusout",
                         validatecommand=(validation, "%P"),
                         justify='center', width=6,
                         relief='solid', borderwidth=1)
            entry.grid(row=2, column=i, padx=2, pady=2)
            self.entries[label] = entry
        
        # Update button with modern styling
        if self.theme:
            update_btn = Button(
                input_frame, text="✓ Apply Weights",
                command=self._handle_manual_update,
                font=self.small_font,
                bg=self.theme.colors.primary,
                fg=self.theme.colors.text_light,
                activebackground=self.theme.colors.primary_dark,
                activeforeground=self.theme.colors.text_light,
                relief='flat', cursor='hand2',
                padx=15, pady=5
            )
        else:
            update_btn = Button(
                input_frame, text="Update weight",
                command=self._handle_manual_update,
                font=self.small_font
            )
        update_btn.grid(row=4, column=0, columnspan=8, pady=10)
    
    def _handle_manual_update(self):
        """Handle manual weight entry."""
        # Collect values
        values = {}
        for label, entry in self.entries.items():
            text = entry.get()
            if not text:
                self._show_omissions_error()
                return
            try:
                value = float(text)
                # Check for negative values
                if value < 0:
                    messagebox.showwarning(
                        "Invalid Input",
                        f"Weight {label} cannot be negative.\nPlease enter a value greater than 0."
                    )
                    return
                values[label] = value
            except ValueError:
                self._show_omissions_error()
                return
        
        # Check sum
        total = sum(values.values())
        if round(total, 2) != 1.0:
            self._show_sum_error()
            return
        
        # Apply
        self.weights.update(values)
        self._trigger_update()
    
    def _show_sum_error(self):
        """Show error for invalid weight sum."""
        from esai.ui.components import ErrorPopup
        ErrorPopup(self, "Please re-enter the weight values\nfor each module if the weight sum is not 1.")
    
    def _show_omissions_error(self):
        """Show error for missing weights."""
        from esai.ui.components import ErrorPopup
        ErrorPopup(self, "Please make sure that the weights \nfor each module have been entered!")
    
    def _trigger_update(self):
        """Trigger the update callback."""
        if self.on_update:
            self.on_update()
    
    def get_weights(self) -> Dict[str, float]:
        """Get current weight values."""
        return self.weights.copy()
    
    def get_weight(self, label: str) -> float:
        """Get a specific weight value."""
        return self.weights.get(label, 0.0)
