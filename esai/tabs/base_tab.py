"""
Base Tab Class for ESAI
=======================

This module provides the base class for all assessment tabs.
"""

import tkinter as tk
from tkinter import ttk, Frame, Label, Text, Radiobutton, Entry, Button, StringVar, DoubleVar, messagebox
from typing import Callable, List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
import numpy as np

# Import UI components
try:
    from esai.ui.components import ToolTip, HelpButton
except ImportError:
    # Fallback if components not available
    ToolTip = None
    HelpButton = None


@dataclass
class RadioChoice:
    """Configuration for a radio button choice."""
    text: str
    raw_score: float
    color_value: float
    pdf_text: str = ""
    
    def __post_init__(self):
        if not self.pdf_text:
            self.pdf_text = self.text


@dataclass
class QuestionConfig:
    """Configuration for a question in a tab."""
    id: int  # Principle ID (1-27)
    title: str
    question_type: str = "radio"  # "radio", "entry", "calculated"
    choices: List[RadioChoice] = field(default_factory=list)
    entry_unit: str = ""
    entry_default: str = ""
    max_score: float = 20.0
    # For calculated/entry types
    calculate_score: Callable[[float], Tuple[float, float]] = None


class BaseTab(Frame):
    """
    Base class for all assessment tabs.
    
    Provides common functionality for creating questions,
    handling user input, and calculating scores.
    """
    
    def __init__(self, parent, notebook: ttk.Notebook, tab_name: str,
                 on_update: Callable = None,
                 font_style: Tuple[str, int] = ('Segoe UI', 11),
                 theme=None):
        """
        Initialize the base tab.
        
        Args:
            parent: Parent widget
            notebook: Notebook widget to add tab to
            tab_name: Display name for the tab
            on_update: Callback when scores change
            font_style: Font configuration
            theme: Theme configuration (optional)
        """
        super().__init__(parent)
        self.notebook = notebook
        self.tab_name = tab_name
        self.on_update = on_update
        self.font_style = font_style
        self.theme = theme
        
        # Font styles
        if theme:
            self.font_style = theme.fonts.body
            self.small_font = theme.fonts.small
            self.title_font = theme.fonts.heading
            self.bg_color = theme.colors.bg_main
            self.configure(bg=theme.colors.bg_main)
        else:
            self.small_font = ('Segoe UI', 10)
            self.title_font = ('Segoe UI', 12, 'bold')
            self.bg_color = None
        
        # Score storage
        self.scores: Dict[int, DoubleVar] = {}  # principle_id -> raw score (0-max)
        self.colors: Dict[int, DoubleVar] = {}  # principle_id -> color value (0-1)
        self.pdf_texts: Dict[int, StringVar] = {}  # principle_id -> PDF display text
        self.selected_vars: Dict[int, StringVar] = {}  # principle_id -> selected radio value
        
        # Create scrollable content area
        self._create_scrollable_frame()
        
        # Add to notebook
        notebook.add(self, text=tab_name)
        
        # Setup the tab content
        self._setup_content()
    
    def _create_scrollable_frame(self):
        """Create a scrollable frame for tab content."""
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        if self.bg_color:
            self.canvas.configure(bg=self.bg_color)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create content frame inside canvas
        self.content_frame = Frame(self.canvas)
        if self.bg_color:
            self.content_frame.configure(bg=self.bg_color)
        
        # Configure grid columns to have equal weight for better layout
        self.content_frame.columnconfigure(0, weight=1, uniform='col')
        self.content_frame.columnconfigure(1, weight=1, uniform='col')
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Bind events
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Enable mouse wheel scrolling when mouse is over the canvas
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
    
    def _bind_mousewheel(self, event):
        """Bind mouse wheel when entering canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        """Unbind mouse wheel when leaving canvas."""
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_frame_configure(self, event):
        """Update scroll region when content changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Resize content frame when canvas resizes."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _setup_content(self):
        """
        Setup the tab content. Override in subclasses.
        """
        pass
    
    def get_score(self, principle_id: int) -> float:
        """Get the raw score for a principle."""
        if principle_id in self.scores:
            return self.scores[principle_id].get()
        return 0.0
    
    def get_color(self, principle_id: int) -> float:
        """Get the color value (0-1) for a principle."""
        if principle_id in self.colors:
            return self.colors[principle_id].get()
        return 0.0
    
    def get_pdf_text(self, principle_id: int) -> str:
        """Get the PDF display text for a principle."""
        if principle_id in self.pdf_texts:
            return self.pdf_texts[principle_id].get()
        return ""
    
    def _trigger_update(self):
        """Trigger the update callback."""
        if self.on_update:
            self.on_update()
    
    def _init_score_vars(self, principle_id: int, default_pdf_text: str = ""):
        """Initialize score variables for a principle."""
        self.scores[principle_id] = DoubleVar(value=0.0)
        self.colors[principle_id] = DoubleVar(value=0.0)
        self.pdf_texts[principle_id] = StringVar(value=default_pdf_text)
        self.selected_vars[principle_id] = StringVar(value='0')
    
    def create_radio_question(self, parent: Frame, config: QuestionConfig,
                              row: int = 0, column: int = 0) -> Frame:
        """
        Create a radio button question with card-style layout.
        
        Args:
            parent: Parent frame
            config: Question configuration
            row: Grid row
            column: Grid column
            
        Returns:
            The question frame
        """
        # Get theme colors
        if self.theme:
            bg_card = self.theme.colors.bg_card
            bg_main = self.theme.colors.bg_main
            border_color = self.theme.colors.border
        else:
            bg_card = 'white'
            bg_main = None
            border_color = '#E0E0E0'
        
        # Card container
        card = Frame(parent, bg=bg_card, 
                    highlightbackground=border_color,
                    highlightthickness=1,
                    padx=10, pady=10)
        
        # Question number badge
        if self.theme:
            badge_frame = Frame(card, bg=self.theme.colors.primary, padx=8, pady=3)
            badge_label = Label(badge_frame, text=f"Q{config.id}", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = config.title
        if self.theme:
            title_label = Text(card,
                             font=self.title_font,
                             fg=self.theme.colors.text_primary,
                             bg=bg_card,
                             height=2,
                             wrap='word',
                             relief='flat',
                             highlightthickness=0,
                             cursor='arrow')
        else:
            title_label = Text(card,
                             font=self.font_style,
                             bg=bg_card,
                             height=2,
                             wrap='word',
                             relief='flat',
                             highlightthickness=0,
                             cursor='arrow')
        title_label.insert('1.0', title_text)
        title_label.config(state='disabled')
        title_label.pack(fill='x', pady=(0, 10))
        
        # Initialize variables
        default_pdf = config.choices[0].pdf_text if config.choices else ""
        self._init_score_vars(config.id, default_pdf)
        
        # Options container
        options_frame = Frame(card, bg=bg_card)
        options_frame.pack(fill='x', pady=(5, 0))
        
        # Create radio buttons
        buttons = []
        for i, choice in enumerate(config.choices):
            # Option row container
            option_row = Frame(options_frame, bg=bg_card)
            option_row.pack(fill='x', pady=1)
            
            if self.theme:
                btn = Radiobutton(
                    option_row, text=choice.text,
                    variable=self.selected_vars[config.id],
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
                    option_row, text=choice.text,
                    variable=self.selected_vars[config.id],
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
            
            # Create callback for this choice
            def make_callback(c=choice, pid=config.id):
                def callback():
                    self.scores[pid].set(c.raw_score)
                    self.colors[pid].set(c.color_value)
                    self.pdf_texts[pid].set(c.pdf_text)
                    self._trigger_update()
                return callback
            
            btn.config(command=make_callback())
            buttons.append(btn)
        
        card.grid(row=row, column=column, sticky='ew', pady=5, padx=5)
        return card
    
    def create_entry_question(self, parent: Frame, config: QuestionConfig,
                              row: int = 0, column: int = 0,
                              calculate_func: Callable[[float], Tuple[float, float]] = None) -> Frame:
        """
        Create an entry field question with card-style layout.
        
        Args:
            parent: Parent frame
            config: Question configuration
            row: Grid row
            column: Grid column
            calculate_func: Function to calculate (score, color) from input value
            
        Returns:
            The question frame
        """
        # Get theme colors
        if self.theme:
            bg_card = self.theme.colors.bg_card
            border_color = self.theme.colors.border
        else:
            bg_card = 'white'
            border_color = '#E0E0E0'
        
        # Card container
        card = Frame(parent, bg=bg_card,
                    highlightbackground=border_color,
                    highlightthickness=1,
                    padx=10, pady=10)
        
        # Question number badge
        if self.theme:
            badge_frame = Frame(card, bg=self.theme.colors.primary, padx=8, pady=3)
            badge_label = Label(badge_frame, text=f"Q{config.id}", 
                              font=(self.theme.fonts.family, 9, 'bold'),
                              bg=self.theme.colors.primary,
                              fg=self.theme.colors.text_light)
            badge_label.pack()
            badge_frame.pack(anchor='w', pady=(0, 5))
        
        # Title
        title_text = config.title
        if self.theme:
            label = Text(card,
                       font=self.title_font,
                       fg=self.theme.colors.text_primary,
                       bg=bg_card,
                       height=2,
                       wrap='word',
                       relief='flat',
                       highlightthickness=0,
                       cursor='arrow')
        else:
            label = Text(card,
                       font=self.font_style,
                       bg=bg_card,
                       height=2,
                       wrap='word',
                       relief='flat',
                       highlightthickness=0,
                       cursor='arrow')
        label.insert('1.0', title_text)
        label.config(state='disabled')
        label.pack(fill='x', pady=(0, 10))
        
        # Initialize variables
        self._init_score_vars(config.id, config.entry_default)
        
        # Input area
        input_frame = Frame(card, bg=bg_card)
        input_frame.pack(fill='x', pady=(5, 5))
        
        # Entry field with modern styling and placeholder
        placeholder_text = f"Unit: {config.entry_unit}" if hasattr(config, 'entry_unit') and config.entry_unit else ""
        entry_var = StringVar(value=config.entry_default or "")
        
        def validate_entry_text(text):
            if not text:  # Allow empty
                return True
            try:
                float(text)
                return True
            except ValueError:
                return False
        
        validation = parent.register(validate_entry_text)
        
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
        if placeholder_text:
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
            
            # Set initial placeholder if empty
            if not entry_var.get():
                entry_var.set(placeholder_text)
                entry.config(fg=placeholder_color)
        
        # Calculate button with modern styling
        def handle_value():
            text = entry_var.get()
            # Ignore placeholder text
            if text == placeholder_text:
                text = ''
            if not text:
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
            
            if calculate_func:
                score, color = calculate_func(value)
                self.scores[config.id].set(score)
                self.colors[config.id].set(color)
                if hasattr(config, 'entry_unit'):
                    self.pdf_texts[config.id].set(f"{value} {config.entry_unit}")
                else:
                    self.pdf_texts[config.id].set(str(value))
            
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
        
        card.grid(row=row, column=column, sticky='ew', pady=5, padx=5)
        return card


class ScorePanel(Frame):
    """
    Panel for displaying dimension scores.
    """
    
    def __init__(self, parent, dimension_names: List[str],
                 font_style: Tuple[str, int] = ('Times New Roman', 12)):
        """
        Initialize the score panel.
        
        Args:
            parent: Parent widget
            dimension_names: List of dimension names
            font_style: Font configuration
        """
        super().__init__(parent, highlightbackground="grey", highlightthickness=1)
        
        self.font_style = font_style
        self.score_vars: Dict[str, DoubleVar] = {}
        self.total_var = DoubleVar(value=0.0)
        
        self._setup_ui(dimension_names)
    
    def _setup_ui(self, dimension_names: List[str]):
        """Setup the score panel UI."""
        # Total score
        total_frame = Frame(self, highlightbackground="grey", highlightthickness=1.5, padx=5, pady=10)
        Label(total_frame, text='Total:', bd=1, font=self.font_style).grid(row=0, column=0)
        total_frame.grid(row=0, column=0, sticky="w")
        
        total_value_lbl = Label(self, textvariable=self.total_var, bd=1,
                               font=('Times New Roman', 11),
                               highlightbackground="grey", highlightthickness=1.5,
                               padx=7, pady=12)
        total_value_lbl.grid(row=1, column=0, sticky="we")
        
        # Dimension scores
        row = 0
        col = 1
        for name in dimension_names:
            self.score_vars[name] = DoubleVar(value=0.0)
            
            frame = Frame(self, highlightbackground='gray', highlightthickness=1, pady=10.5, padx=5)
            Label(frame, text=f'{name}:', bd=1, font=self.font_style).grid(row=0, column=0, sticky="w")
            Label(frame, textvariable=self.score_vars[name], bd=1, width=3,
                 font=('Times New Roman', 11)).grid(row=0, column=1, padx=9, sticky="w")
            
            frame.grid(row=row, column=col, sticky="we")
            
            col += 1
            if col > 4:
                col = 1
                row += 1
    
    def set_score(self, dimension: str, value: float):
        """Set a dimension score."""
        if dimension in self.score_vars:
            self.score_vars[dimension].set(round(value, 2))
    
    def set_total(self, value: float):
        """Set the total score."""
        self.total_var.set(round(value, 2))
