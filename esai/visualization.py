"""
Visualization Module for ESAI
=============================

This module contains:
- Radar chart (octagonal) visualization
- Color mapping and colorbar generation
- Figure management for tkinter embedding
"""

from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.colors import Normalize
import numpy as np
import os

from esai.config import ColorConfig


class RadarChart:
    """
    Octagonal radar chart for ESAI score visualization.
    
    The chart displays:
    - 8 dimensional sectors (SC, SP, AT, Economy, Method, Operator, Reagent, Waste)
    - 27 principle indicators as trapezoid segments
    - Central circle with total score
    - Color-coded scores from red (low) to green (high)
    """
    
    # Dimension layout configuration (clockwise from top)
    DIMENSION_ORDER = ['SC', 'SP', 'AT', 'Economy', 'Method', 'Operator', 'Reagent', 'Waste']
    DIMENSION_SHORT = ['C', 'P', 'A', 'E', 'M', 'O', 'R', 'W']
    
    # Principle positions for each dimension
    PRINCIPLE_POSITIONS = {
        'SC': [1, 2, 3, 4],          # Top
        'SP': [5, 6, 7, 8, 9, 10],   # Top-right
        'AT': [11, 12, 13, 14, 15, 16],  # Right
        'Economy': [17],             # Bottom-right
        'Method': [18, 19],          # Bottom
        'Operator': [20],            # Bottom-left
        'Reagent': [21, 22, 23, 24, 25],  # Left
        'Waste': [26, 27]            # Top-left
    }
    
    def __init__(self, colors: Optional[ColorConfig] = None, figsize: Tuple[int, int] = (5, 5)):
        """
        Initialize the radar chart.
        
        Args:
            colors: Color configuration
            figsize: Figure size in inches
        """
        self.colors = colors or ColorConfig()
        self.figsize = figsize
        self.fig: Optional[Figure] = None
        self.ax = None
        
        # Create colormap
        self._setup_colormap()
    
    def _setup_colormap(self):
        """Setup the color mapping."""
        self.colormap = mcolors.LinearSegmentedColormap(
            'ESAI_ColorMap',
            self.colors.color_dict
        )
    
    def _get_trapezoid_vertices(self) -> Dict:
        """
        Get all trapezoid vertices for the 27 principles.
        
        Returns:
            Dictionary mapping principle IDs to their polygon vertices
        """
        vertices = {}
        
        # Top trapezoids (SC: principles 1-4)
        vertices[1] = [(-2.7, 7), (-0.7, 7), (-0.7, 10), (-3.7, 10)]
        vertices[2] = [(-0.7, 7), (0.7, 7), (0.7, 10), (-0.7, 10)]
        vertices[3] = [(0.7, 7), (2.1, 7), (2.1, 10), (0.7, 10)]
        vertices[4] = [(2.1, 7), (2.7, 7), (3.7, 10), (2.1, 10)]
        
        # Top-right trapezoids (SP: principles 5-10)
        vertices[5] = [(3.2, 6.8), (3.8, 6.2), (5.8, 8.2), (4.2, 9.8)]
        vertices[6] = [(3.8, 6.2), (5.8, 8.2), (6.3, 7.7), (4.3, 5.7)]
        vertices[7] = [(4.3, 5.7), (6.3, 7.7), (7.3, 6.7), (5.3, 4.7)]
        vertices[8] = [(5.3, 4.7), (7.3, 6.7), (8.3, 5.7), (6.3, 3.7)]
        vertices[9] = [(6.3, 3.7), (8.3, 5.7), (8.8, 5.2), (6.8, 3.2)]
        vertices[10] = [(6.8, 3.2), (8.8, 5.2), (9.8, 4.2), (6.8, 3.2)]
        
        # Right trapezoids (AT: principles 11-16)
        vertices[11] = [(7, 1.8), (10, 1.8), (10, 3.7), (7, 2.7)]
        vertices[12] = [(7, 1.8), (10, 1.8), (10, 1.2), (7, 1.2)]
        vertices[13] = [(7, 1.2), (10, 1.2), (10, 0), (7, 0)]
        vertices[14] = [(7, 0), (10, 0), (10, -1.2), (7, -1.2)]
        vertices[15] = [(7, -1.2), (10, -1.2), (10, -1.8), (7, -1.8)]
        vertices[16] = [(7, -1.8), (10, -1.8), (10, -3.7), (7, -2.7)]
        
        # Bottom-right trapezoid (Economy: principle 17)
        vertices[17] = [(3.2, -6.8), (4.2, -9.8), (9.8, -4.2), (6.8, -3.2)]
        
        # Bottom trapezoids (Method: principles 18-19)
        vertices[18] = [(2.7, -7), (3.7, -10), (0, -10), (0, -7)]
        vertices[19] = [(-2.7, -7), (-3.7, -10), (0, -10), (0, -7)]
        
        # Bottom-left trapezoid (Operator: principle 20)
        vertices[20] = [(-3.2, -6.8), (-4.2, -9.8), (-9.8, -4.2), (-6.8, -3.2)]
        
        # Left trapezoids (Reagent: principles 21-25)
        vertices[21] = [(-7, -2.7), (-10, -3.7), (-10, -1.6), (-7, -1.6)]
        vertices[22] = [(-7, -1.6), (-10, -1.6), (-10, -0.8), (-7, -0.8)]
        vertices[23] = [(-7, -0.8), (-10, -0.8), (-10, 0), (-7, 0)]
        vertices[24] = [(-7, 0), (-10, 0), (-10, 1.6), (-7, 1.6)]
        vertices[25] = [(-7, 1.6), (-10, 1.6), (-10, 3.7), (-7, 2.7)]
        
        # Top-left trapezoids (Waste: principles 26-27)
        vertices[26] = [(-5, 5), (-7, 7), (-9.8, 4.2), (-6.8, 3.2)]
        vertices[27] = [(-3.2, 6.8), (-4.2, 9.8), (-7, 7), (-5, 5)]
        
        return vertices
    
    def _get_text_positions(self) -> Dict[int, Tuple[float, float]]:
        """Get text label positions for each principle."""
        return {
            1: (-2, 8.5), 2: (0, 8.5), 3: (1.4, 8.5), 4: (2.7, 8.5),
            5: (4.5, 7.8), 6: (5.1, 7), 7: (5.8, 6.2), 8: (6.8, 5.2),
            9: (7.6, 4.5), 10: (8.3, 4.0),
            11: (8.5, 2.5), 12: (8.5, 1.4), 13: (8.5, 0.4),
            14: (8.5, -0.8), 15: (8.5, -1.6), 16: (8.5, -2.5),
            17: (6.1, -5.9),
            18: (1.5, -8.5), 19: (-1.5, -8.5),
            20: (-6.1, -5.9),
            21: (-8.5, -2.2), 22: (-8.5, -1.3), 23: (-8.5, -0.5),
            24: (-8.5, 0.8), 25: (-8.5, 2.2),
            26: (-7, 5), 27: (-5, 7)
        }
    
    def _get_dimension_label_positions(self) -> Dict[str, Tuple[float, float]]:
        """Get positions for dimension labels."""
        return {
            'C': (0, 6), 'P': (4.2, 4.3), 'A': (6, 0),
            'E': (4.2, -4.3), 'M': (0, -6), 'O': (-4.2, -4.3),
            'R': (-6, 0), 'W': (-4.2, 4.3)
        }
    
    def _get_score_positions(self) -> Dict[str, Tuple[float, float]]:
        """Get positions for dimension score displays."""
        return {
            'SC': (0, 3.5), 'SP': (2.7, 2.6), 'AT': (3.5, 0),
            'Economy': (2.7, -2.6), 'Method': (0, -3.5),
            'Operator': (-2.7, -2.6), 'Reagent': (-3.5, 0),
            'Waste': (-2.7, 2.6)
        }
    
    def create_figure(self, dimension_scores: Dict[str, float],
                      principle_colors: Dict[int, float],
                      total_score: float) -> Figure:
        """
        Create the radar chart figure.
        
        Args:
            dimension_scores: Dictionary of dimension scores
            principle_colors: Dictionary of principle color values (0-1)
            total_score: Total ESAI score
            
        Returns:
            Matplotlib Figure object
        """
        self.fig = Figure(figsize=self.figsize, dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Calculate colors
        dimension_colors = self._calculate_dimension_colors(dimension_scores)
        center_color = mcolors.to_rgb(self.colormap(Normalize(0, 100)(total_score)))
        
        # Draw sectors (8 wedges)
        self._draw_sectors(dimension_colors)
        
        # Draw center circle
        self._draw_center_circle(center_color, total_score)
        
        # Draw trapezoids for principles
        self._draw_trapezoids(principle_colors)
        
        # Draw outline frames
        self._draw_outlines()
        
        # Add labels
        self._add_labels(dimension_scores, total_score)
        
        # Configure axes
        self._configure_axes()
        
        return self.fig
    
    def _calculate_dimension_colors(self, dimension_scores: Dict[str, float]) -> List:
        """Calculate colors for each dimension sector."""
        weights = [0.1, 0.2, 0.2, 0.05, 0.05, 0.1, 0.1, 0.2]  # w1-w8 defaults
        dimension_order = ['SP', 'SC', 'Waste', 'Reagent', 'Operator', 'Method', 'Economy', 'AT']
        
        colors = []
        for i, dim in enumerate(dimension_order):
            score = dimension_scores.get(dim, 0)
            max_score = 100 * weights[i] if i < len(weights) else 10
            norm = Normalize(vmin=0, vmax=max_score)
            colors.append(mcolors.to_rgb(self.colormap(norm(score))))
        
        return colors
    
    def _draw_sectors(self, colors: List):
        """Draw the 8 wedge sectors."""
        center = (0, 0)
        radius = 5
        num_segments = 8
        angle = 360 / num_segments
        
        for i in range(num_segments):
            theta1 = i * angle + 22.5
            theta2 = theta1 + angle
            sector = Wedge(center, radius, theta1, theta2,
                          edgecolor='black', facecolor=colors[i], linewidth=0.5)
            self.ax.add_patch(sector)
    
    def _draw_center_circle(self, color, total_score: float):
        """Draw the center circle with total score."""
        small_circle = Circle((0, 0), 2, edgecolor='black',
                             facecolor=color, linewidth=0.5)
        self.ax.add_patch(small_circle)
    
    def _draw_trapezoids(self, principle_colors: Dict[int, float]):
        """Draw trapezoid polygons for each principle."""
        vertices = self._get_trapezoid_vertices()
        
        for principle_id, verts in vertices.items():
            color_value = principle_colors.get(principle_id, 0)
            color = self.colormap(color_value)
            
            polygon = Polygon(verts, closed=True, edgecolor='black',
                            facecolor=color, alpha=1, linewidth=0.5)
            self.ax.add_patch(polygon)
    
    def _draw_outlines(self):
        """Draw outline frames for dimension groups."""
        # Top frame (SC)
        top_outline = [(-2.7, 7), (-3.7, 10), (3.7, 10), (2.7, 7)]
        self.ax.add_patch(Polygon(top_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
        
        # Right-top frame (SP)
        rt_outline = [(3.2, 6.8), (4.2, 9.8), (9.8, 4.2), (6.8, 3.2)]
        self.ax.add_patch(Polygon(rt_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
        
        # Right frame (AT)
        right_outline = [(7, -2.7), (10, -3.7), (10, 3.7), (7, 2.7)]
        self.ax.add_patch(Polygon(right_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
        
        # Bottom frame (Method)
        bottom_outline = [(-2.7, -7), (-3.7, -10), (3.7, -10), (2.7, -7)]
        self.ax.add_patch(Polygon(bottom_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
        
        # Left-top frame (Waste)
        lt_outline = [(-3.2, 6.8), (-4.2, 9.8), (-9.8, 4.2), (-6.8, 3.2)]
        self.ax.add_patch(Polygon(lt_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
        
        # Left frame (Reagent)
        left_outline = [(-7, -2.7), (-10, -3.7), (-10, 3.7), (-7, 2.7)]
        self.ax.add_patch(Polygon(left_outline, closed=True, edgecolor='black',
                                  facecolor='none', linewidth=1))
    
    def _add_labels(self, dimension_scores: Dict[str, float], total_score: float):
        """Add all text labels to the chart."""
        fontsize = 9
        fontweight = 100
        
        # Total score in center
        self.ax.text(0, 0, total_score, ha='center', va='center',
                    fontsize=20, fontfamily='Times New Roman')
        
        # Dimension scores
        score_positions = self._get_score_positions()
        for dim, pos in score_positions.items():
            score = dimension_scores.get(dim, 0)
            self.ax.text(pos[0], pos[1], score, ha='center', va='center',
                        fontsize=13, fontfamily='Times New Roman')
        
        # Dimension labels
        label_positions = self._get_dimension_label_positions()
        for label, pos in label_positions.items():
            self.ax.text(pos[0], pos[1], label, ha='center', va='center',
                        fontsize=13, fontfamily='Times New Roman')
        
        # Principle numbers
        text_positions = self._get_text_positions()
        for num, pos in text_positions.items():
            self.ax.text(pos[0], pos[1], str(num), ha='center', va='center',
                        fontsize=fontsize, fontfamily='Arial', fontweight=fontweight)
    
    def _configure_axes(self):
        """Configure the axes appearance."""
        self.ax.set_xlim(-10.1, 10.1)
        self.ax.set_ylim(-10.1, 10.1)
        self.ax.set_aspect('equal')
        
        # Hide axes
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Transparent background
        self.fig.patch.set_facecolor('none')
        self.ax.set_facecolor('none')
    
    def save_figure(self, filepath: str, dpi: int = 300):
        """Save the figure to a file."""
        if self.fig:
            self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white')
    
    def get_figure(self) -> Optional[Figure]:
        """Get the current figure."""
        return self.fig


class ColorbarGenerator:
    """Generator for colorbar images."""
    
    def __init__(self, colormap=None, colors: Optional[ColorConfig] = None):
        """
        Initialize the colorbar generator.
        
        Args:
            colormap: Pre-configured colormap (optional)
            colors: Color configuration
        """
        if colormap is not None:
            self.colormap = colormap
        else:
            self.colors = colors or ColorConfig()
            self._setup_colormap()
    
    def _setup_colormap(self):
        """Setup the color mapping."""
        self.colormap = mcolors.LinearSegmentedColormap(
            'ESAI_ColorMap',
            self.colors.color_dict
        )
    
    def draw(self, ax):
        """
        Draw colorbar on an existing axis.
        
        Args:
            ax: Matplotlib axes object
        """
        import matplotlib.pyplot as plt
        
        norm = Normalize(vmin=0, vmax=100)
        sm = plt.cm.ScalarMappable(norm=norm, cmap=self.colormap)
        sm.set_array([])
        
        # Create a gradient image
        gradient = np.linspace(0, 1, 256).reshape(256, 1)
        ax.imshow(gradient, aspect='auto', cmap=self.colormap, origin='lower',
                 extent=[0, 1, 0, 100])
        
        ax.set_ylabel('Score', fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 100)
        ax.set_xticks([])
        ax.set_yticks([0, 25, 50, 75, 100])
    
    def create_colorbar(self, filepath: str, figsize: Tuple[float, float] = (1, 3)):
        """
        Create and save a colorbar image.
        
        Args:
            filepath: Output file path
            figsize: Figure size in inches
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        norm = Normalize(vmin=0, vmax=100)
        sm = plt.cm.ScalarMappable(norm=norm, cmap=self.colormap)
        
        cbar = fig.colorbar(sm, ax=ax, pad=0.1, aspect=20)
        cbar.ax.set_position([0.4, 0.1, 0.8, 0.8])
        
        # Set ticks
        cbar.set_ticks([0, 50, 75, 100])
        cbar.set_ticklabels(['0%', '50%', '75%', '100%'])
        cbar.ax.tick_params(labelsize=10)
        
        # Hide axes
        for spine in ax.spines.values():
            spine.set_color('none')
        ax.set_xticks([])
        ax.set_yticks([])
        
        fig.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close(fig)


class RadarChartSimple:
    """
    Simplified radar chart that can draw on an existing axis.
    Used for tkinter embedding.
    """
    
    def __init__(self, ax, colormap):
        """
        Initialize with an existing axis and colormap.
        
        Args:
            ax: Matplotlib axes object
            colormap: Colormap to use for colors
        """
        self.ax = ax
        self.colormap = colormap
    
    def draw(self, principle_colors: Dict[int, float], weights: Dict[str, float], 
             total_score: float, dimension_scores: Dict[str, float] = None):
        """
        Draw the radar chart on the axis.
        
        Args:
            principle_colors: Dictionary mapping principle ID to color value (0-1)
            weights: Dictionary of dimension weights
            total_score: Total ESAI score
            dimension_scores: Dictionary of dimension scores (optional)
        """
        from matplotlib.patches import Circle, Wedge, Polygon
        
        # Clear axis
        self.ax.clear()
        
        # Calculate center color
        center_color = mcolors.to_rgb(self.colormap(Normalize(0, 100)(total_score)))
        
        # Draw main circle outline
        main_circle = Circle((0, 0), 5, edgecolor='black', facecolor='none', linewidth=0.5)
        self.ax.add_patch(main_circle)
        
        # Draw center circle
        small_circle = Circle((0, 0), 2, edgecolor='black', facecolor=center_color, linewidth=0.5)
        self.ax.add_patch(small_circle)
        
        # Draw dimension sectors (8 wedges)
        dimension_order = ['SP', 'SC', 'Waste', 'Reagent', 'Operator', 'Method', 'Economy', 'AT']
        weight_map = {
            'SC': weights.get('w1', 0.1),
            'SP': weights.get('w2', 0.2),
            'AT': weights.get('w3', 0.2),
            'Economy': weights.get('w4', 0.05),
            'Method': weights.get('w5', 0.05),
            'Operator': weights.get('w6', 0.1),
            'Reagent': weights.get('w7', 0.1),
            'Waste': weights.get('w8', 0.2)
        }
        
        angle = 360 / 8
        for i, dim in enumerate(dimension_order):
            theta1 = i * angle + 22.5
            theta2 = theta1 + angle
            
            # Get average color for dimension
            dim_principles = {
                'SC': [1, 2, 3, 4],
                'SP': [5, 6, 7, 8, 9, 10],
                'AT': [11, 12, 13, 14, 15, 16],
                'Economy': [17],
                'Method': [18, 19],
                'Operator': [20],
                'Reagent': [21, 22, 23, 24, 25],
                'Waste': [26, 27]
            }
            
            principles = dim_principles.get(dim, [])
            if principles:
                avg_color = sum(principle_colors.get(p, 0) for p in principles) / len(principles)
            else:
                avg_color = 0
            
            color = self.colormap(avg_color)
            sector = Wedge((0, 0), 5, theta1, theta2, width=3,
                          edgecolor='black', facecolor=color, linewidth=0.5)
            self.ax.add_patch(sector)
        
        # Draw trapezoids for each principle
        vertices = self._get_trapezoid_vertices()
        for pid, verts in vertices.items():
            color_val = principle_colors.get(pid, 0)
            color = self.colormap(color_val)
            polygon = Polygon(verts, closed=True, edgecolor='black',
                            facecolor=color, alpha=1, linewidth=0.5)
            self.ax.add_patch(polygon)
        
        # Add text labels
        self._add_labels(total_score, dimension_scores)
        
        # Configure axes - ensure full visibility with padding
        self.ax.set_xlim(-11.5, 11.5)
        self.ax.set_ylim(-11.5, 11.5)
        self.ax.set_aspect('equal')
        
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
    
    def _get_trapezoid_vertices(self) -> Dict:
        """Get trapezoid vertices for principles."""
        vertices = {}
        
        # Top trapezoids (SC: principles 1-4)
        vertices[1] = [(-2.7, 7), (-0.7, 7), (-0.7, 10), (-3.7, 10)]
        vertices[2] = [(-0.7, 7), (0.7, 7), (0.7, 10), (-0.7, 10)]
        vertices[3] = [(0.7, 7), (2.1, 7), (2.1, 10), (0.7, 10)]
        vertices[4] = [(2.1, 7), (2.7, 7), (3.7, 10), (2.1, 10)]
        
        # Top-right trapezoids (SP: principles 5-10)
        vertices[5] = [(3.2, 6.8), (3.8, 6.2), (5.8, 8.2), (4.2, 9.8)]
        vertices[6] = [(3.8, 6.2), (4.3, 5.7), (6.3, 7.7), (5.8, 8.2)]
        vertices[7] = [(4.3, 5.7), (5.3, 4.7), (7.3, 6.7), (6.3, 7.7)]
        vertices[8] = [(5.3, 4.7), (6.3, 3.7), (8.3, 5.7), (7.3, 6.7)]
        vertices[9] = [(6.3, 3.7), (6.8, 3.2), (8.8, 5.2), (8.3, 5.7)]
        vertices[10] = [(6.8, 3.2), (9.8, 4.2), (8.8, 5.2), (6.8, 3.2)]
        
        # Right trapezoids (AT: principles 11-16) - fixed vertex order
        vertices[11] = [(7, 2.7), (10, 3.7), (10, 1.8), (7, 1.8)]
        vertices[12] = [(7, 1.8), (10, 1.8), (10, 1.2), (7, 1.2)]
        vertices[13] = [(7, 1.2), (10, 1.2), (10, 0), (7, 0)]
        vertices[14] = [(7, 0), (10, 0), (10, -1.2), (7, -1.2)]
        vertices[15] = [(7, -1.2), (10, -1.2), (10, -1.8), (7, -1.8)]
        vertices[16] = [(7, -1.8), (10, -1.8), (10, -3.7), (7, -2.7)]
        
        # Bottom-right trapezoid (Economy: principle 17)
        vertices[17] = [(3.2, -6.8), (4.2, -9.8), (9.8, -4.2), (6.8, -3.2)]
        
        # Bottom trapezoids (Method: principles 18-19)
        vertices[18] = [(0, -7), (0, -10), (3.7, -10), (2.7, -7)]
        vertices[19] = [(0, -7), (0, -10), (-3.7, -10), (-2.7, -7)]
        
        # Bottom-left trapezoid (Operator: principle 20)
        vertices[20] = [(-3.2, -6.8), (-6.8, -3.2), (-9.8, -4.2), (-4.2, -9.8)]
        
        # Left trapezoids (Reagent: principles 21-25)
        vertices[21] = [(-7, -1.6), (-10, -1.6), (-10, -3.7), (-7, -2.7)]
        vertices[22] = [(-7, -0.8), (-10, -0.8), (-10, -1.6), (-7, -1.6)]
        vertices[23] = [(-7, 0), (-10, 0), (-10, -0.8), (-7, -0.8)]
        vertices[24] = [(-7, 1.6), (-10, 1.6), (-10, 0), (-7, 0)]
        vertices[25] = [(-7, 2.7), (-10, 3.7), (-10, 1.6), (-7, 1.6)]
        
        # Top-left trapezoids (Waste: principles 26-27)
        vertices[26] = [(-5, 5), (-6.8, 3.2), (-9.8, 4.2), (-7, 7)]
        vertices[27] = [(-3.2, 6.8), (-5, 5), (-7, 7), (-4.2, 9.8)]
        
        return vertices
    
    def _add_labels(self, total_score: float, dimension_scores: Dict[str, float] = None):
        """Add text labels."""
        # Total score in center
        self.ax.text(0, 0, f'{total_score}', ha='center', va='center',
                    fontsize=16, fontfamily='Times New Roman')
        
        # Dimension scores (in inner sectors)
        if dimension_scores:
            score_positions = {
                'SC': (0, 3.5), 
                'SP': (2.7, 2.6), 
                'AT': (3.5, 0.0),
                'Economy': (2.7, -2.6), 
                'Method': (0.0, -3.5),
                'Operator': (-2.7, -2.6), 
                'Reagent': (-3.5, 0.0),
                'Waste': (-2.7, 2.6)
            }
            
            for dim, pos in score_positions.items():
                score = dimension_scores.get(dim, 0)
                self.ax.text(pos[0], pos[1], f'{score:.1f}', ha='center', va='center',
                            fontsize=13, fontfamily='Times New Roman')
        
        # Dimension labels (outer ring)
        dim_labels = {
            'C': (0, 6), 'P': (4.2, 4.3), 'A': (6, 0),
            'E': (4.2, -4.3), 'M': (0, -6), 'O': (-4.2, -4.3),
            'R': (-6, 0), 'W': (-4.2, 4.3)
        }
        
        for label, pos in dim_labels.items():
            self.ax.text(pos[0], pos[1], label, ha='center', va='center',
                        fontsize=13, fontfamily='Times New Roman')
        
        # Principle numbers
        principle_positions = {
            1: (-2, 8.5), 2: (0, 8.5), 3: (1.4, 8.5), 4: (2.7, 8.5),
            5: (4.5, 7.8), 6: (5.1, 7), 7: (5.8, 6.2), 8: (6.8, 5.2),
            9: (7.6, 4.5), 10: (8.3, 4.0),
            11: (8.5, 2.5), 12: (8.5, 1.4), 13: (8.5, 0.4),
            14: (8.5, -0.8), 15: (8.5, -1.6), 16: (8.5, -2.5),
            17: (6.1, -5.9),
            18: (1.5, -8.5), 19: (-1.5, -8.5),
            20: (-6.1, -5.9),
            21: (-8.5, -2.2), 22: (-8.5, -1.3), 23: (-8.5, -0.5),
            24: (-8.5, 0.8), 25: (-8.5, 2.2),
            26: (-7, 5), 27: (-5, 7)
        }
        
        for num, pos in principle_positions.items():
            self.ax.text(pos[0], pos[1], str(num), ha='center', va='center',
                        fontsize=8, fontfamily='Arial')


def create_radar_chart(colors: ColorConfig = None) -> RadarChart:
    """
    Factory function to create a RadarChart instance.
    
    Args:
        colors: Optional color configuration
        
    Returns:
        Configured RadarChart instance
    """
    return RadarChart(colors=colors)


def create_colorbar_generator(colors: ColorConfig = None) -> ColorbarGenerator:
    """
    Factory function to create a ColorbarGenerator instance.
    
    Args:
        colors: Optional color configuration
        
    Returns:
        Configured ColorbarGenerator instance
    """
    return ColorbarGenerator(colors=colors)
