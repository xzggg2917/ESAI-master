"""
UI Components for ESAI
======================

This module contains reusable UI components:
- Score display widgets
- Validation entry fields
- Radio button groups
- Dialog utilities
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Tuple, Optional, Dict, Any


class ScoreDisplay(tk.Frame):
    """
    Widget for displaying a dimension score with label.
    """
    
    def __init__(self, parent, label: str, font_style: Tuple[str, int] = ("Times New Roman", 12)):
        """
        Initialize the score display widget.
        
        Args:
            parent: Parent widget
            label: Label text
            font_style: Font configuration
        """
        super().__init__(parent, highlightbackground='gray', highlightthickness=1, pady=10.5, padx=5)
        
        self.score_var = tk.DoubleVar(value=0.0)
        
        lbl = tk.Label(self, text=f'{label}:', bd=1, font=font_style)
        lbl.grid(row=0, column=0, sticky="w")
        
        value_lbl = tk.Label(self, textvariable=self.score_var, bd=1, width=3,
                            font=('Times New Roman', 11))
        value_lbl.grid(row=0, column=1, padx=9, sticky="w")
    
    def set_score(self, value: float):
        """Set the displayed score value."""
        self.score_var.set(round(value, 2))
    
    def get_score(self) -> float:
        """Get the current score value."""
        return self.score_var.get()


class ValidationEntry(tk.Entry):
    """
    Entry widget with built-in validation.
    """
    
    def __init__(self, parent, validation_func: Callable[[str], bool] = None,
                 invalid_callback: Callable = None, **kwargs):
        """
        Initialize the validation entry.
        
        Args:
            parent: Parent widget
            validation_func: Function to validate input
            invalid_callback: Callback when validation fails
            **kwargs: Additional Entry widget arguments
        """
        self._validation_func = validation_func or self._default_validation
        self._invalid_callback = invalid_callback
        
        # Register validation
        vcmd = (parent.register(self._validate), '%P')
        icmd = (parent.register(self._on_invalid),)
        
        super().__init__(parent, validate="focusout", validatecommand=vcmd,
                        invalidcommand=icmd, **kwargs)
    
    def _default_validation(self, text: str) -> bool:
        """Default validation: check if text is a valid float."""
        if not text:
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    def _validate(self, text: str) -> bool:
        """Validate the entry content."""
        return self._validation_func(text)
    
    def _on_invalid(self):
        """Handle invalid input."""
        if self._invalid_callback:
            self._invalid_callback()
        else:
            self.delete(0, tk.END)
    
    def get_float(self, default: float = 0.0) -> float:
        """Get the entry value as float."""
        try:
            return float(self.get())
        except ValueError:
            return default


class RadioButtonGroup(tk.Frame):
    """
    Group of radio buttons with callback support.
    """
    
    def __init__(self, parent, options: List[Tuple[str, Any]], 
                 on_select: Callable[[Any], None] = None,
                 font_style: Tuple[str, int] = ('Times New Roman', 10),
                 orientation: str = 'vertical'):
        """
        Initialize the radio button group.
        
        Args:
            parent: Parent widget
            options: List of (label, value) tuples
            on_select: Callback when selection changes
            font_style: Font configuration
            orientation: 'vertical' or 'horizontal'
        """
        super().__init__(parent)
        
        self.selected_var = tk.StringVar(value='0')
        self._on_select = on_select
        self._buttons: List[tk.Radiobutton] = []
        
        for i, (label, value) in enumerate(options):
            btn = tk.Radiobutton(
                self, text=label, variable=self.selected_var,
                value=str(value), activeforeground='green',
                font=font_style, command=self._handle_select
            )
            
            if orientation == 'vertical':
                btn.pack(anchor='w', padx=20)
            else:
                btn.pack(side='left', padx=10)
            
            self._buttons.append(btn)
    
    def _handle_select(self):
        """Handle radio button selection."""
        if self._on_select:
            self._on_select(self.selected_var.get())
    
    def get_selection(self) -> str:
        """Get the current selection value."""
        return self.selected_var.get()
    
    def set_selection(self, value: Any):
        """Set the selection to a specific value."""
        self.selected_var.set(str(value))


class DropdownSelector(tk.Frame):
    """
    Dropdown menu with label.
    """
    
    def __init__(self, parent, label: str, options: List[str],
                 on_change: Callable[[str], None] = None,
                 font_style: Tuple[str, int] = ('Times New Roman', 10)):
        """
        Initialize the dropdown selector.
        
        Args:
            parent: Parent widget
            label: Label text
            options: List of option strings
            on_change: Callback when selection changes
            font_style: Font configuration
        """
        super().__init__(parent)
        
        self.selected_var = tk.StringVar()
        self._on_change = on_change
        
        if label:
            lbl = tk.Label(self, text=label, font=font_style)
            lbl.pack(side='left', padx=5)
        
        self.combo = ttk.Combobox(self, textvariable=self.selected_var,
                                  values=options, state='readonly')
        self.combo.pack(side='left', padx=5)
        
        if options:
            self.combo.current(0)
        
        self.selected_var.trace_add('write', self._handle_change)
    
    def _handle_change(self, *args):
        """Handle selection change."""
        if self._on_change:
            self._on_change(self.selected_var.get())
    
    def get_selection(self) -> str:
        """Get the current selection."""
        return self.selected_var.get()
    
    def set_selection(self, value: str):
        """Set the selection."""
        self.selected_var.set(value)


def create_labeled_frame(parent, label: str, **kwargs) -> tk.LabelFrame:
    """
    Create a labeled frame with standard styling.
    
    Args:
        parent: Parent widget
        label: Frame label text
        **kwargs: Additional LabelFrame arguments
        
    Returns:
        Configured LabelFrame widget
    """
    frame = tk.LabelFrame(parent, text=label, font=('Times New Roman', 11), **kwargs)
    return frame


def show_error_dialog(title: str, message: str, parent: tk.Tk = None):
    """
    Show an error dialog.
    
    Args:
        title: Dialog title
        message: Error message
        parent: Parent window
    """
    messagebox.showerror(title, message, parent=parent)


def show_info_dialog(title: str, message: str, parent: tk.Tk = None):
    """
    Show an information dialog.
    
    Args:
        title: Dialog title
        message: Information message
        parent: Parent window
    """
    messagebox.showinfo(title, message, parent=parent)


def show_warning_dialog(title: str, message: str, parent: tk.Tk = None):
    """
    Show a warning dialog.
    
    Args:
        title: Dialog title
        message: Warning message
        parent: Parent window
    """
    messagebox.showwarning(title, message, parent=parent)


class PopupWindow(tk.Toplevel):
    """
    Base class for popup windows with modern styling.
    """
    
    def __init__(self, parent, title: str, width: int = 380, height: int = 140):
        """
        Initialize the popup window.
        
        Args:
            parent: Parent window
            title: Window title
            width: Window width
            height: Window height
        """
        super().__init__(parent)
        self.title(title)
        
        # Modern styling
        self.configure(bg='#FAFAFA')
        
        # Center the popup
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        
        # Grab focus
        self.grab_set()
        self.focus_set()


class ErrorPopup(PopupWindow):
    """
    Popup window for displaying error messages with modern styling.
    """
    
    def __init__(self, parent, message: str):
        """
        Initialize the error popup.
        
        Args:
            parent: Parent window
            message: Error message to display
        """
        super().__init__(parent, "⚠ Notice", width=400, height=160)
        
        # Main container
        container = tk.Frame(self, bg='#FAFAFA')
        container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icon and message
        icon_label = tk.Label(container, text="⚠", font=('Segoe UI', 24),
                             fg='#FF9800', bg='#FAFAFA')
        icon_label.pack(pady=(0, 5))
        
        msg_label = tk.Label(container, text=message, 
                            font=('Segoe UI', 11),
                            fg='#424242', bg='#FAFAFA',
                            wraplength=350, justify='center')
        msg_label.pack(pady=5)
        
        # OK button
        btn_frame = tk.Frame(container, bg='#FAFAFA')
        btn_frame.pack(pady=(10, 0))
        
        ok_btn = tk.Button(btn_frame, text="OK", command=self.destroy,
                          font=('Segoe UI', 10),
                          bg='#2196F3', fg='white',
                          activebackground='#1976D2',
                          activeforeground='white',
                          relief='flat', cursor='hand2',
                          padx=30, pady=5)
        ok_btn.pack()
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.destroy())


class ToolTip:
    """
    Create a tooltip for a given widget.
    
    Shows helpful information when the user hovers over a widget.
    """
    
    def __init__(self, widget, text: str, delay: int = 500):
        """
        Initialize the tooltip.
        
        Args:
            widget: Widget to attach tooltip to
            text: Tooltip text to display
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.schedule_id = None
        
        # Bind events
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<ButtonPress>", self._on_leave)
    
    def _on_enter(self, event=None):
        """Schedule tooltip display when mouse enters widget."""
        self._cancel_schedule()
        self.schedule_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _on_leave(self, event=None):
        """Hide tooltip when mouse leaves widget."""
        self._cancel_schedule()
        self._hide_tooltip()
    
    def _cancel_schedule(self):
        """Cancel scheduled tooltip display."""
        if self.schedule_id:
            self.widget.after_cancel(self.schedule_id)
            self.schedule_id = None
    
    def _show_tooltip(self):
        """Display the tooltip window."""
        if self.tooltip_window or not self.text:
            return
        
        # Calculate position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Create label with tooltip text
        label = tk.Label(
            tw, text=self.text, justify='left',
            background="#FFFFE0", foreground="#000000",
            relief='solid', borderwidth=1,
            font=('Segoe UI', 9), padx=8, pady=6
        )
        label.pack()
    
    def _hide_tooltip(self):
        """Hide the tooltip window."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class HelpButton(tk.Button):
    """
    Button that displays help information when clicked.
    """
    
    def __init__(self, parent, help_text: str, help_title: str = "Help",
                 **kwargs):
        """
        Initialize the help button.
        
        Args:
            parent: Parent widget
            help_text: Help information to display
            help_title: Title for help dialog
            **kwargs: Additional Button arguments
        """
        self.help_text = help_text
        self.help_title = help_title
        
        # Default styling
        button_kwargs = {
            'text': '?',
            'command': self._show_help,
            'font': ('Segoe UI', 10, 'bold'),
            'bg': '#2196F3',
            'fg': 'white',
            'activebackground': '#1976D2',
            'activeforeground': 'white',
            'relief': 'flat',
            'cursor': 'hand2',
            'width': 2,
            'height': 1
        }
        button_kwargs.update(kwargs)
        
        super().__init__(parent, **button_kwargs)
        
        # Add tooltip
        ToolTip(self, "Click for help information")
    
    def _show_help(self):
        """Display help dialog."""
        HelpDialog(self.winfo_toplevel(), self.help_title, self.help_text)


class HelpDialog(tk.Toplevel):
    """
    Dialog window for displaying help information.
    """
    
    def __init__(self, parent, title: str, message: str):
        """
        Initialize the help dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Help message to display
        """
        super().__init__(parent)
        self.title(title)
        
        # Window configuration
        self.configure(bg='#FAFAFA')
        width = 600
        height = 400
        
        # Center the dialog
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Main container
        container = tk.Frame(self, bg='#FAFAFA')
        container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            container, text=title,
            font=('Segoe UI', 14, 'bold'),
            fg='#1976D2', bg='#FAFAFA'
        )
        title_label.pack(pady=(0, 10))
        
        # Create scrollable text area
        text_frame = tk.Frame(container, bg='#FAFAFA')
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(
            text_frame, wrap='word',
            font=('Segoe UI', 10),
            bg='white', fg='#424242',
            relief='solid', borderwidth=1,
            padx=10, pady=10,
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Insert help text
        text_widget.insert('1.0', message)
        text_widget.config(state='disabled')  # Make read-only
        
        # Close button
        btn_frame = tk.Frame(container, bg='#FAFAFA')
        btn_frame.pack(pady=(10, 0))
        
        close_btn = tk.Button(
            btn_frame, text="Close", command=self.destroy,
            font=('Segoe UI', 10),
            bg='#2196F3', fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief='flat', cursor='hand2',
            padx=30, pady=5
        )
        close_btn.pack()
        
        # Bind Escape key
        self.bind('<Escape>', lambda e: self.destroy())
        
        # Grab focus
        self.grab_set()
        self.focus_set()

