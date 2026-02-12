"""
Splash Screen for ESAI
======================

This module contains the splash screen shown during application startup.
"""

import tkinter as tk
from PIL import Image, ImageTk
from typing import Callable, Optional
import os


class SplashScreen(tk.Toplevel):
    """
    Splash screen shown during application startup.
    """
    
    def __init__(self, parent, image_path: str, duration: int = 1000,
                 on_close: Callable = None):
        """
        Initialize the splash screen.
        
        Args:
            parent: Parent window
            image_path: Path to splash image
            duration: How long to show splash (ms)
            on_close: Callback when splash closes
        """
        super().__init__(parent)
        
        self._duration = duration
        self._on_close = on_close
        self._image_ref = None
        
        # Configure window
        self.overrideredirect(True)  # Remove window decorations
        self.configure(bg='white')  # White background
        
        # Load and display image
        self._setup_image(image_path)
        
        # Center on screen
        self._center_window()
        
        # Schedule auto-close
        self.after(duration, self._close_splash)
    
    def _setup_image(self, image_path: str):
        """Load and display the splash image."""
        try:
            if os.path.exists(image_path):
                # Load image
                img = Image.open(image_path)
                
                # Get screen dimensions
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                
                # Calculate max size (80% of screen)
                max_width = int(screen_width * 0.8)
                max_height = int(screen_height * 0.8)
                
                # Get original dimensions
                img_width, img_height = img.size
                
                # Calculate scaling ratio
                width_ratio = max_width / img_width
                height_ratio = max_height / img_height
                scale_ratio = min(width_ratio, height_ratio, 1.0)  # Don't upscale
                
                # Resize if needed
                if scale_ratio < 1.0:
                    new_width = int(img_width * scale_ratio)
                    new_height = int(img_height * scale_ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                self._image_ref = ImageTk.PhotoImage(img)
                
                label = tk.Label(self, image=self._image_ref, bg='white')
                label.pack()
            else:
                # Fallback if image not found
                self._create_fallback_splash()
        except Exception as e:
            print(f"Error loading splash image: {e}")
            self._create_fallback_splash()
    
    def _create_fallback_splash(self):
        """Create a fallback splash if image cannot be loaded."""
        self.configure(bg='white')
        self.geometry("400x200")
        
        label = tk.Label(self, text="ESAI", font=('Times New Roman', 36, 'bold'),
                        bg='white', fg='#2c3e50')
        label.pack(expand=True)
        
        subtitle = tk.Label(self, text="Environmental Suitability Assessment Index",
                           font=('Times New Roman', 12), bg='white', fg='gray')
        subtitle.pack(pady=20)
    
    def _center_window(self):
        """Center the splash screen on the display."""
        self.update_idletasks()
        
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _close_splash(self):
        """Close the splash screen and invoke callback."""
        self.destroy()
        if self._on_close:
            self._on_close()


def show_splash(parent: tk.Tk, image_path: str, duration: int = 1000,
                on_done: Callable = None):
    """
    Convenience function to show a splash screen.
    
    Args:
        parent: Parent window
        image_path: Path to splash image
        duration: How long to show splash (ms)
        on_done: Callback when splash closes
    """
    splash = SplashScreen(parent, image_path, duration, on_done)
    return splash
