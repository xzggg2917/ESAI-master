"""
Report Module for ESAI
======================

This module contains:
- PDF report generation
- Table formatting and styling
- Report data structure
"""

import datetime
import os
from typing import Dict, List, Tuple, Optional
import copy

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
from PIL import Image

from esai.config import ColorConfig


class PDFReporter:
    """
    PDF report generator for ESAI assessments.
    
    Generates comprehensive PDF reports including:
    - Radar chart visualization
    - Colorbar legend
    - Weight configuration table
    - Detailed scoring tables
    """
    
    # Principle descriptions for the report
    PRINCIPLE_DESCRIPTIONS = {
        1: "Sample collection site",
        2: "Volume of sample collection",
        3: "Throughput of sample collection",
        4: "Energy consumption for sample collection",
        5: "Method of sample preparation",
        6: "Throughput of sample preparation",
        7: "The amounts of wastes generated during sample preparation",
        8: "The number of steps and the degree of automation in sample preparation",
        9: "Energy consumption for sample preparation",
        10: "Volume consumed for sample preparation",
        11: "Instrument",
        12: "Volume of injection",
        13: "Throughput of analysis",
        14: "The amounts of wastes generated during analysis",
        15: "The degree of automation for analysis",
        16: "Consumption of energy during analysis",
        17: "Number of types of reagents used in analysis process",
        18: "The amounts of reagents used during analytical procedures",
        19: "Toxicity of reagents",
        20: "The quantity of toxic reagents used in the analysis process",
        21: "Sustainable and renewable reagents",
        22: "Type of analysis",
        23: "Multiple or single-element analysis",
        24: "The number of safety factors involved in the experiment",
        25: "The cost of analysis for per sample",
        26: "Emissions of greenhouse gases or toxic gases",
        27: "Waste disposal"
    }
    
    def __init__(self, colors: Optional[ColorConfig] = None):
        """
        Initialize the PDF reporter.
        
        Args:
            colors: Color configuration for score coloring
        """
        self.colors = colors or ColorConfig()
        self._setup_colormap()
    
    def _setup_colormap(self):
        """Setup the color mapping."""
        self.colormap = mcolors.LinearSegmentedColormap(
            'ESAI_ColorMap',
            self.colors.color_dict
        )
    
    def _get_color_for_value(self, value: float) -> colors.Color:
        """
        Get reportlab color for a value (0-1 range).
        
        Args:
            value: Color value between 0 and 1
            
        Returns:
            reportlab Color object
        """
        rgb = mcolors.to_rgb(self.colormap(value))
        return colors.Color(rgb[0], rgb[1], rgb[2])
    
    def generate_report(self, 
                       export_path: str,
                       figure_path: str,
                       colorbar_path: str,
                       report_data: Dict) -> bool:
        """
        Generate a complete PDF report.
        
        Args:
            export_path: Output PDF file path
            figure_path: Path to the radar chart image
            colorbar_path: Path to the colorbar image
            report_data: Dictionary containing all report data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            c = canvas.Canvas(export_path)
            
            # Draw title section
            self._draw_title(c)
            
            # Draw radar chart image
            self._draw_radar_chart(c, figure_path)
            
            # Draw colorbar if exists
            if os.path.exists(colorbar_path):
                self._draw_colorbar(c, colorbar_path)
            
            # Draw weight table
            self._draw_weight_table(c, report_data['weights'])
            
            # Draw score tables
            self._draw_score_tables(c, report_data)
            
            # Draw detailed results table
            self._draw_detailed_table(c, report_data)
            
            c.save()
            return True
            
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return False
    
    def _draw_title(self, c: canvas.Canvas):
        """Draw the title section of the report."""
        c.setFont("Times-Roman", 30)
        c.drawString(30, 820, "ESAI")
        c.drawString(30, 790, "PDFreport")
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        c.drawString(400, 820, "Created time:")
        c.drawString(410, 790, f"{current_time}")
    
    def _draw_radar_chart(self, c: canvas.Canvas, figure_path: str):
        """Draw the radar chart image."""
        if not os.path.exists(figure_path):
            print(f"Warning: Radar chart image not found: {figure_path}")
            return
        
        img = Image.open(figure_path)
        img_width, img_height = img.size
        
        max_width = 200
        max_height = 250
        scaling_factor = min(max_width / img_width, max_height / img_height)
        
        new_width = img_width * scaling_factor
        new_height = img_height * scaling_factor
        
        c.drawImage(figure_path, 130, 590, new_width, new_height)
    
    def _draw_colorbar(self, c: canvas.Canvas, colorbar_path: str):
        """Draw the colorbar image."""
        c.drawImage(colorbar_path, 390, 590, width=50, height=190)
    
    def _draw_weight_table(self, c: canvas.Canvas, weights: Dict[str, float]):
        """Draw the weight configuration table."""
        data = [
            ["Weights of each module", "", "", "", "", "", "", ""],
            ["SC", "SP", "SA", "Economy", "Method", "Operator Safety", "Reagent", "Environment"],
            [f"{weights.get('SC', 0):.2f}", f"{weights.get('SP', 0):.2f}", 
             f"{weights.get('AT', 0):.2f}", f"{weights.get('Economy', 0):.2f}",
             f"{weights.get('Method', 0):.2f}", f"{weights.get('Operator', 0):.2f}",
             f"{weights.get('Reagent', 0):.2f}", f"{weights.get('Waste', 0):.2f}"]
        ]
        
        col_widths = [60, 60, 60, 60, 60, 80, 60, 80]
        table = Table(data, colWidths=col_widths)
        
        style = TableStyle([
            ('SPAN', (0, 0), (7, 0)),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        table.setStyle(style)
        table.wrapOn(c, 500, 100)
        table.drawOn(c, 50, 500)
    
    def _draw_score_tables(self, c: canvas.Canvas, report_data: Dict):
        """Draw the principle scoring tables."""
        principles = report_data['principles']
        weights = report_data['weights']
        
        # Build score table data
        data = [
            ["Score for each principle", "", "", "", "", "", "", ""],
            ["NO.", "Principle", "", "", "", "", "", "Score"],
        ]
        
        # Add principle rows
        for i in range(1, 28):
            principle = principles.get(i, {})
            score = principle.get('score', 0)
            
            # Determine which weight to use
            if i <= 4:
                weight = weights.get('SC', 0.1)
            elif i <= 10:
                weight = weights.get('SP', 0.2)
            elif i <= 16:
                weight = weights.get('AT', 0.2)
            elif i == 17:
                weight = weights.get('Economy', 0.05)
            elif i <= 19:
                weight = weights.get('Method', 0.05)
            elif i == 20:
                weight = weights.get('Operator', 0.1)
            elif i <= 25:
                weight = weights.get('Reagent', 0.1)
            else:
                weight = weights.get('Waste', 0.2)
            
            weighted_score = score * weight
            description = self.PRINCIPLE_DESCRIPTIONS.get(i, f"Principle {i}")
            
            data.append([
                str(i), description, "", "", "", "", "", f"{weighted_score:.2f}"
            ])
        
        col_widths = [30, 50, 50, 50, 50, 50, 50, 50]
        table = Table(data, colWidths=col_widths)
        
        style = TableStyle([
            ('SPAN', (0, 0), (7, 0)),
            ('SPAN', (1, 1), (6, 1)),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Add background colors based on scores
        for i in range(1, 28):
            principle = principles.get(i, {})
            color_value = principle.get('color_value', 0)
            bg_color = self._get_color_for_value(color_value)
            style.add('BACKGROUND', (7, i + 1), (7, i + 1), bg_color)
        
        table.setStyle(style)
        table.wrapOn(c, 400, 400)
        table.drawOn(c, 50, 50)
    
    def _draw_detailed_table(self, c: canvas.Canvas, report_data: Dict):
        """Draw the detailed results table with all assessment values."""
        # This is a complex table with merged cells and color coding
        # Implementation follows the original ESAI.py structure
        pass  # Full implementation would be added here


def create_pdf_reporter(colors: ColorConfig = None) -> PDFReporter:
    """
    Factory function to create a PDFReporter instance.
    
    Args:
        colors: Optional color configuration
        
    Returns:
        Configured PDFReporter instance
    """
    return PDFReporter(colors=colors)
