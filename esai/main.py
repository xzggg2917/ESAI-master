"""
ESAI Main Application Entry Point
=================================

Environmental Suitability Assessment Index (ESAI) Application

This is the main entry point for the refactored ESAI application.
It assembles all modules together to create the complete GUI application.
"""

import tkinter as tk
from tkinter import ttk, Frame, Label, Button, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
from matplotlib.patches import Circle, Polygon
import numpy as np
from typing import Dict, Optional
import os
import sys
import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# Import ESAI modules
from esai.config import (
    AppConfig, configure_locale, configure_matplotlib_fonts,
    get_resource_path
)
from esai.scoring import ScoreCalculator
from esai.visualization import RadarChartSimple, ColorbarGenerator
from esai.report import PDFReporter
from esai.ui.styles import THEME, TAB_NAMES
from esai.ui.components import ToolTip, HelpButton
from esai.tabs.weight_tab import WeightTab
from esai.tabs.sc_tab import SCTab
from esai.tabs.sp_tab import SPTab
from esai.tabs.at_tab import ATTab
from esai.tabs.economy_tab import EconomyTab
from esai.tabs.method_tab import MethodTab
from esai.tabs.operator_tab import OperatorTab
from esai.tabs.reagent_tab import ReagentTab
from esai.tabs.waste_tab import WasteTab


class ESAIApplication:
    """
    Main ESAI Application class.
    
    Coordinates all the modules and manages the main window.
    """
    
    def __init__(self):
        """Initialize the ESAI application."""
        # Configure environment
        configure_locale()
        configure_matplotlib_fonts()
        
        # Load configuration
        self.config = AppConfig()
        self.theme = THEME
        
        # Initialize main window
        self._init_window()
        
        # Show splash screen
        self._show_splash()
        
        # Initialize components
        self.calculator = ScoreCalculator(self.colormap)
        
        # Setup UI
        self._setup_ui()
    
    def _init_window(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        
        # Apply modern theme
        self.theme.apply_to_root(self.root)
        
        self.root.title("ESAI - Environmental Suitability Assessment Index")
        
        # Set window size and position (larger for better layout)
        window_width = 1450
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1350, 700)
        
        # Set icon (use both methods for better compatibility)
        try:
            icon_path = get_resource_path("logo.ico")
            # Method 1: iconbitmap for file icon
            self.root.iconbitmap(icon_path)
            # Method 2: iconphoto for window icon (more reliable on some Windows versions)
            icon_img = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, icon_photo)
            # Keep reference to prevent garbage collection
            self.root._icon_photo = icon_photo
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
        
        # Hide main window initially (will show after splash)
        self.root.withdraw()
        
        # Initialize colormap
        self._init_colormap()
    
    def _init_colormap(self):
        """Initialize the color map for visualization."""
        colors = self.config.colors
        start_rgb = self._hex_to_rgb(colors.start_color_hex)
        end_rgb = self._hex_to_rgb(colors.end_color_hex)
        
        cdict = {
            'red': ((0.0, start_rgb[0], start_rgb[0]),
                    (0.5, 1.0, 1.0),
                    (1.0, end_rgb[0], end_rgb[0])),
            'green': ((0.0, start_rgb[1], start_rgb[1]),
                      (0.5, 1.0, 1.0),
                      (1.0, end_rgb[1], end_rgb[1])),
            'blue': ((0.0, start_rgb[2], start_rgb[2]),
                     (0.5, 1.0, 1.0),
                     (1.0, end_rgb[2], end_rgb[2])),
        }
        self.colormap = mcolors.LinearSegmentedColormap('ESAI', cdict)
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to normalized RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
    
    def _show_splash(self):
        """Show the splash screen."""
        try:
            splash_path = get_resource_path("rj.png")
            
            splash = tk.Toplevel(self.root)
            splash.overrideredirect(True)
            splash.configure(bg='white')
            
            # Load image
            img = Image.open(splash_path)
            
            # Get screen dimensions
            screen_width = splash.winfo_screenwidth()
            screen_height = splash.winfo_screenheight()
            
            # Calculate max size (80% of screen to leave margins)
            max_width = int(screen_width * 0.8)
            max_height = int(screen_height * 0.8)
            
            # Get original image dimensions
            img_width, img_height = img.size
            
            # Calculate scaling to fit screen while maintaining aspect ratio
            width_ratio = max_width / img_width
            height_ratio = max_height / img_height
            scale_ratio = min(width_ratio, height_ratio, 1.0)  # Don't upscale
            
            # Resize if needed
            if scale_ratio < 1.0:
                new_width = int(img_width * scale_ratio)
                new_height = int(img_height * scale_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            
            label = tk.Label(splash, image=photo, bg='white')
            label.image = photo
            label.pack()
            
            # Center splash
            splash.update_idletasks()
            w = splash.winfo_width()
            h = splash.winfo_height()
            x = (screen_width - w) // 2
            y = (screen_height - h) // 2
            splash.geometry(f"+{x}+{y}")
            
            # Close after 2 seconds (increased for better visibility)
            splash.after(2000, splash.destroy)
            splash.wait_window()
            
            # Show main window after splash closes
            self.root.deiconify()
        except Exception as e:
            print(f"Warning: Could not show splash: {e}")
            # If splash fails, make sure main window is visible
            self.root.deiconify()
    
    def _setup_ui(self):
        """Setup the main UI components."""
        # Font styles from theme
        self.font_style = self.theme.fonts.body
        self.title_font = self.theme.fonts.title
        
        # Main container with grid layout for responsive design
        self.main_container = Frame(self.root, bg=self.theme.colors.bg_main)
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure grid weights for responsive layout
        self.main_container.rowconfigure(0, weight=82)  # Top area (tabs + chart)
        self.main_container.rowconfigure(1, weight=18)  # Bottom panel (scores)
        self.main_container.columnconfigure(0, weight=48)  # Left frame (tabs)
        self.main_container.columnconfigure(1, weight=52)  # Right frame (chart)
        
        # Create main frames
        self._create_left_frame()
        self._create_right_frame()
        self._create_bottom_panel()
        
        # Initialize tabs
        self._create_tabs()
        
        # Initial update
        self._update_display()
    
    def _create_left_frame(self):
        """Create the left frame containing tabs."""
        self.left_frame = Frame(self.main_container, bg=self.theme.colors.bg_main)
        self.left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Create styled notebook
        style = ttk.Style()
        style.configure('Custom.TNotebook', background=self.theme.colors.bg_main)
        style.configure('Custom.TNotebook.Tab', 
                       padding=[10, 6], 
                       font=self.theme.fonts.small)
        
        self.notebook = ttk.Notebook(self.left_frame, style='Custom.TNotebook')
    
    def _create_right_frame(self):
        """Create the right frame containing the radar chart."""
        self.right_frame = Frame(self.main_container, bg=self.theme.colors.bg_card,
                                highlightbackground=self.theme.colors.border,
                                highlightthickness=1)
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        # Title bar with help button
        title_bar = Frame(self.right_frame, bg=self.theme.colors.bg_card)
        title_bar.pack(fill='x', pady=(8, 2))
        
        title_label = Label(title_bar, text="Assessment Overview",
                           font=self.theme.fonts.heading,
                           bg=self.theme.colors.bg_card,
                           fg=self.theme.colors.primary_dark)
        title_label.pack(side='left', padx=10)
        
        # Add help button
        help_text = """ESAI Assessment Overview

The radar chart shows your environmental suitability assessment across 8 dimensions:

1. Sample Collection (SC): Evaluate sample collection methods
2. Sample Preparation (SP): Assess sample preparation processes
3. Analytical Technique (AT): Evaluate analytical methods used
4. Reagents: Assess reagent usage and environmental impact
5. Method Performance: Evaluate method characteristics
6. Operator Safety: Assess operational safety
7. Economic: Evaluate cost and resource efficiency
8. Waste Disposal: Assess waste management practices

Scoring:
- Each dimension is scored based on weighted criteria
- Colors indicate greenness: Red (poor) → Yellow → Green (excellent)
- Total score out of 100 represents overall environmental suitability

How to use:
1. Set dimension weights in the "Weight" tab
2. Answer questions in each assessment tab
3. View real-time updates in the radar chart
4. Export comprehensive PDF reports

Hover over any element to see tooltips with more information."""
        
        help_btn = HelpButton(title_bar, help_text, "ESAI Help")
        help_btn.pack(side='right', padx=10)
        ToolTip(help_btn, "Click for help and instructions")
        
        # Create figure for radar chart - ensure full visibility
        self.fig = Figure(figsize=(6, 5.5), dpi=100, facecolor=self.theme.colors.bg_card)
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.theme.colors.bg_card)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().configure(bg=self.theme.colors.bg_card)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=2)
    
    def _create_bottom_panel(self):
        """Create the bottom panel with scores and buttons."""
        self.bottom_panel = Frame(self.main_container, bg=self.theme.colors.bg_main)
        self.bottom_panel.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(10, 0))
        
        # Score panel on the left
        self._create_score_panel()
        
        # Buttons on the right
        self._create_buttons()
    
    def _create_score_panel(self):
        """Create the score display panel."""
        score_container = Frame(self.bottom_panel, bg=self.theme.colors.bg_card,
                               highlightbackground=self.theme.colors.border,
                               highlightthickness=1)
        score_container.pack(side='left', fill='both', expand=True, padx=(0, 10), pady=5)
        
        # Total score - compact design
        total_container = Frame(score_container, bg=self.theme.colors.bg_card)
        total_container.pack(side='left', fill='y', padx=8, pady=8)
        
        total_frame = Frame(total_container, bg=self.theme.colors.primary,
                           highlightbackground=self.theme.colors.primary_dark,
                           highlightthickness=1)
        total_frame.pack()
        
        self.total_var = tk.StringVar(value='0.00')
        
        Label(total_frame, text='TOTAL', 
             font=(self.theme.fonts.family, 8, 'bold'),
             bg=self.theme.colors.primary, 
             fg=self.theme.colors.text_light).pack(pady=(8, 2), padx=15)
        
        Label(total_frame, textvariable=self.total_var, 
             font=(self.theme.fonts.family, 24, 'bold'),
             bg=self.theme.colors.primary, 
             fg=self.theme.colors.text_light).pack(pady=(0, 1), padx=15)
        
        Label(total_frame, text='/100', 
             font=(self.theme.fonts.family, 9),
             bg=self.theme.colors.primary, 
             fg=self.theme.colors.text_light).pack(pady=(0, 8), padx=15)
        
        # Dimension scores - compact grid
        dims_container = Frame(score_container, bg=self.theme.colors.bg_card)
        dims_container.pack(side='left', fill='both', expand=True, padx=5, pady=8)
        
        self.dimension_vars = {}
        dimensions = [
            ('Sample collection', '#2196F3'),
            ('Sample preparation', '#9C27B0'),
            ('Analytical techniques', '#F44336'),
            ('Economy', '#FF9800'),
            ('Method', '#4CAF50'),
            ('Operator', '#795548'),
            ('Reagent', '#E91E63'),
            ('Waste', '#009688')
        ]
        
        # Configure grid for 2 rows x 4 columns
        for i in range(4):
            dims_container.columnconfigure(i, weight=1, uniform='dim')
        for i in range(2):
            dims_container.rowconfigure(i, weight=1, uniform='row')
        
        for idx, (dim_key, color) in enumerate(dimensions):
            row = idx // 4
            col = idx % 4
            
            var = tk.StringVar(value='0.00')
            self.dimension_vars[dim_key] = var
            
            # Compact card
            card = Frame(dims_container, bg='white',
                        highlightbackground='#ddd',
                        highlightthickness=1)
            card.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            
            # Top accent
            Frame(card, bg=color, height=2).pack(fill='x')
            
            # Content
            content = Frame(card, bg='white')
            content.pack(fill='both', expand=True, padx=8, pady=6)
            
            Label(content, text=dim_key, 
                 font=(self.theme.fonts.family, 9, 'bold'),
                 bg='white', fg='#333').pack(anchor='w')
            
            score_row = Frame(content, bg='white')
            score_row.pack(anchor='w', pady=(2, 0))
            
            Label(score_row, textvariable=var,
                 font=(self.theme.fonts.family, 14, 'bold'),
                 bg='white', fg=color).pack(side='left')
            
            Label(score_row, text='pts',
                 font=(self.theme.fonts.family, 8),
                 bg='white', fg='#999').pack(side='left', padx=(3, 0), anchor='s', pady=(0, 1))
    
    def _create_buttons(self):
        """Create action buttons."""
        button_frame = Frame(self.bottom_panel, bg=self.theme.colors.bg_main)
        button_frame.pack(side='right', pady=20, padx=20)
        
        # Style configuration for buttons
        btn_style = self.theme.get_button_style("primary")
        success_style = self.theme.get_button_style("success")
        
        # PDF Export button
        export_btn = tk.Button(button_frame, text="📄 Export PDF", 
                              command=self._export_pdf, **btn_style)
        export_btn.pack(side='left', padx=5)
        
        # Add tooltip
        ToolTip(export_btn, "Export assessment results as PDF report\nIncludes radar chart, weights, and detailed scores")
        
        # Add hover effects
        export_btn.bind('<Enter>', lambda e: export_btn.configure(bg=self.theme.colors.primary_dark))
        export_btn.bind('<Leave>', lambda e: export_btn.configure(bg=self.theme.colors.primary))
        
        # Colorbar button
        colorbar_btn = tk.Button(button_frame, text="🎨 Colorbar",
                                command=self._show_colorbar, **success_style)
        colorbar_btn.pack(side='left', padx=5)
        
        # Add tooltip
        ToolTip(colorbar_btn, "View color scale legend\nShows greenness levels from red (poor) to green (excellent)")
        
        colorbar_btn.bind('<Enter>', lambda e: colorbar_btn.configure(bg=self.theme.colors.secondary_dark))
        colorbar_btn.bind('<Leave>', lambda e: colorbar_btn.configure(bg=self.theme.colors.success))
    
    def _create_tabs(self):
        """Create all assessment tabs."""
        # Weight tab
        self.weight_tab = WeightTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # SC tab
        self.sc_tab = SCTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # SP tab
        self.sp_tab = SPTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # AT tab
        self.at_tab = ATTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Economy tab
        self.economy_tab = EconomyTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Method tab
        self.method_tab = MethodTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Operator tab
        self.operator_tab = OperatorTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Reagent tab
        self.reagent_tab = ReagentTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Waste tab
        self.waste_tab = WasteTab(
            self.left_frame, self.notebook,
            on_update=self._update_display,
            font_style=self.font_style,
            theme=self.theme
        )
        
        # Pack notebook
        self.notebook.pack(fill='both', expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.notebook.focus())
    
    def _collect_scores(self) -> Dict[int, float]:
        """Collect all principle scores from tabs."""
        scores = {}
        
        # Collect from each tab
        tabs = [
            self.sc_tab, self.sp_tab, self.at_tab,
            self.economy_tab, self.method_tab, self.operator_tab,
            self.reagent_tab, self.waste_tab
        ]
        
        for tab in tabs:
            for p_id in tab.PRINCIPLES:
                scores[p_id] = tab.get_score(p_id)
        
        return scores
    
    def _collect_colors(self) -> Dict[int, float]:
        """Collect all principle colors from tabs."""
        colors = {}
        
        tabs = [
            self.sc_tab, self.sp_tab, self.at_tab,
            self.economy_tab, self.method_tab, self.operator_tab,
            self.reagent_tab, self.waste_tab
        ]
        
        for tab in tabs:
            for p_id in tab.PRINCIPLES:
                colors[p_id] = tab.get_color(p_id)
        
        return colors
    
    def _collect_principle_scores(self) -> Dict[int, float]:
        """Collect all principle scores (raw scores, not weighted) from tabs."""
        scores = {}
        
        tabs = [
            self.sc_tab, self.sp_tab, self.at_tab,
            self.economy_tab, self.method_tab, self.operator_tab,
            self.reagent_tab, self.waste_tab
        ]
        
        for tab in tabs:
            for p_id in tab.PRINCIPLES:
                scores[p_id] = tab.scores[p_id].get()
        
        return scores
    
    def _update_display(self):
        """Update the display with current scores."""
        # Get weights from Settings tab
        weights = self.weight_tab.get_weights()
        
        # Calculate dimension scores (sum of principle scores × weight)
        sc_score = self.sc_tab.get_dimension_score(weights['w1'])
        sp_score = self.sp_tab.get_dimension_score(weights['w2'])
        at_score = self.at_tab.get_dimension_score(weights['w3'])
        economy_score = self.economy_tab.get_dimension_score(weights['w4'])
        method_score = self.method_tab.get_dimension_score(weights['w5'])
        operator_score = self.operator_tab.get_dimension_score(weights['w6'])
        reagent_score = self.reagent_tab.get_dimension_score(weights['w7'])
        waste_score = self.waste_tab.get_dimension_score(weights['w8'])
        
        # Update dimension displays with 2 decimal places
        self.dimension_vars['Sample collection'].set(f'{sc_score:.2f}')
        self.dimension_vars['Sample preparation'].set(f'{sp_score:.2f}')
        self.dimension_vars['Analytical techniques'].set(f'{at_score:.2f}')
        self.dimension_vars['Economy'].set(f'{economy_score:.2f}')
        self.dimension_vars['Method'].set(f'{method_score:.2f}')
        self.dimension_vars['Operator'].set(f'{operator_score:.2f}')
        self.dimension_vars['Reagent'].set(f'{reagent_score:.2f}')
        self.dimension_vars['Waste'].set(f'{waste_score:.2f}')
        
        # Calculate total with 2 decimal places
        total = round(sc_score + sp_score + at_score + economy_score + 
                     method_score + operator_score + reagent_score + waste_score, 2)
        self.total_var.set(f'{total:.2f}')
        
        # Update radar chart
        self._update_radar_chart(weights)
    
    def _update_radar_chart(self, weights: Dict[str, float]):
        """Update the radar chart display."""
        # Get colors for each principle
        colors = self._collect_colors()
        
        # Calculate dimension scores (weighted)
        dimension_scores = {
            'SC': self.sc_tab.get_dimension_score(weights['w1']),
            'SP': self.sp_tab.get_dimension_score(weights['w2']),
            'AT': self.at_tab.get_dimension_score(weights['w3']),
            'Economy': self.economy_tab.get_dimension_score(weights['w4']),
            'Method': self.method_tab.get_dimension_score(weights['w5']),
            'Operator': self.operator_tab.get_dimension_score(weights['w6']),
            'Reagent': self.reagent_tab.get_dimension_score(weights['w7']),
            'Waste': self.waste_tab.get_dimension_score(weights['w8'])
        }
        
        # Create radar chart (convert total from string to float)
        radar = RadarChartSimple(self.ax, self.colormap)
        radar.draw(colors, float(self.total_var.get()), dimension_scores)
        
        self.canvas.draw()
    
    def _export_pdf(self):
        """Export assessment report to PDF."""
        try:
            # Get save path
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Report As"
            )
            
            if not file_path:
                return
            
            # Collect data
            weights = self.weight_tab.get_weights()
            
            # Save radar chart image temporarily
            temp_radar = "temp_radar.png"
            self.fig.savefig(temp_radar, dpi=300, bbox_inches='tight')
            
            # Create PDF document
            c = canvas.Canvas(file_path)
            
            # ============= PAGE 1: Overview =============
            # Draw title
            c.setFont("Helvetica-Bold", 30)
            c.drawString(50, 800, "ESAI Assessment Report")
            
            c.setFont("Helvetica", 11)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            c.drawString(420, 805, f"Generated: {current_time}")
            
            # Draw radar chart image - larger on page 1
            if os.path.exists(temp_radar):
                with Image.open(temp_radar) as img:
                    img_width, img_height = img.size
                    max_width = 280
                    max_height = 300
                    scaling_factor = min(max_width / img_width, max_height / img_height)
                    new_width = img_width * scaling_factor
                    new_height = img_height * scaling_factor
                c.drawImage(temp_radar, 155, 460, new_width, new_height)
            
            # Build weight table - more spacious
            w_dict = weights
            weight_data = [
                ["Weights of each module", "", "", "", "", "", "", ""],
                ["Sample\ncollection", "Sample\npreparation", "Analytical\ntechniques", "Economy", "Method", "Operator", "Reagent", "Waste"],
                [f"{w_dict['w1']:.2f}", f"{w_dict['w2']:.2f}", f"{w_dict['w3']:.2f}", 
                 f"{w_dict['w4']:.2f}", f"{w_dict['w5']:.2f}", f"{w_dict['w6']:.2f}",
                 f"{w_dict['w7']:.2f}", f"{w_dict['w8']:.2f}"]
            ]
            
            # Create weight table with better spacing
            weight_col_widths = [70, 70, 70, 60, 55, 60, 58, 52]
            weight_table = Table(weight_data, colWidths=weight_col_widths)
            
            weight_style = TableStyle([
                ('SPAN', (0, 0), (7, 0)),
                ('BACKGROUND', (0, 0), (7, 0), colors.HexColor('#5B9BD5')),
                ('TEXTCOLOR', (0, 0), (7, 0), colors.white),
                ('FONTNAME', (0, 0), (7, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (7, 0), 14),
                ('TOPPADDING', (0, 0), (7, 0), 12),
                ('BOTTOMPADDING', (0, 0), (7, 0), 12),
                ('BACKGROUND', (0, 1), (7, 1), colors.HexColor('#D6E9F8')),
                ('FONTNAME', (0, 1), (7, 1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (7, 1), 9),
                ('TOPPADDING', (0, 1), (7, 1), 10),
                ('BOTTOMPADDING', (0, 1), (7, 1), 10),
                ('FONTSIZE', (0, 2), (7, 2), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('GRID', (0, 0), (-1, -1), 0.75, colors.grey),
            ])
            
            weight_table.setStyle(weight_style)
            weight_table.wrapOn(c, 495, 100)
            weight_table.drawOn(c, 50, 320)
            
            # Add page footer
            c.setFont("Helvetica", 9)
            c.drawString(270, 30, "Page 1 of 2")
            
            # Start new page for scores
            c.showPage()
            
            # ============= PAGE 2: Detailed Scores =============
            # Page 2 title
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, 800, "Principle Scores")
            
            # Draw radar chart image again - smaller on page 2, at top
            if os.path.exists(temp_radar):
                with Image.open(temp_radar) as img:
                    img_width, img_height = img.size
                    max_width = 240
                    max_height = 260
                    scaling_factor = min(max_width / img_width, max_height / img_height)
                    new_width = img_width * scaling_factor
                    new_height = img_height * scaling_factor
                c.drawImage(temp_radar, 177, 555, new_width, new_height)
            
            # Build score table
            score_data = [
                ["NO.", "Principle", "Score"]
            ]
            
            # Collect scores from all tabs
            tabs = [
                (self.sc_tab, [1, 2, 3, 4], 'w1'),
                (self.sp_tab, [5, 6, 7, 8, 9, 10], 'w2'),
                (self.at_tab, [11, 12, 13, 14, 15, 16], 'w3'),
                (self.economy_tab, [17], 'w4'),
                (self.method_tab, [18, 19], 'w5'),
                (self.operator_tab, [20], 'w6'),
                (self.reagent_tab, [21, 22, 23, 24, 25], 'w7'),
                (self.waste_tab, [26, 27], 'w8')
            ]
            
            principle_names = {
                1: "Sample collection site",
                2: "Volume of sample collection",
                3: "Throughput of sample collection",
                4: "Energy consumption for sample collection",
                5: "Method of sample preparation",
                6: "Throughput of sample preparation",
                7: "Wastes generated during sample preparation",
                8: "Steps and automation in sample preparation",
                9: "Energy consumption for sample preparation",
                10: "Volume consumed for sample preparation",
                11: "Instrument",
                12: "Volume of injection",
                13: "Throughput of analysis",
                14: "Wastes generated during analysis",
                15: "Degree of automation for analysis",
                16: "Consumption of energy during analysis",
                17: "Cost of analysis per sample",
                18: "Types of methods",
                19: "Methods used",
                20: "Number of safety factors",
                21: "Number of types of reagents",
                22: "Amounts of reagents",
                23: "Toxicity of reagents",
                24: "Quantity of toxic reagents",
                25: "Sustainable and renewable reagents",
                26: "Emissions of greenhouse gases",
                27: "Waste disposal"
            }
            
            for tab, principles, weight_key in tabs:
                weight = w_dict[weight_key]
                for p_id in principles:
                    score = tab.get_score(p_id)
                    weighted_score = score * weight
                    name = principle_names.get(p_id, f"Principle {p_id}")
                    score_data.append([
                        str(p_id), name, f"{weighted_score:.2f}"
                    ])
            
            # Create score table with wider columns for better readability
            score_col_widths = [40, 380, 75]
            score_table = Table(score_data, colWidths=score_col_widths)
            
            # Create score table style
            score_style = TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#5B9BD5')),
                ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
                ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (2, 0), 11),
                ('TOPPADDING', (0, 0), (2, 0), 6),
                ('BOTTOMPADDING', (0, 0), (2, 0), 6),
                
                # General styling
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Left align principle names
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (1, 1), (1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ])
            
            # Add background colors for score column
            row = 1
            for tab, principles, weight_key in tabs:
                for p_id in principles:
                    color_val = tab.get_color(p_id)
                    rgb = mcolors.to_rgb(self.colormap(color_val))
                    bg_color = colors.Color(rgb[0], rgb[1], rgb[2])
                    score_style.add('BACKGROUND', (2, row), (2, row), bg_color)
                    
                    # Add alternating row colors for better readability
                    if row % 2 == 0:
                        score_style.add('BACKGROUND', (0, row), (1, row), colors.HexColor('#F5F5F5'))
                    
                    row += 1
            
            score_table.setStyle(score_style)
            score_table.wrapOn(c, 495, 530)
            score_table.drawOn(c, 50, 25)
            
            # Page footer
            c.setFont("Helvetica", 9)
            c.drawString(270, 15, "Page 2 of 2")
            
            # Save PDF
            c.save()
            
            # Clean up temporary files
            if os.path.exists(temp_radar):
                os.remove(temp_radar)
            
            # Show success message
            from tkinter import messagebox
            messagebox.showinfo("Success", f"Report saved to:\n{file_path}")
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to export PDF:\n{str(e)}")
            print(f"PDF export error: {e}")
    
    def _show_colorbar(self):
        """Show colorbar in a new window."""
        colorbar_window = tk.Toplevel(self.root)
        colorbar_window.title("ESAI Score Colorbar")
        colorbar_window.configure(bg=self.theme.colors.bg_card)
        colorbar_window.resizable(False, False)
        
        # Header
        header = Label(colorbar_window, text="Score Color Reference",
                      font=self.theme.fonts.heading,
                      bg=self.theme.colors.bg_card,
                      fg=self.theme.colors.primary_dark)
        header.pack(pady=(15, 5))
        
        # Description
        desc = Label(colorbar_window, 
                    text="Colors range from Red (low) → Yellow (mid) → Green (high)",
                    font=self.theme.fonts.small,
                    bg=self.theme.colors.bg_card,
                    fg=self.theme.colors.text_secondary)
        desc.pack(pady=(0, 10))
        
        fig = Figure(figsize=(7, 1.2), dpi=100, facecolor=self.theme.colors.bg_card)
        ax = fig.add_subplot(111)
        
        generator = ColorbarGenerator(self.colormap)
        generator.draw(ax)
        
        canvas = FigureCanvasTkAgg(fig, master=colorbar_window)
        canvas.get_tk_widget().configure(bg=self.theme.colors.bg_card)
        canvas.get_tk_widget().pack(padx=20, pady=10)
        canvas.draw()
        
        # Center window
        colorbar_window.update_idletasks()
        w = colorbar_window.winfo_width()
        h = colorbar_window.winfo_height()
        x = (colorbar_window.winfo_screenwidth() - w) // 2
        y = (colorbar_window.winfo_screenheight() - h) // 2
        colorbar_window.geometry(f"+{x}+{y}")
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = ESAIApplication()
    app.run()


if __name__ == "__main__":
    main()
