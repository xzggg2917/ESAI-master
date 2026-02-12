import datetime
import locale
import os
import sys
from pathlib import Path

# ============================================================================
# Resource Path Management
# ============================================================================
# This section provides robust file path handling to prevent FileNotFoundError
# when the application is run from different working directories

def get_resource_path(relative_path):
    """
    Get absolute path to resource files (images, icons, etc.).
    Works correctly regardless of the current working directory.
    
    Args:
        relative_path (str): Relative path to the resource file
        
    Returns:
        str: Absolute path to the resource file
        
    This function ensures that resource files can be found even when:
    - Running from different working directories
    - Running as a script vs. frozen executable (PyInstaller, etc.)
    - Importing as a module
    """
    try:
        # Get the directory where this script is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable (PyInstaller)
            base_path = Path(sys.executable).parent
        else:
            # Running as normal Python script
            base_path = Path(__file__).parent.resolve()
        
        # Construct absolute path to resource
        resource_path = base_path / relative_path
        
        # Verify the file exists
        if not resource_path.exists():
            raise FileNotFoundError(
                f"Resource file not found: {resource_path}\n"
                f"Looking in directory: {base_path}\n"
                f"Please ensure the file exists in the application directory."
            )
        
        return str(resource_path)
        
    except Exception as e:
        # Provide helpful error message for debugging
        print(f"Error locating resource '{relative_path}': {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script directory: {Path(__file__).parent if '__file__' in globals() else 'Unknown'}")
        raise

# ============================================================================
# Locale Configuration
# ============================================================================
# Fix locale issues for ttkbootstrap compatibility
# This prevents crashes on systems with non-standard locale settings
# (common in Docker containers, minimal Linux installations, and various Windows configurations)
try:
    # Try to set a safe locale before importing ttkbootstrap
    if os.name == 'nt':  # Windows
        try:
            locale.setlocale(locale.LC_ALL, 'C')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except:
                pass
    else:  # Unix-like systems
        os.environ['LC_ALL'] = 'C'
        os.environ['LANG'] = 'C'
except Exception as e:
    print(f"Warning: Could not set locale: {e}")

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from reportlab.lib import colors
from reportlab.pdfgen import canvas as cs
from reportlab.platypus import Table, TableStyle
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *

# Try to import ttkbootstrap with fallback to standard ttk
USE_TTKBOOTSTRAP = False
try:
    import ttkbootstrap
    USE_TTKBOOTSTRAP = True
except (ImportError, Exception) as e:
    print(f"Warning: ttkbootstrap not available or failed to load: {e}")
    print("Falling back to standard ttk styling")
    USE_TTKBOOTSTRAP = False

from PIL import Image, ImageTk
from matplotlib.patches import Circle, Wedge, Polygon
import copy

# Configure matplotlib fonts with fallback mechanism
# This prevents font-related warnings/errors on systems without Chinese fonts
def configure_matplotlib_fonts():
    """
    Configure matplotlib to use appropriate fonts with intelligent fallback.
    Tries multiple font options to ensure compatibility across different systems.
    """
    import matplotlib.font_manager as fm
    
    # List of fonts to try, in order of preference
    # Includes Chinese fonts, common system fonts, and universal fallbacks
    font_candidates = [
        # Chinese fonts (for proper Chinese character display)
        'SimHei',           # Windows simplified Chinese
        'Microsoft YaHei',  # Windows modern Chinese
        'STHeiti',          # macOS Chinese
        'WenQuanYi Micro Hei',  # Linux Chinese
        'Noto Sans CJK SC', # Google Noto (cross-platform)
        'Source Han Sans CN',  # Adobe Source Han
        'PingFang SC',      # macOS modern Chinese
        'Hiragino Sans GB', # macOS Japanese/Chinese
        # Universal fallbacks
        'DejaVu Sans',      # Common on Linux
        'Arial',            # Common on Windows/Mac
        'Helvetica',        # macOS default
        'sans-serif'        # System default
    ]
    
    # Get list of available fonts on the system
    available_fonts = set(f.name for f in fm.fontManager.ttflist)
    
    # Find which fonts from our list are actually available
    available_candidates = [font for font in font_candidates if font in available_fonts]
    
    if available_candidates:
        # Set the font family to our available fonts
        matplotlib.rcParams['font.sans-serif'] = available_candidates
        print(f"Matplotlib configured with fonts: {', '.join(available_candidates[:3])}")
        if available_candidates[0] not in ['SimHei', 'Microsoft YaHei', 'STHeiti', 
                                            'WenQuanYi Micro Hei', 'Noto Sans CJK SC']:
            print("Warning: No Chinese fonts available. Chinese characters may not display correctly.")
    else:
        # Use system default if none of our candidates are available
        print("Warning: Using system default fonts. Text display may vary.")
    
    # Disable font warnings to prevent cluttering console
    matplotlib.rcParams['font.family'] = 'sans-serif'
    # Handle missing glyphs gracefully
    matplotlib.rcParams['axes.unicode_minus'] = False

# Configure fonts before creating any plots
try:
    configure_matplotlib_fonts()
except Exception as e:
    print(f"Warning: Could not configure custom fonts: {e}")
    print("Using matplotlib default fonts.")

# Create a window
win = Tk()
win.overrideredirect(True)

# Load icon with absolute path
try:
    ico_image = Image.open(get_resource_path("logo.ico"))
    icon = ImageTk.PhotoImage(ico_image)
    win.iconphoto(True, icon)
except FileNotFoundError as e:
    print(f"Warning: Could not load application icon: {e}")
except Exception as e:
    print(f"Warning: Error loading icon: {e}")

# win.overrideredirect(True)  # Visually the entire border of the form disappears
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
# Setting the window size
win_width = 1000
win_height = 510
# Calculate window position
x_position = (screen_width - win_width) // 2
y_position = (screen_height - win_height) // 2
x_positionsmall = (screen_width - win_width) // 2 + 200
y_positionsmall = (screen_height - win_height) // 2 + 150
# # Setting window position
win.geometry(f"{win_width}x{win_height}+{x_position}+{y_position}")

# Load splash screen image with absolute path
try:
    image_file = get_resource_path("rj.png")
    original_image = Image.open(image_file)
    # Get the original size of the image
    scaled_image = original_image.resize((win_width, win_height))
    tk_image = ImageTk.PhotoImage(scaled_image)
    canvas = Canvas(win, height=win_height, width=win_width, bd=0, highlightthickness=0)
    canvas.image = tk_image  # Saving a Reference to a PhotoImage Object
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    canvas.pack()
except FileNotFoundError as e:
    print(f"Warning: Could not load splash screen: {e}")
    # Create simple text splash screen as fallback
    canvas = Canvas(win, height=win_height, width=win_width, bd=0, highlightthickness=0)
    canvas.create_text(win_width//2, win_height//2, 
                      text="ESAI\nEnvironmental Suitability Assessment Index",
                      font=("Times New Roman", 24), justify="center")
    canvas.pack()
except Exception as e:
    print(f"Warning: Error loading splash screen: {e}")

win.after(2000, win.destroy)
win.mainloop()
def Allreset():
    global SCsum, SPsum, SAsum, Economysum, Methodsum, Operatorsum, Reagentsum, Environmentsum, label_value
    priscore1.set(0)
    pripdf1.set('Ex situ')
    priscore2.set(0)
    pripdf2.set('0 g/ml')
    priscore3.set(0)
    pripdf3.set('≤1 sample per hour')
    priscore4.set(0)
    pripdf4.set('>1 kWh per sample')
    priscore5.set(0)
    pripdf5.set(1)
    priscore6.set(0)
    pripdf6.set('<1 g/mL')
    priscore7.set(0)
    pripdf7.set('>10 g or 10 mL per sample')
    pripdf81.set('≤2 steps')
    pripdf82.set('Fully automatic')
    priscore8.set(0)

    priscore9.set(0)
    pripdf9.set('>1 kWh per sample')
    priscore10.set(0)
    pripdf10.set('>100 g or 100 mL')
    priscore11.set(0)
    pripdf11.set('High-energy consumption instrument (such as HPLC, GC, UHPLC, LC-MS, 2D-LC, GC-MS, 2D-GC, XRD,XRF.etc.)')
    priscore12.set(0)
    pripdf12.set('>1 mL')
    priscore13.set(0)
    pripdf13.set('≤1 sample per hour')
    priscore14.set(0)
    pripdf14.set('>10 g or 10 mL per sample')
    priscore15.set(0)
    pripdf15.set('Manual')
    priscore16.set(0)
    pripdf16.set('>1 kWh per sample')
    priscore17.set(0)
    pripdf17.set('0 yuan')
    priscore18.set(0)
    pripdf18.set(
        'Qualitative')
    priscore19.set(0)
    pripdf19.set('Single target per analysis')
    priscore20.set(0)
    pripdf20.set(0)
    priscore21.set(0)
    pripdf21.set('>6')
    priscore22.set(0)
    pripdf22.set('>10 mL')
    priscore23.set(0)
    pripdf23.set('Acute toxicity: (e.g.  irritation and corrosiveness to the eyes, skin, and respiratory tract)')
    priscore24.set(0)
    pripdf24.set('> 100 mL')
    priscore25.set(0)
    pripdf25.set('0-25%')
    priscore26.set(0)
    pripdf26.set('Yes')
    priscore27.set(0)
    pripdf27.set('0-25%')
    pricolor1.set(0)
    pricolor2.set(0)
    pricolor3.set(0)
    pricolor4.set(0)
    pricolor5.set(0)
    pricolor6.set(0)
    pricolor7.set(0)
    pricolor8.set(0)
    pricolor9.set(0)
    pricolor10.set(0)
    pricolor11.set(0)
    pricolor12.set(0)
    pricolor13.set(0)
    pricolor14.set(0)
    pricolor15.set(0)
    pricolor16.set(0)
    pricolor17.set(0)
    pricolor18.set(0)
    pricolor19.set(0)
    pricolor20.set(0)
    pricolor21.set(0)
    pricolor22.set(0)
    pricolor23.set(0)
    pricolor24.set(0)
    pricolor25.set(0)
    pricolor26.set(0)
    pricolor27.set(0)
    SCsum.set(0.00)
    SPsum.set(0.00)
    SAsum.set(0.00)
    Economysum.set(0.00)
    Methodsum.set(0.00)
    Operatorsum.set(0.00)
    Reagentsum.set(0.00)
    Environmentsum.set(0.00)
    label_value=0.00

    bottomlabel_value=0
    sampleentry.delete(0, tk.END)
    Dosagetrentry.delete(0, tk.END)
    ecoentry.delete(0, tk.END)
    spentry.delete(0, tk.END)
    Ramountentry.delete(0, tk.END)
    saentry.delete(0, tk.END)
    update_picture()
def save_image():
    global fig

    # Let the user choose the file save path
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:


        fig.savefig(file_path, dpi=300, facecolor='white')
        tk.messagebox.showinfo("Save Image", f"Image saved successfully at {file_path}")

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
win = Tk()
# Setting the title
win.title("Environmental suitability assessment index")
win.geometry(f"{win_width}x{win_height}+{x_position}+{y_position}")
font_style = ("Times New Roman", 12)

# 左框架
left_frame = Frame(win)
left_frame.place(relx=0, rely=0)
# 菜单
menubar = Menu(win)
win.config(menu=menubar)
global filemenu ,Exportpdf
filemenu = Menu(menubar, tearoff=False, font=('Times New Roman', 10))

menubar.add(itemType="cascade", label="File", menu=filemenu)
editmenu = Menu(menubar)
filemenu.add(itemType="command", label="Save image", command=save_image)
filemenu.add(itemType="command", label="All reset", command=Allreset)

filemenu.add(itemType="separator")

Exportpdf = False
# 页面
notebook = ttk.Notebook(left_frame)

#  Weight Frame
weightframe = Frame(notebook)
notebook.add(weightframe, text=' Set ')
Setweight = Frame(weightframe)
Setweightlal = Label(weightframe,
                     text='Please select the appropriate weights',
                     font=font_style)
Setweightlal.pack()
global w1, w2, w3, w4, w5, w6, w7, w8
# Default weights
w1 = 0.1
w2 = 0.2
w3 = 0.2
w4 = 0.05
w5 = 0.05
w6 = 0.1
w7 = 0.1
w8 = 0.2
# Total columns at the bottom
label_value = 0
label_text = 10


def Score():
    global SCsum, SPsum, SAsum, Economysum, Methodsum, Operatorsum, Reagentsum, Environmentsum, label_value
    start_color_hex = 'C5161B'
    # start_color_hex = 'f3993a'
    end_color_hex = '#008843'
    # start_color_hex = 'FF6E03'
    # end_color_hex = '#363636'
    # start_color_hex = '#073CFA'
    # end_color_hex = '#FF5A00'
    # start_color_hex = '#058C64'
    # end_color_hex = '#7D5A37'
    start_color_rgb = hex_to_rgb(start_color_hex)
    end_color_rgb = hex_to_rgb(end_color_hex)

    # 更新颜色字典
    cdict = {
        'red': ((0.0, start_color_rgb[0], start_color_rgb[0]),
                (0.5, 1.0, 1.0),
                (1.0, end_color_rgb[0], end_color_rgb[0])),

        'green': ((0.0, start_color_rgb[1], start_color_rgb[1]),
                  (0.5, 1.0, 1.0),
                  (1.0, end_color_rgb[1], end_color_rgb[1])),

        'blue': ((0.0, start_color_rgb[2], start_color_rgb[2]),
                 (0.5, 1.0, 1.0),
                 (1.0, end_color_rgb[2], end_color_rgb[2]))
    }
    global orange_blue_cmap
    orange_blue_cmap = mcolors.LinearSegmentedColormap('OrangeBlue', cdict)
    lefthalfcolor = orange_blue_cmap(1.0)
    lefthalfcolor_rgb = (int(lefthalfcolor[0] * 255), int(lefthalfcolor[1] * 255), int(lefthalfcolor[2] * 255))
    lefthalfcolor_hex = '#{:02x}{:02x}{:02x}'.format(*lefthalfcolor_rgb)

    righthalfcolor = orange_blue_cmap(0.0)
    righthalfcolor_rgb = (int(righthalfcolor[0] * 255), int(righthalfcolor[1] * 255), int(righthalfcolor[2] * 255))
    righthalfcolor_hex = '#{:02x}{:02x}{:02x}'.format(*righthalfcolor_rgb)
    SCsum = tk.DoubleVar()
    SCsum.set(
        round((float(priscore1.get()) + float(priscore2.get()) + float(priscore3.get())+ float(priscore4.get())) * w1, 2))

    Sorceframe = Frame(win, highlightbackground="grey", highlightthickness=1)
    Sorceframe.place(x=0, y=414)
    SPsum = tk.DoubleVar()
    SPsum.set( round((float(priscore5.get())+float(priscore6.get()) +float(priscore7.get())+float(priscore8.get())+float(priscore9.get())+float(priscore10.get())) * w2, 2))
    SAsum = tk.DoubleVar()
    SAsum.set(
        round((float(priscore11.get())+float(priscore12.get())+float(priscore13.get())+float(priscore14.get()) +float(priscore15.get())+float(priscore16.get()) ) * w3, 2)
    )
    Economysum = tk.DoubleVar()
    Economysum.set(round((float(priscore17.get())) * w5, 2))
    Methodsum = tk.DoubleVar()
    Methodsum.set( round((float(priscore18.get())+float(priscore19.get()) ) * w5, 2))
    Operatorsum = tk.DoubleVar()
    Operatorsum.set(round((float(priscore20.get())) * w6, 2))
    Reagentsum = tk.DoubleVar()
    Reagentsum.set(round((float(priscore21.get())+float(priscore22.get())+float(priscore23.get())+float(priscore24.get())+float(priscore25.get())) * w7, 2))
    Environmentsum = tk.DoubleVar()
    Environmentsum.set(round((float(priscore26.get())+float(priscore27.get())) * w8, 2))

    label_value = round(SCsum.get()+SPsum.get()+SAsum.get()+Economysum.get()+Methodsum.get()+Operatorsum.get()+Reagentsum.get()+Environmentsum.get(),2)

    totalframe = Frame(Sorceframe, highlightbackground="grey", highlightthickness=1.5, padx=5, pady=10)
    lalscore = Label(totalframe, text='Total:', bd=1, font=font_style)
    lalscore.grid(row=0, column=0)
    totalframe.grid(row=0, column=0, sticky="w")

    totalsum = tk.DoubleVar()
    totalsum.set(float(label_value))
    laltotalvalue = Label(Sorceframe, textvariable=totalsum, bd=1, font=('Times New Roman', 11),
                          highlightbackground="grey", highlightthickness=1.5, padx=7, pady=12)
    laltotalvalue.grid(row=1, column=0, sticky="we")

    SCscoreframe = Frame(Sorceframe,highlightbackground='gray',  highlightthickness=1, pady=10.5, padx=5)
    lalSC = Label(SCscoreframe, text='SC:', bd=1, font=font_style)
    lalSC.grid(row=0, column=0, sticky="we")
    lalSCvalue = Label(SCscoreframe, textvariable=SCsum, bd=1, width=3, font=('Times New Roman', 11))
    lalSCvalue.grid(row=0, column=1, padx=11, sticky="we")
    SCscoreframe.grid(row=0, column=1, sticky="we")

    SPscoreframe = Frame(Sorceframe, highlightbackground='gray',  highlightthickness=1, pady=10.5, padx=5)
    lalSP = Label(SPscoreframe, text='SP：', bd=1, font=font_style)
    lalSP.grid(row=0, column=0, sticky="w")
    lalSPvalue = Label(SPscoreframe, textvariable=SPsum, bd=1, width=3, font=('Times New Roman', 11))
    lalSPvalue.grid(row=0, column=1, padx=9, sticky="w")
    SPscoreframe.grid(row=0, column=2, sticky="we")

    SAscoreframe = Frame(Sorceframe, highlightbackground='gray',  highlightthickness=1, pady=10.5, padx=5)
    lalSA = Label(SAscoreframe, text='AT:', bd=1, font=font_style)
    lalSA.grid(row=0, column=0, sticky="w")
    lalSAvalue = Label(SAscoreframe, textvariable=SAsum, bd=1, width=3, font=('Times New Roman', 11))
    lalSAvalue.grid(row=0, column=1, padx=9, sticky="w")
    SAscoreframe.grid(row=0, column=3, sticky="we")

    Economyscoreframe = Frame(Sorceframe, highlightbackground='gray',  highlightthickness=1, pady=10.5,
                              padx=5)
    lalEconomy = Label(Economyscoreframe, text='Economy:', bd=1, font=font_style)
    lalEconomy.grid(row=0, column=0, sticky="w")
    lalEconomyvalue = Label(Economyscoreframe, textvariable=Economysum, bd=1, width=3,
                            font=('Times New Roman', 11))
    lalEconomyvalue.grid(row=0, column=1, padx=9)
    Economyscoreframe.grid(row=0, column=4, sticky="we")

    Methodscoreframe = Frame(Sorceframe, highlightbackground='gray',  highlightthickness=1, pady=11)
    lalMethod = Label(Methodscoreframe, text='Method:', bd=1, font=font_style)
    lalMethod.grid(row=0, column=0, sticky="w")
    lalMethodvalue = Label(Methodscoreframe, textvariable=Methodsum, bd=1, width=3, font=('Times New Roman', 11))
    lalMethodvalue.grid(row=0, column=1, padx=8, sticky="w")
    Methodscoreframe.grid(row=1, column=1, sticky="we")

    operatorscoreframe = Frame(Sorceframe,highlightbackground='gray',  highlightthickness=1, pady=10.5)
    lalOperator = Label(operatorscoreframe, text='Operator:', bd=1, font=font_style)
    lalOperator.grid(row=0, column=0, sticky="w")
    lalOperatorvalue = Label(operatorscoreframe, textvariable=Operatorsum, bd=1, width=3, font=('Times New Roman', 11))
    lalOperatorvalue.grid(row=0, column=1, padx=9, sticky="w")
    operatorscoreframe.grid(row=1, column=3, sticky="we")

    Reagentscoreframe = Frame(Sorceframe,highlightbackground='gray',  highlightthickness=1, pady=10.5,
                              padx=1)
    lalReagent = Label(Reagentscoreframe, text='Reagent:', bd=1, font=font_style)
    lalReagent.grid(row=0, column=0, sticky="w")
    lalReagentvalue = Label(Reagentscoreframe, textvariable=Reagentsum, bd=1, width=3, font=('Times New Roman', 11))
    lalReagentvalue.grid(row=0, column=1, padx=9, sticky="w")
    Reagentscoreframe.grid(row=1, column=2, sticky="we")

    Environmentscoreframe = Frame(Sorceframe, highlightbackground='gray', highlightthickness=1, pady=10.5)
    lalEnvironment = Label(Environmentscoreframe, text=' Waste:', bd=1, font=font_style)
    lalEnvironment.grid(row=0, column=0, sticky="w")
    lalEnvironmentvalue = Label(Environmentscoreframe, textvariable=Environmentsum, bd=1, width=3,
                                font=('Times New Roman', 11))
    lalEnvironmentvalue.grid(row=0, column=1, padx=8, sticky="w")
    Environmentscoreframe.grid(row=1, column=4, sticky="we")


def Sumscore():
    global label_text, label_value
    label_text = round(
        (float(priscore1.get())) * w1, 2)

    label_value = round(
        (float(priscore1.get())) * w1, 2)


def showerr():
    top = Toplevel()
    top.title("Please note.")
    top.geometry(f"420x150+{x_positionsmall}+{y_positionsmall}")
    topLabel = Label(top, text="Please re-enter the weight values\nfor each module if the weight sum is not 1.",
                     font=('Times New Roman', 15))
    topLabel.pack()


def showomissions():
    top = Toplevel()
    top.title("Please note.")
    top.geometry(f"420x150+{x_positionsmall}+{y_positionsmall}")
    topLabel = Label(top, text="Please make sure that the weights \nfor each module have been entered!",
                     font=('Times New Roman', 15))
    topLabel.pack()


def SET_weight():
    global w1, w2, w3, w4, w5, w6, w7, w8
    value = selected_weightvalue.get()

    if value == '1':
        w1 = 0.2
        w2 = 0.2
        w3 = 0.1
        w4 = 0.05
        w5 = 0.05
        w6 = 0.05
        w7 = 0.15
        w8 = 0.2
    if value == '2':
        w1 = 0.2
        w2 = 0.2
        w3 = 0.2
        w4 = 0.05
        w5 = 0.05
        w6 = 0.05
        w7 = 0.05
        w8 = 0.2
    if value == '3':
        w1 = 0.1
        w2 = 0.2
        w3 = 0.1
        w4 = 0.1
        w5 = 0.1
        w6 = 0.1
        w7 = 0.1
        w8 = 0.2
    if value == '4':
        w1 = 0.2
        w2 = 0.2
        w3 = 0.05
        w4 = 0.05
        w5 = 0.05
        w6 = 0.05
        w7 = 0.2
        w8 = 0.2
    if value == '5':
        w1 = 0.2
        w2 = 0.2
        w3 = 0.2
        w4 = 0.05
        w5 = 0.05
        w6 = 0.05
        w7 = 0.2
        w8 = 0.05
    if value == '6':
        w1 = 0.2
        w2 = 0.2
        w3 = 0.2
        w4 = 0.1
        w5 = 0.05
        w6 = 0.1
        w7 = 0.1
        w8 = 0.05
    if value == '7':
        w1 = 0.1
        w2 = 0.2
        w3 = 0.2
        w4 = 0.05
        w5 = 0.05
        w6 = 0.1
        w7 = 0.1
        w8 = 0.2

    update_picture()


def validate_entry_text(text):
    # Verify that the input text is a floating point number or an integer
    try:
        float(text)
        return True
    except ValueError:
        return False


def handle_invalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    text = w1entry.get()
    if not text or validate_entry_text(text):
        # Validation passes or content is null, invalid input handler not executed
        return
    else:
        w1entry.delete(0, tk.END)
        w2entry.delete(0, tk.END)
        w3entry.delete(0, tk.END)
        w4entry.delete(0, tk.END)
        w5entry.delete(0, tk.END)
        w6entry.delete(0, tk.END)


def Handle_weightvalue():
    global w1, w2, w3, w4, w5, w6, w7, w8
    tempw1 = w1entry.get()
    tempw2 = w2entry.get()
    tempw3 = w3entry.get()
    tempw4 = w4entry.get()
    tempw5 = w5entry.get()
    tempw6 = w6entry.get()
    tempw7 = w7entry.get()
    tempw8 = w8entry.get()
    if tempw1 == '' or tempw2 == '' or tempw3 == '' or tempw4 == '' or tempw5 == '' or tempw6 == '' or tempw7 == '' or tempw8 == '':
        showomissions()
        return

    if round(float(tempw1) + float(tempw2) + float(tempw3) + float(tempw4) + float(tempw5) + float(tempw6) + float(
            tempw7) + float(tempw8), 2) == 1.0:

        w1 = float(tempw1)
        w2 = float(tempw2)
        w3 = float(tempw3)
        w4 = float(tempw4)
        w5 = float(tempw5)
        w6 = float(tempw6)
        w7 = float(tempw7)
        w8 = float(tempw8)
        update_picture()
    else:
        showerr()


selected_weightvalue = tk.StringVar()
option1 = Radiobutton(weightframe, text='w1=0.2, w2=0.2, w3=0.1, w4=0.05, w5=0.05, w6=0.05, w7=0.15, w8=0.2',
                      variable=selected_weightvalue,
                      value=1, activeforeground='green', font=('Times New Roman', 10))
option2 = Radiobutton(weightframe, text='w1=0.2, w2=0.2, w3=0.2, w4=0.05, w5=0.05, w6=0.05, w7=0.05, w8=0.2',
                      variable=selected_weightvalue,
                      value=2, activeforeground='green', font=('Times New Roman', 10))
option3 = Radiobutton(weightframe, text='w1=0.1, w2=0.2, w3=0.1, w4=0.1, w5=0.1, w6=0.1, w7=0.1, w8=0.2',
                      variable=selected_weightvalue,
                      value=3, activeforeground='green', font=('Times New Roman', 10))
option4 = Radiobutton(weightframe, text='w1=0.2, w2=0.2, w3=0.05, w4=0.05, w5=0.05, w6=0.05, w7=0.2, w8=0.2',
                      variable=selected_weightvalue,
                      value=4, activeforeground='green', font=('Times New Roman', 10))
option5 = Radiobutton(weightframe, text='w1=0.2, w2=0.2, w3=0.2, w4=0.05, w5=0.05, w6=0.05, w7=0.2, w8=0.05',
                      variable=selected_weightvalue,
                      value=5, activeforeground='green', font=('Times New Roman', 10))
option6 = Radiobutton(weightframe, text='w1=0.2, w2=0.2, w3=0.2, w4=0.1, w5=0.05, w6=0.1, w7=0.1, w8=0.05',
                      variable=selected_weightvalue,
                      value=6, activeforeground='green', font=('Times New Roman', 10))
Default_weights = Radiobutton(weightframe,
                              text='Default_weights: SC (w1) =0.1, SP (w2) =0.2, AT (w3)=0.2, Economy (w4) =0.05, Method\n(w5) =0.05, Safety of operator (w6) =0.1, Reagent (w7) =0.1, Waste (w8) =0.2                 ',
                              variable=selected_weightvalue, value=7,
                              activeforeground='green', font=('Times New Roman', 10), anchor="w")
# Set the selected property to 0 (unchecked state)
selected_weightvalue.set(0)
Default_weights.pack(anchor="w", padx=10)
option1.pack(anchor="w", padx=10)
option2.pack(anchor="w", padx=10)
option3.pack(anchor="w", padx=10)
option4.pack(anchor="w", padx=10)
option5.pack(anchor="w", padx=10)
option6.pack(anchor="w", padx=10)
# Weight Setting Functions


option1.config(command=SET_weight)
option2.config(command=SET_weight)
option3.config(command=SET_weight)
option4.config(command=SET_weight)
option5.config(command=SET_weight)
option6.config(command=SET_weight)
Default_weights.config(command=SET_weight)
Setweightinputframe = Frame(weightframe)
Setweightinputframe.pack()
Setweightinputlal = Label(Setweightinputframe,
                          text="If no suitable weights found above,\nplease enter them below. \nMake sure all the weights sum to 1.",
                          bd=1, font=font_style)
Setweightinputlal.grid(row=0, column=0, columnspan=8, pady=10)

validation = win.register(validate_entry_text)
invalid_command = win.register(handle_invalid_input)
w1lal = Label(Setweightinputframe, text="w1", width=5, font=('Times New Roman', 10))
w2lal = Label(Setweightinputframe, text="w2", width=5, font=('Times New Roman', 10))
w3lal = Label(Setweightinputframe, text="w3", width=5, font=('Times New Roman', 10))
w4lal = Label(Setweightinputframe, text="w4", width=5, font=('Times New Roman', 10))
w5lal = Label(Setweightinputframe, text="w5", width=5, font=('Times New Roman', 10))
w6lal = Label(Setweightinputframe, text="w6", width=5, font=('Times New Roman', 10))
w7lal = Label(Setweightinputframe, text="w7", width=5, font=('Times New Roman', 10))
w8lal = Label(Setweightinputframe, text="w8", width=5, font=('Times New Roman', 10))
w1entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w2entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w3entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w4entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w5entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w6entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w7entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w8entry = tk.Entry(Setweightinputframe, validate="focusout", validatecommand=(validation, "%P"),
                   invalidcommand=(invalid_command,), justify='center', width=5)
w1lal.grid(row=1, column=0)
w2lal.grid(row=1, column=1)
w3lal.grid(row=1, column=2)
w4lal.grid(row=1, column=3)
w5lal.grid(row=1, column=4)
w6lal.grid(row=1, column=5)
w7lal.grid(row=1, column=6)
w8lal.grid(row=1, column=7)
w1entry.grid(row=2, column=0)
w2entry.grid(row=2, column=1)
w3entry.grid(row=2, column=2)
w4entry.grid(row=2, column=3)
w5entry.grid(row=2, column=4)
w6entry.grid(row=2, column=5)
w7entry.grid(row=2, column=6)
w8entry.grid(row=2, column=7)
weightbutton = tk.Button(Setweightinputframe, text="Update weight", command=Handle_weightvalue,
                         font=('Times New Roman', 10))
weightbutton.grid(row=4, column=0, columnspan=8, pady=10)

"""
#样品采集页面
"""

collectionframe = Frame(notebook)
notebook.add(collectionframe, text='SC')
Samplecollection = Frame(collectionframe)
SCsitelal = Label(Samplecollection, text='1. Sample collection site', bd=5, font=font_style)
SCsitelal.pack()
selected_value = tk.StringVar()
selected_value.set(0.0)
exsuit = Radiobutton(Samplecollection, text='Ex situ', variable=selected_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
onsuit = Radiobutton(Samplecollection, text='On site', variable=selected_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
online = Radiobutton(Samplecollection, text='On-line', variable=selected_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
insuit = Radiobutton(Samplecollection, text='In-line', variable=selected_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
exsuit.pack(anchor='w',padx=20)
onsuit.pack(anchor='w',padx=20)
online.pack(anchor='w',padx=20)
insuit.pack(anchor='w',padx=20)
Samplecollection.grid(row=0, column=0, pady=30, sticky="w")
priscore1 = tk.StringVar()
priscore1.set(0.0)
pricolor1 = tk.StringVar()
pricolor1.set(0.0)
pripdf1 = tk.StringVar()
pripdf1.set('Ex situ')
def on_radiobutton_selected():
    value = selected_value.get()

    if value == '1':
        value = 10
        value1 = 0.0

    if value == '2':
        value = 20
        value1 = 0.33
        pripdf1.set('On site')
    if value == '3':
        value = 30
        value1 = 0.66
        pripdf1.set('On-line')
    if value == '4':
        value = 40
        value1 = 1.0
        pripdf1.set('In-line')
    priscore1.set(value)
    pricolor1.set(value1)

    update_picture()


# Set the Radiobutton's callback function
exsuit.config(command=on_radiobutton_selected)
onsuit.config(command=on_radiobutton_selected)
online.config(command=on_radiobutton_selected)
insuit.config(command=on_radiobutton_selected)
########################################Samplevolume###############
Samplevolume = Frame(collectionframe)
SCsitelal = Label(Samplevolume, text='2. Volume of sample collection\n( mg or µL )', bd=5,font=font_style)
SCsitelal.pack()


def validate_entry_text(text):
    # Verify that the input text is a floating point number or an integer
    try:
        float(text)
        return True
    except ValueError:
        return False


def handlesc_invalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    sampleentry.delete(0, tk.END)

invalidsc_command = win.register(handlesc_invalid_input)
name = StringVar()
# Default value setting
name.set("Unit: mg or µL")
sampleentry = tk.Entry(Samplevolume, validate="key", textvariable=name, validatecommand=(validation, "%P"),
                       invalidcommand=(invalidsc_command), justify='center', font=('Times New Roman', 10))
priscore2 = tk.DoubleVar()
priscore2.set(0.0)
pricolor2 = tk.DoubleVar()
pricolor2.set(0.0)
pripdf2 = tk.StringVar()
pripdf2.set(0.0)

def Handle_value():
    # Get the value of the input box


    if sampleentry.get() == '' or sampleentry.get() == 'Unit: mg or µL':
        value = 0
    else:
        value = float(sampleentry.get())
        pripdf2.set(sampleentry.get()+' mg/µL')
        if value > 100000:

            priscore2.set(0.0)
            pricolor2.set(0.0)


        elif value < 10:

            pricolor2.set(1.0)
            priscore2.set(20.0)

        elif value >= 10 and value <= 100000:

            pricolor2.set(round(-0.215*np.log(value)+2.48, 2)/2)
            priscore2.set(round(-0.215*np.log(value)+2.48, 2) * 10)

    update_picture()


# Input box preselection function
def sampledelete():
    if name.get() == "Unit: mg or µL":
        sampleentry.delete(0, 'end')


sampleentry.bind('<FocusIn>', lambda x: sampledelete())
sampleentry.pack()
# Create a button that gets the value of the input box when clicked
button = tk.Button(Samplevolume, text="Confirm", command=Handle_value, font=('Times New Roman', 10))
button.pack(pady=(10, 10))
Samplevolume.grid(row=0, column=1, sticky="nw",pady=30)

########################################Sampleefficiency#######################

Sampleefficiency = Frame(collectionframe, pady=20)
SCefflal = Label(Sampleefficiency, text='3. Throughtput of sample collection', bd=5,font=font_style)
SCefflal.pack()
sampleeff_value = tk.StringVar()
sampleeff_value.set(0.0)
sceff1 = Radiobutton(Sampleefficiency, text='≤1 sample per hour', variable=sampleeff_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
sceff2 = Radiobutton(Sampleefficiency, text='2-10 samples per hour', variable=sampleeff_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
sceff3 = Radiobutton(Sampleefficiency, text='10-60 samples per hour', variable=sampleeff_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
sceff4 = Radiobutton(Sampleefficiency, text='>60 samples per hour', variable=sampleeff_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
sceff1.pack(anchor='w',padx=20)
sceff2.pack(anchor='w',padx=20)
sceff3.pack(anchor='w',padx=20)
sceff4.pack(anchor='w',padx=20)
Sampleefficiency.grid(row=1, column=0,sticky='nw')
priscore3 = tk.StringVar()
priscore3.set(0.0)
pricolor3 = tk.StringVar()
pricolor3.set(0.0)
pripdf3 = tk.StringVar()
pripdf3.set('≤1 sample per hour')

def on_sampleeff_selected():
    value = sampleeff_value.get()

    if value == '1':
        value = 0
        value1 = 0.0
        pripdf3.set('≤1 sample per hour')
    if value == '2':
        value = 10
        value1 = 0.33
        pripdf3.set('2-10 samples per hour')
    if value == '3':
        value = 15
        value1 = 0.66
        pripdf3.set('10-60 samples per hour')
    if value == '4':
        value = 20
        value1 = 1.0
        pripdf3.set('>60 samples per hour')
    priscore3.set(value)

    pricolor3.set(value1)

    update_picture()
# Set the Radiobutton's callback function
sceff1.config(command=on_sampleeff_selected)
sceff2.config(command=on_sampleeff_selected)
sceff3.config(command=on_sampleeff_selected)
sceff4.config(command=on_sampleeff_selected)


Sampleenergy = Frame(collectionframe)
SCenerlal = Label(Sampleenergy, text='4. Energy consumption for sample collection', bd=5,font=font_style)
SCenerlal.pack()
sampleener_value = tk.StringVar()
sampleener_value.set(0.0)
scener1 = Radiobutton(Sampleenergy, text='>1 kWh per sample', variable=sampleener_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
scener2 = Radiobutton(Sampleenergy, text='0.1-1 kWh per sample', variable=sampleener_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
scener3 = Radiobutton(Sampleenergy, text='<0.1 kWh per sample', variable=sampleener_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

scener1.pack(anchor='w',padx=20)
scener2.pack(anchor='w',padx=20)
scener3.pack(anchor='w',padx=20)
Sampleenergy.grid(row=1, column=1,sticky='nw',pady=20)
priscore4 = tk.StringVar()
priscore4.set(0.0)
pricolor4 = tk.StringVar()
pricolor4.set(0.0)
pripdf4 = tk.StringVar()
pripdf4.set('>1 kWh per sample')
def on_sampleener_selected():
    value = sampleener_value.get()

    if value == '1':
        value = 0
        value1 = 0.0
        pripdf4.set('>1 kWh per sample')
    if value == '2':
        value = 10
        value1 = 0.5
        pripdf4.set('0.1-1 kWh per sample')
    if value == '3':
        value = 20
        value1 = 1.0
        pripdf4.set('<0.1 kWh per sample')

    priscore4.set(value)
    pricolor4.set(value1)

    update_picture()

scener1.config(command=on_sampleener_selected)
scener2.config(command=on_sampleener_selected)
scener3.config(command=on_sampleener_selected)





# 样品处理页面
preparationframe = Frame(notebook)
notebook.add(preparationframe, text='SP')
prpmethod = Frame(preparationframe)
prpmethodlal = Label(prpmethod, text='5. Method of sample preparation', bd=5, font=font_style)
prpmethodlal.pack(expand=False, anchor='w',)
prpmethodvalues = ['Please select here',
          'Not required sample preparation',
          'High-greenness preparation method (such as SFE, SPME, enzymatic reaction, membrane separation.etc.)',
          'Medium-greenness preparation method (such as ASE, PSE, PPT.etc.)',
          'Low-greenness preparation method (such as LLE, SPE, Acid-base pretreatment.etc.)',
          ]
prpmethodvar = tk.StringVar()
prpmethodvar.set(prpmethodvalues[0])
prpmethodoption_menu = ttk.OptionMenu(prpmethod, prpmethodvar, *prpmethodvalues)
prpmethodoption_menu.pack( side='left', padx=(30,0),pady=(10,0))
prpmethodoption_menu.configure(width=15)
menu = prpmethodoption_menu['menu']
priscore5 = tk.StringVar()
priscore5.set(0.0)
pricolor5 = tk.StringVar()
pricolor5.set(0.0)
pripdf5 = tk.StringVar()
pripdf5.set('Low-greenness preparation method (such as LLE, SPE, Acid-base pretreatment.etc.)')
def prpmethodoption_changed(*args):
    value = prpmethodvar.get()
    if value == 'Please select here':
        value3 = 1.0
        value = 0.0
    if value == 'Not required sample preparation':
        pripdf5.set('Not required sample preparation')
        value = 30.0
        value3 = 1.0
    if value == 'High-greenness preparation method (such as SFE, SPME, enzymatic reaction, membrane separation.etc.)':
        pripdf5.set('High-greenness preparation method (such as SFE, SPME, enzymatic reaction, membrane separation.etc.)')
        value = 20.0
        value3 = 0.66
    if value == 'Medium-greenness preparation method (such as ASE, PSE, PPT.etc.)':
        pripdf5.set('Medium-greenness preparation method (such as ASE, PSE, PPT.etc.)')
        value = 10.0
        value3 = 0.33
    if value == 'Low-greenness preparation method (such as LLE, SPE, Acid-base pretreatment.etc.)':
        pripdf5.set('Low-greenness preparation method (such as LLE, SPE, Acid-base pretreatment.etc.)')
        value = 0.0
        value3 = 0.0
    priscore5.set(value)
    pricolor5.set(value3)

    update_picture()


prpmethodvar.trace('w', prpmethodoption_changed)
prpmethod.grid(row=0, column=0,sticky='nw')
########################################Sampleprepefficiency#######################

Sampleprepefficiency = Frame(preparationframe)
SPefflal = Label(Sampleprepefficiency, text='6. Throughput of sample preparation', font=font_style)
SPefflal.pack()
sampleprepeff_value = tk.StringVar()
sampleprepeff_value.set(0.0)
speff1 = Radiobutton(Sampleprepefficiency, text='≤1 sample per hour', variable=sampleprepeff_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
speff2 = Radiobutton(Sampleprepefficiency, text='2-10 samples per hour', variable=sampleprepeff_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
speff3 = Radiobutton(Sampleprepefficiency, text='10-60 samples per hour', variable=sampleprepeff_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
speff4 = Radiobutton(Sampleprepefficiency, text='>60 samples per hour', variable=sampleprepeff_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
speff1.pack(anchor='w', padx=20)
speff2.pack(anchor='w', padx=20)
speff3.pack(anchor='w', padx=20)
speff4.pack(anchor='w', padx=20)
Sampleprepefficiency.grid(row=0, column=1,sticky='w')
priscore6 = tk.StringVar()
priscore6.set(0.0)
pricolor6 = tk.StringVar()
pricolor6.set(0.0)

pripdf6 = tk.StringVar()

pripdf6.set('≤1 sample per hour')
def on_sampleprepeff_selected():
    value = sampleprepeff_value.get()

    if value == '1':
        value = 2.5
        value1 = 0.0
        pripdf5.set('≤1 sample per hour')
    if value == '2':
        value = 8
        value1 = 0.33
        pripdf5.set('2-10 samples per hour')
    if value == '3':
        value = 7.5
        value1 = 0.66
        pripdf5.set('10-60 samples per hour')
    if value == '4':
        value = 10
        value1 = 1.0
        pripdf5.set('>60 samples per hour')
    priscore6.set(value)
    pricolor6.set(value1)

    update_picture()


# Set the Radiobutton's callback function
speff1.config(command=on_sampleprepeff_selected)
speff2.config(command=on_sampleprepeff_selected)
speff3.config(command=on_sampleprepeff_selected)
speff4.config(command=on_sampleprepeff_selected)
#waste
samplewasteframe =Frame(preparationframe)
SPwastelal = Label(samplewasteframe, text='7. The amounts of wastes generated during sample preparation', bd=5,font=font_style)
SPwastelal.pack(anchor='w')
sampleprepwaste_value = tk.StringVar()
sampleprepwaste_value.set(0.0)
spwaste1 = Radiobutton(samplewasteframe, text='<1 g or 1 mL per sample', variable=sampleprepwaste_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
spwaste2 = Radiobutton(samplewasteframe, text='1-10 g or 1-10 mL per sample', variable=sampleprepwaste_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
spwaste3 = Radiobutton(samplewasteframe, text='>10 g or 10 mL per sample', variable=sampleprepwaste_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

spwaste1.pack(side='left',anchor='w')
spwaste2.pack(side='left',anchor='w')
spwaste3.pack(anchor='w')
samplewasteframe .grid(row=1, column=0,columnspan=2,sticky='w')
priscore7 = tk.StringVar()
priscore7.set(0.0)
pricolor7 = tk.StringVar()
pricolor7.set(0.0)
pripdf7 = tk.StringVar()
pripdf7.set('<1 g or 1 mL per sample')
#SPenergy
def on_sampleprepwaste_selected():
    value = sampleprepwaste_value.get()

    if value == '1':
        value = 20
        value1 = 1.0
        pripdf6.set('<1 g or 1 mL per sample')
    if value == '2':
        value = 10
        value1 = 0.5
        pripdf6.set('1-10 g or 1-10 mL per sample')

    if value == '3':
        value = 0
        value1 = 0.0
        pripdf6.set('>10 g or 10 mL per sample')


    priscore7.set(value)
    pricolor7.set(value1)


    update_picture()
spwaste1.config(command=on_sampleprepwaste_selected)
spwaste2.config(command=on_sampleprepwaste_selected)
spwaste3.config(command=on_sampleprepwaste_selected)




#############自动化程度
samplestepframe =Frame(preparationframe)
sampleautoframe =Frame(preparationframe)
SPautolal = Label(samplestepframe, text='8. The number of steps and degree of automation in sample preparation',bd=5, font=font_style)
SPautolal.pack()

sampleprepauto_value = tk.StringVar()
sampleprepauto_value.set(0.0)
sampleprepstep_value = tk.StringVar()
sampleprepstep_value.set(0.0)
spstep1 = Radiobutton(samplestepframe, text='≤2 steps', variable=sampleprepstep_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
spstep2 = Radiobutton(samplestepframe, text='3-5 steps', variable=sampleprepstep_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
spstep3 = Radiobutton(samplestepframe, text='≥6 steps', variable=sampleprepstep_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

spstep1.pack(side='left',anchor='w', padx=20)
spstep2.pack(side='left',anchor='w', padx=20)
spstep3.pack(anchor='w', padx=20)
#
spauto1 = Radiobutton(sampleautoframe, text='Fully automatic', variable=sampleprepauto_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
spauto2 = Radiobutton(sampleautoframe, text='Semi-automatic', variable=sampleprepauto_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
spauto3 = Radiobutton(sampleautoframe, text='Manual', variable=sampleprepauto_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

spauto1.pack(side='left',anchor='w', padx=(20,0))
spauto2.pack(side='left',anchor='w', padx=(3,3))
spauto3.pack(anchor='w', padx=(4))
samplestepframe.grid(row=2, column=0,columnspan=2,sticky='w')
sampleautoframe.grid(row=3, column=0,columnspan=2,sticky='nw')
priscore8 = tk.StringVar()
priscore8.set(0.0)
pricolor8 = tk.StringVar()
pricolor8.set(0.0)
pripdf81 = tk.StringVar()
pripdf81.set('≤2 steps')
pripdf82 = tk.StringVar()
pripdf82.set('Fully automatic')
def on_sampleprepstep_selected():
    value11 = sampleprepstep_value.get()
    value12 = sampleprepauto_value.get()

    if value11 == '1' and value12 != '0.0':
        valuescore1 = 10
        valuecolor1 = 0.5
        pripdf81.set('≤2 steps')
    if value11 == '2' and value12 != '0.0':
        valuescore1 = 5
        valuecolor1 = 0.25
        pripdf81.set('3-5 steps')
    if value11 == '3' and value12 != '0.0':
        valuescore1 = 0
        valuecolor1 = 0.0
        pripdf81.set('≥6 steps')
    if value12 == '1' and value11 != '0.0':
        valuescore2 = 10
        valuecolor2 = 0.5
        pripdf82.set('Fully automatic')
    if value12 == '2' and value11 != '0.0':
        valuescore2 = 5
        valuecolor2 = 0.25
        pripdf82.set('Semi-automatic')
    if value12 == '3' and value11 != '0.0':
        valuescore2 = 0
        valuecolor2 = 0.0
        pripdf82.set('Manual')
    if value11 !='0.0' and value12 !='0.0':
        value =valuescore1+valuescore2
        value1=valuecolor1+valuecolor2
        priscore8.set(value)
        pricolor8.set(value1)
        update_picture()
spstep1.config(command=on_sampleprepstep_selected)
spstep2.config(command=on_sampleprepstep_selected)
spstep3.config(command=on_sampleprepstep_selected)
spauto1.config(command=on_sampleprepstep_selected)
spauto2.config(command=on_sampleprepstep_selected)
spauto3.config(command=on_sampleprepstep_selected)



#SPenergy
SPenergy = Frame(preparationframe)
SPenerlal = Label(SPenergy, text='9. Energy consumption for sample preparation', bd=5,font=font_style)
SPenerlal.pack(anchor='w')
spener_value = tk.StringVar()
spener_value.set(0.0)
spener1 = Radiobutton(SPenergy, text='>1 kWh per sample', variable=spener_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
spener2 = Radiobutton(SPenergy, text='0.1-1 kWh per sample', variable=spener_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
spener3 = Radiobutton(SPenergy, text='<0.1 kWh per sample', variable=spener_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

spener1.pack(side='left', anchor='w')
spener2.pack(side='left',anchor='w')
spener3.pack(anchor='w')
SPenergy.grid(row=4, column=0,sticky='nw',columnspan=2)
priscore9 = tk.StringVar()
priscore9.set(0.0)
pricolor9 = tk.StringVar()
pricolor9.set(0.0)
pripdf9 = tk.StringVar()
pripdf9.set('>1 kWh per sample')
def on_spener_selected():
    value = spener_value.get()

    if value == '1':
        value = 0
        value1 = 0.0
        pripdf9.set('>1 kWh per sample')
    if value == '2':
        value = 5
        value1 = 0.5
        pripdf9.set('0.1-1 kWh per sample')
    if value == '3':
        value = 10
        value1 = 1.0
        pripdf9.set('<0.1 kWh per sample')

    priscore9.set(value)
    pricolor9.set(value1)

    update_picture()

spener1.config(command=on_spener_selected)
spener2.config(command=on_spener_selected)
spener3.config(command=on_spener_selected)
########################################SPvolume###############
SPvolume = Frame(preparationframe)
SPsitelal = Label(SPvolume, text='10. Volume consumed for sample preparation ( mg or µL, per sample )', bd=5,font=font_style)
SPsitelal.pack()





def handle_spinvalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    spentry.delete(0, tk.END)

invalidsp_command = win.register(handle_spinvalid_input)
spname = StringVar()
# Default value setting
spname.set("Unit: mg or µL")
spentry = tk.Entry(SPvolume, validate="key", textvariable=spname, validatecommand=(validation, "%P"),
                       invalidcommand=(invalidsp_command), justify='center', font=('Times New Roman', 10))
priscore10 = tk.DoubleVar()
priscore10.set(0.0)
pricolor10 = tk.DoubleVar()
pricolor10.set(0.0)
pripdf10 = tk.StringVar()
pripdf10.set('0 mg/µL')

def HandleSP_value():
    # Get the value of the input box


    if spentry.get() == '' or spentry.get() == 'Unit: mg or µL':
        value = 0
    else:
        value = float(spentry.get())
        pripdf10.set(spentry.get()+' mg/µL')
        if value > 100000:

            priscore10.set(0.0)
            pricolor10.set(0.0)


        elif value < 10:

            pricolor10.set(1.0)
            priscore10.set(10.0)

        elif value >= 10 and value <= 100000:

            pricolor10.set(round((-0.067*np.log(value)**1.432+2.22), 2)/2)
            priscore10.set(round(-0.067*np.log(value)**1.432+2.22,2) * 5)

    update_picture()


# Input box preselection function
def spdelete():
    if spname.get() == "Unit: mg or µL":
        spentry.delete(0, 'end')


spentry.bind('<FocusIn>', lambda x: spdelete())
spentry.pack(side='left',padx=30)
# Create a button that gets the value of the input box when clicked
SPbutton = tk.Button(SPvolume, text="Confirm", command=HandleSP_value, font=('Times New Roman', 10))
SPbutton.pack(pady=(5, 10),padx=(30,0))
SPvolume.grid(row=5, column=0, sticky="nw",columnspan=2)





# 样品分析页面
analysisframe = Frame(notebook)
notebook.add(analysisframe, text='AT')
###############################################instrument##########################################################
SAinstrument = Frame(analysisframe)
SAinstrumentlal = Label(SAinstrument, text='11. Instrument', bd=5, font=font_style)
SAinstrumentlal.pack(expand=False, anchor='w',)
SAinstrumentvalues = ['Please select here',
          'High-energy consumption instrument (such as HPLC, GC, UHPLC, LC-MS, 2D-LC, GC-MS, 2D-GC, XRD,XRF.etc.)',
          'Medium-energy consumption instrument (such as UV-Vis, fluorescence spectrophotometer, atomic absorption spectrometer, Mini mass spectrometer.etc.)',
          'Low-energy consumption instrument (such as portable analyzer, handheld Raman spectrometer.etc.)',
          ]
SAinstrumentvar = tk.StringVar()
SAinstrumentvar.set(SAinstrumentvalues[0])
SAinstrumentoption_menu = ttk.OptionMenu(SAinstrument, SAinstrumentvar, *SAinstrumentvalues)
SAinstrumentoption_menu.pack( side='left', padx=(10,0),pady=(10,0))
SAinstrumentoption_menu.configure(width=15)
menu = SAinstrumentoption_menu['menu']
priscore11 = tk.StringVar()
priscore11.set(0.0)
pricolor11 = tk.StringVar()
pricolor11.set(0.0)
pripdf11 = tk.StringVar()
pripdf11.set('Molecular optical spectroscopic techniques (e.g. UV-vis spectrophotometry,\n fluorimetry, chemiluminescence, etc.)')
def SAinstrumentoption_changed(*args):
    value = SAinstrumentvar.get()
    if value == 'Please select here':
        value3 = 1.0
        value = 0.0
    if value == 'Low-energy consumption instrument (such as portable analyzer, handheld Raman spectrometer.etc.)':

        value = 20.0
        value3 = 1.0

    if value == 'Medium-energy consumption instrument (such as UV-Vis, fluorescence spectrophotometer, atomic absorption spectrometer, Mini mass spectrometer.etc.)':

        value = 10
        value3 = 0.5
    if value == 'High-energy consumption instrument (such as HPLC, GC, UHPLC, LC-MS, 2D-LC, GC-MS, 2D-GC, XRD,XRF.etc.)':

        value = 5
        value3 = 0.0
    priscore11.set(value)
    pricolor11.set(value3)

    update_picture()

# 绑定追踪回调到StringVar对象
SAinstrumentvar.trace('w', SAinstrumentoption_changed)
SAinstrument.grid(row=0, column=0,sticky='n')
###############################################################SAvolume##############################################################
SAvolume = Frame(analysisframe)
SAvolumelal = Label(SAvolume, text='12. Volume of injection ( mg or µL )', font=font_style)
SAvolumelal.pack(padx=(70,0))
def handle_sainvalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    saentry.delete(0, tk.END)

invalidsa_command = win.register(handle_sainvalid_input)
saname = StringVar()
# Default value setting
saname.set("Unit: mg or µL")
saentry = tk.Entry(SAvolume, validate="key", textvariable=saname, validatecommand=(validation, "%P"),
                       invalidcommand=(invalidsa_command), justify='center', font=('Times New Roman', 10))
priscore12 = tk.DoubleVar()
priscore12.set(0.0)
pricolor12 = tk.DoubleVar()
pricolor12.set(0.0)
pripdf12 = tk.StringVar()
pripdf12.set('>1 mL')

def HandleSA_value():
    # Get the value of the input box


    if saentry.get() == '' or saentry.get() == 'Unit: mg or µL':
        value = 0
    else:
        value = float(saentry.get())
        pripdf12.set(saentry.get()+' mg/µL')
        if value > 1000:

            priscore12.set(0.0)
            pricolor12.set(0.0)


        elif value < 1:

            pricolor12.set(1.0)
            priscore12.set(10.0)

        elif value >= 1 and value <= 1000:

            pricolor12.set(round((-0.289*np.log(value)+2), 2)/2)
            priscore12.set(round(-0.289*np.log(value)+2,2) * 5)

    update_picture()


# Input box preselection function
def sadelete():
    if saname.get() == "Unit: mg or µL":
        saentry.delete(0, 'end')


saentry.bind('<FocusIn>', lambda x: sadelete())
saentry.pack(side='left',padx=(90,30))
# Create a button that gets the value of the input box when clicked
SAbutton = tk.Button(SAvolume, text="Confirm", command=HandleSA_value, font=('Times New Roman', 10))
SAbutton.pack(pady=(5, 10),padx=(30,0))
SAvolume.grid(row=0, column=1, sticky="nw",columnspan=2)

#########################################################SAeffframe########################################
SAeffframe =Frame(analysisframe,pady=10)
SAefflal = Label(SAeffframe, text='13. Throughput of analysis', bd=5,font=font_style)
SAefflal.pack(anchor='w')
SAeff_value = tk.StringVar()
SAeff_value.set(0.0)
SAeff1 = Radiobutton(SAeffframe, text='≤1 sample per hour', variable=SAeff_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
SAeff2 = Radiobutton(SAeffframe, text='2-10 samples per hour', variable=SAeff_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
SAeff3 = Radiobutton(SAeffframe, text='10-90 samples per hour', variable=SAeff_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
SAeff4 = Radiobutton(SAeffframe, text='>90 samples per hour', variable=SAeff_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
SAeff1.pack(anchor='w',padx=10)
SAeff2.pack(anchor='w',padx=10)
SAeff3.pack(anchor='w',padx=10)
SAeff4.pack(anchor='w',padx=10)
SAeffframe .grid(row=1, column=0,columnspan=2,sticky='w')
priscore13 = tk.StringVar()
priscore13.set(0.0)
pricolor13 = tk.StringVar()
pricolor13.set(0.0)
pripdf13 = tk.StringVar()
pripdf13.set(1)
def on_SAeff_selected():
    value = SAeff_value.get()

    if value == '4':
        value = 20
        value1 = 1.0
        pripdf13.set('>90 samples per hour')
    if value == '3':
        value = 15
        value1 = 0.66
        pripdf13.set('11-90 samples per hour')
    if value == '2':
        value = 10
        value1 = 0.33

        pripdf13.set('2-10 samples per hour')
    if value == '1':
        value = 5
        value1 = 0.0
        pripdf13.set('≤1 sample per hour')




    priscore13.set(value)
    pricolor13.set(value1)

    update_picture()
SAeff1.config(command=on_SAeff_selected)
SAeff2.config(command=on_SAeff_selected)
SAeff3.config(command=on_SAeff_selected)
SAeff4.config(command=on_SAeff_selected)
################################################################SAwasteframe################################################
SAwasteframe =Frame(analysisframe,pady=10,padx=40)
SAwastelal = Label(SAwasteframe, text='14. The amounts of wastes\ngenerated during analysis',bd=5, font=font_style)
SAwastelal.pack(anchor='w')
SAwaste_value = tk.StringVar()
SAwaste_value.set(0.0)
SAwaste1 = Radiobutton(SAwasteframe, text='>10 g or 10 mL per sample', variable=SAwaste_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
SAwaste2 = Radiobutton(SAwasteframe, text='1-10 g or 1-10 mL per sample', variable=SAwaste_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
SAwaste3 = Radiobutton(SAwasteframe, text='<1 g or 1 mL per sample', variable=SAwaste_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

SAwaste1.pack(anchor='w', padx=10)
SAwaste2.pack(anchor='w', padx=10)
SAwaste3.pack(anchor='w', padx=10)
SAwasteframe .grid(row=1, column=1,columnspan=2,sticky='e')
priscore14 = tk.StringVar()
priscore14.set(0.0)
pricolor14 = tk.StringVar()
pricolor14.set(0.0)
pripdf14 = tk.StringVar()
pripdf14.set('<1 g or 1 mL per sample')
def on_SAwaste_selected():
    value = SAwaste_value.get()

    if value == '3':
        value = 20
        value1 = 1.0
        pripdf14.set('<1 g or 1 mL per sample')
    if value == '2':
        value = 10
        value1 = 0.5
        pripdf14.set('1-10 g or 1-10 mL per sample')
    if value == '1':
        value = 0
        value1 = 0.0
        pripdf14.set('>10 g or 10 mL per sample')


    priscore14.set(value)
    pricolor14.set(value1)

    update_picture()
SAwaste1.config(command=on_SAwaste_selected)
SAwaste2.config(command=on_SAwaste_selected)
SAwaste3.config(command=on_SAwaste_selected)
#############################################################SAdeframe####################
SAdeframe =Frame(analysisframe,pady=10)
SAdelal = Label(SAdeframe, text='15. The degree of automation\n for analysis',bd=5, font=font_style)
SAdelal.pack(anchor='w')
SAde_value = tk.StringVar()
SAde_value.set(0.0)

SAde1 = Radiobutton(SAdeframe, text='Manual', variable=SAde_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
SAde2 = Radiobutton(SAdeframe, text='Semi-automatic', variable=SAde_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
SAde3 = Radiobutton(SAdeframe, text='Fully automatic', variable=SAde_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

SAde1.pack(anchor='w', padx=10)
SAde2.pack(anchor='w', padx=10)
SAde3.pack(anchor='w', padx=10)
SAdeframe .grid(row=3, column=0,columnspan=2,sticky='nw')
priscore15 = tk.StringVar()
priscore15.set(0.0)
pricolor15 = tk.StringVar()
pricolor15.set(0.0)
pripdf15 = tk.StringVar()
pripdf15.set('Manual')
def on_SAde_selected():
    value = SAde_value.get()

    if value == '1':
        value = 0
        value1 = 0.0
        pripdf15.set('Manual')
    if value == '2':
        value = 5
        value1 = 0.5
        pripdf15.set('Semi-automatic')
    if value == '3':
        value = 10
        value1 = 1.0
        pripdf15.set('Fully automatic')


    priscore15.set(value)
    pricolor15.set(value1)

    update_picture()
SAde1.config(command=on_SAde_selected)
SAde2.config(command=on_SAde_selected)
SAde3.config(command=on_SAde_selected)
#############################################################analysisframe####################
SAecframe =Frame(analysisframe,pady=10,padx=60)
SAeclal = Label(SAecframe, text='16. Consumption of energy\n during analysis',bd=5, font=font_style)
SAeclal.pack(anchor='w')
SAec_value = tk.StringVar()
SAec_value.set(0.0)

SAec1 = Radiobutton(SAecframe, text='<0.1 kWh per sample', variable=SAec_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
SAec2 = Radiobutton(SAecframe, text='0.1-1 kWh per sample', variable=SAec_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
SAec3 = Radiobutton(SAecframe, text='>1 kWh per sample', variable=SAec_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

SAec1.pack(anchor='w', padx=10)
SAec2.pack(anchor='w', padx=10)
SAec3.pack(anchor='w', padx=10)
SAecframe .grid(row=3, column=1,columnspan=2,sticky='e')
priscore16 = tk.StringVar()
priscore16.set(0.0)
pricolor16 = tk.StringVar()
pricolor16.set(0.0)
pripdf16 = tk.StringVar()
pripdf16.set('<0.1 kWh per sample')
def on_SAec_selected():
    value = SAec_value.get()

    if value == '1':
        value = 20
        value1 = 1.0
        pripdf12.set('<0.1 kWh per sample')
    if value == '2':
        value = 10
        value1 = 0.5
        pripdf12.set('0.1-1 kWh per sample')
    if value == '3':
        value = 0
        value1 = 0.0
        pripdf12.set('>1 kWh per sample')


    priscore16.set(value)
    pricolor16.set(value1)

    update_picture()
SAec1.config(command=on_SAec_selected)
SAec2.config(command=on_SAec_selected)
SAec3.config(command=on_SAec_selected)
# 经济页面

economyframe = Frame(notebook)
notebook.add(economyframe, text='Economy')
Cost = Frame(economyframe, pady=20)
Costlal = Label(Cost, text='17. The cost of analysis for each sample',bd=5, font=font_style)
Costlal.pack(anchor='w')
def handle_ecoinvalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    ecoentry.delete(0, tk.END)

invalideco_command = win.register(handle_ecoinvalid_input)
econame = StringVar()
# Default value setting
econame.set("Unit: RMB")
ecoentry = tk.Entry(Cost, validate="key", textvariable=econame, validatecommand=(validation, "%P"),
                       invalidcommand=(invalideco_command), justify='center', font=('Times New Roman', 10))
priscore17 = tk.DoubleVar()
priscore17.set(0.0)
pricolor17 = tk.DoubleVar()
pricolor17.set(0.0)
pripdf17 = tk.StringVar()
pripdf17.set('0 yuan')

def Handleeco_value():
    # Get the value of the input box


    if ecoentry.get() == '' or ecoentry.get() == 'Unit: RMB':
        value = 0
    else:
        value = float(ecoentry.get())
        pripdf17.set(ecoentry.get()+' RMB')
        if value > 1000:

            priscore17.set(0.0)
            pricolor17.set(0.0)


        elif value < 10:

            pricolor17.set(1.0)
            priscore17.set(100)

        elif value >= 10 and value <= 1000:
            if(-1/99*(value)+ 1000/99<0):
                pricolor17.set(0.0)
                priscore17.set(0.0)
            else:
                pricolor17.set(round((-1/99*(value)+ 1000/99), 2)/10)
                priscore17.set(round((round(-1/99*(value)+ 1000/99,2))*10,2))


    update_picture()


# Input box preselection function
def ECOdelete():
    if econame.get() == "Unit: RMB":
        ecoentry.delete(0, 'end')


ecoentry.bind('<FocusIn>', lambda x: ECOdelete())
ecoentry.pack(side='left',padx=30)
# Create a button that gets the value of the input box when clicked
ecobutton = tk.Button(Cost, text="Confirm", command=Handleeco_value, font=('Times New Roman', 10))
ecobutton.pack(pady=(5, 10),padx=(30,0))
Cost.grid(row=0, column=0, sticky="nw",columnspan=2)
notebook.bind("<<NotebookTabChanged>>", lambda e: notebook.focus())
# 方法页面
methodframe = Frame(notebook)
notebook.add(methodframe, text='Method')
###############################################################TypeA##############################################################
TypeA = Frame(methodframe, pady=20)
TypeAlal = Label(TypeA , text='18. Type of analysis',bd=5, font=font_style)
TypeAlal.pack(anchor='w')
TypeA_value = tk.StringVar()
TypeA_value.set(0.0)
TypeA1 = Radiobutton(TypeA, text='Qualitative', variable=TypeA_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
TypeA2 = Radiobutton(TypeA, text='Qualitative and semi quantitative', variable=TypeA_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
TypeA3 = Radiobutton(TypeA, text='Quantitative', variable=TypeA_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

TypeA1.pack(anchor='w', padx=20)
TypeA2.pack(anchor='w', padx=20)
TypeA3.pack(anchor='w', padx=20)

TypeA.grid(row=0, column=0,sticky='w')
priscore18 = tk.StringVar()
priscore18.set(0.0)
pricolor18 = tk.StringVar()
pricolor18.set(0.0)
pripdf18 = tk.StringVar()
pripdf18.set('Qualitative')

def on_TypeA_selected():
    value = TypeA_value.get()

    if value == '3':
        value = 50
        value1 = 1
        pripdf18.set('Quantitative')
    if value == '2':
        value = 30
        value1 = 0.5
        pripdf18.set('Qualitative and semi quantitative')
    if value == '1':
        value = 0
        value1 = 0.0
        pripdf18.set('Qualitative')


    priscore18.set(value)
    pricolor18.set(value1)

    update_picture()


# Set the Radiobutton's callback function
TypeA1.config(command=on_TypeA_selected)
TypeA2.config(command=on_TypeA_selected)
TypeA3.config(command=on_TypeA_selected)
###############################################################way ##############################################################
Waya = Frame(methodframe, pady=20)
Wayalal = Label(Waya , text='19. Multiple or single-element analysis', font=font_style)
Wayalal.pack(anchor='w')
Waya_value = tk.StringVar()
Waya_value.set(0.0)
Waya1 = Radiobutton(Waya, text='Single target per analysis', variable=Waya_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
Waya2 = Radiobutton(Waya, text='Multiple targets analysis for 2-10 compounds per analysis', variable=Waya_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
Waya3 = Radiobutton(Waya, text='Multiple targets analysis for 11-20 compounds per analysis', variable=Waya_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
Waya4 = Radiobutton(Waya, text='Multiple targets analysis for >20 compounds per analysis', variable=Waya_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))

Waya1.pack(anchor='w', padx=20)
Waya2.pack(anchor='w', padx=20)
Waya3.pack(anchor='w', padx=20)
Waya4.pack(anchor='w', padx=20)

Waya.grid(row=1, column=0,sticky='w')
priscore19 = tk.StringVar()
priscore19.set(0.0)
pricolor19 = tk.StringVar()
pricolor19.set(0.0)
pripdf19 = tk.StringVar()
pripdf19.set('Single element analysis')

def on_Waya_selected():
    value = Waya_value.get()

    if value == '1':
        value = 20
        value1 = 0
        pripdf19.set('Single target per analysis')
    if value == '2':
        value = 30
        value1 = 0.25
        pripdf19.set('Multiple targets analysis for 2-10 compounds per analysis')
    if value == '3':
        value = 40
        value1 = 0.5
        pripdf19.set('Multiple targets analysis for 11-20 compounds per analysis')
    if value == '4':
        value = 50
        value1 = 1
        pripdf15.set('Multiple targets analysis for >20 compounds per analysis')





    priscore19.set(value)
    pricolor19.set(value1)

    update_picture()


# Set the Radiobutton's callback function
Waya1.config(command=on_Waya_selected)
Waya2.config(command=on_Waya_selected)
Waya3.config(command=on_Waya_selected)
Waya4.config(command=on_Waya_selected)


# 操作者安全页面
operatorframe = Frame(notebook)
notebook.add(operatorframe, text='Operator Safety')
#########################################################operator########################################
OSframe =Frame(operatorframe, pady=20)
OSheadlal = Label(OSframe, text='Safety factors involved in the experiment\n \nBio-accumulation potential\nPersistence\nFlammability\nOxidazability\nExplosiveness\nCorrosiveness\nRadiation\nCarcinogenicity\nTeratogenicity', font=font_style)
OSheadlal.pack()
OSlal = Label(OSframe, text='20. The number of safety factors involved in the experiment', font=font_style)
OSlal.pack()
OS_value = tk.StringVar()
OS_value.set(0.0)
OS1 = Radiobutton(OSframe, text='0', variable=OS_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
OS2 = Radiobutton(OSframe, text='1', variable=OS_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
OS3 = Radiobutton(OSframe, text='2', variable=OS_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
OS4 = Radiobutton(OSframe, text='≥3', variable=OS_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
OS1.pack(anchor='w', padx=150)
OS2.pack(anchor='w', padx=150)
OS3.pack( anchor='w', padx=150)
OS4.pack( anchor='w', padx=150)
OSframe .grid(row=0, column=0,columnspan=2,sticky='nw')
priscore20 = tk.StringVar()
priscore20.set(0.0)
pricolor20 = tk.StringVar()
pricolor20.set(0.0)
pripdf20 = tk.StringVar()
pripdf20.set('≥3')
def on_OS_selected():
    value = OS_value.get()

    if value == '1':
        value = 100
        value1 = 1.0
        pripdf16.set('0')
    if value == '2':
        value = 50
        value1 = 0.66
        pripdf20.set('1')

    if value == '3':
        value = 25
        value1 = 0.33
        pripdf20.set('2')
    if value == '4':
        value = 0
        value1 = 0.0
        pripdf20.set('≥3')


    priscore20.set(value)
    pricolor20.set(value1)

    update_picture()
OS1.config(command=on_OS_selected)
OS2.config(command=on_OS_selected)
OS3.config(command=on_OS_selected)
OS4.config(command=on_OS_selected)




# 样品分析页面
reagentframe = Frame(notebook)
notebook.add(reagentframe, text='Reagent')
#########################################################reagent########################################
numframe =Frame(reagentframe)
numlal = Label(numframe, text='21. Number of types of reagents\nused in analysis process',bd=5, font=font_style)
numlal.pack(anchor='w')
num_value = tk.StringVar()
num_value.set(0.0)
num1 = Radiobutton(numframe, text='>6', variable=num_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
num2 = Radiobutton(numframe, text='3-6', variable=num_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
num3 = Radiobutton(numframe, text='<3', variable=num_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

num1.pack(anchor='w', padx=20)
num2.pack(anchor='w', padx=20)
num3.pack( anchor='w', padx=20)

numframe .grid(row=0, column=0,columnspan=2,sticky='w')
priscore21 = tk.StringVar()
priscore21.set(0.0)
pricolor21 = tk.StringVar()
pricolor21.set(0.0)
pripdf21 = tk.StringVar()
pripdf21.set('>6')
def on_num_selected():
    value = num_value.get()

    if value == '1':
        value = 0
        value1 = 0.0
        pripdf21.set('>6')
    if value == '2':
        value = 5
        value1 = 0.5
        pripdf21.set('3-6')
    if value == '3':
        value = 10
        value1 = 1
        pripdf21.set('<3')



    priscore21.set(value)
    pricolor21.set(value1)

    update_picture()
num1.config(command=on_num_selected)
num2.config(command=on_num_selected)
num3.config(command=on_num_selected)
####################
Ramount = Frame(reagentframe)
Ramountlal = Label(Ramount, text='22. The amounts of reagents\n used during\nanalytical procedures (mL)',bd=5, font=font_style)
Ramountlal.pack(anchor='e')
def handle_Ramountinvalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    Ramountentry.delete(0, tk.END)

invalidRamount_command = win.register(handle_Ramountinvalid_input)
Ramountname = StringVar()
# Default value setting
Ramountname.set("Unit: mL")
Ramountentry = tk.Entry(Ramount, validate="key", textvariable=Ramountname, validatecommand=(validation, "%P"),
                       invalidcommand=(invalidRamount_command), justify='center', font=('Times New Roman', 10))
priscore22 = tk.DoubleVar()
priscore22.set(0.0)
pricolor22 = tk.DoubleVar()
pricolor22.set(0.0)
pripdf22 = tk.StringVar()
pripdf22.set('0 mL')

def HandleRamount_value():
    # Get the value of the input box


    if Ramountentry.get() == '' or Ramountentry.get() == 'Unit: mL':
        value = 0
    else:
        value = float(Ramountentry.get())
        pripdf22.set(Ramountentry.get()+' RMB')
        if value > 10:

            priscore22.set(0.0)
            pricolor22.set(0.0)


        elif value < 1:

            pricolor22.set(1.0)
            priscore22.set(10)

        elif value >= 1 and value <= 10:
            if(-1/9*(value)+ 10/9<0):
                pricolor22.set(0.0)
                priscore22.set(0.0)
            else:
                pricolor22.set(round((-1/9*(value)+ 10/9), 2))
                priscore22.set(round(-1/9*(value)+ 10/9,2)*10)


    update_picture()


# Input box preselection function
def Ramountdelete():
    if Ramountname.get() == "Unit: mL":
        Ramountentry.delete(0, 'end')


Ramountentry.bind('<FocusIn>', lambda x: Ramountdelete())
Ramountentry.pack(padx=30)
# Create a button that gets the value of the input box when clicked
Ramountbutton = tk.Button(Ramount, text="Confirm", command=HandleRamount_value, font=('Times New Roman', 10))
Ramountbutton.pack(pady=(5, 10),padx=(30,0))
Ramount.grid(row=0, column=1, sticky="e",columnspan=2)






###############################################################Cot##############################################################
Cot = Frame(reagentframe)
Cotlal = Label(Cot  , text='23. Toxicity of reagents',bd=5, font=font_style)
Cotlal.pack(anchor='w')
Cot_value = tk.StringVar()
Cot_value.set(0.0)
Cot1 = Radiobutton(Cot, text='Non-toxic', variable=Cot_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
Cot2 = Radiobutton(Cot, text='Chronic toxicity: (e.g. carcinogenicity, neurotoxicity, teratogenicity,\n and reproductive toxicity associated with the reagent)', variable=Cot_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
Cot3 = Radiobutton(Cot, text='Acute toxicity: (e.g.  irritation and corrosiveness to the eyes, skin, \nand respiratory tract)', variable=Cot_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))

Cot1.pack(anchor='w', padx=20)
Cot2.pack(anchor='w', padx=20)
Cot3.pack(anchor='w', padx=20)

Cot.grid(row=1, column=0,columnspan=2,sticky='nw')
priscore23 = tk.StringVar()
priscore23.set(0.0)
pricolor23 = tk.StringVar()
pricolor23.set(0.0)
pripdf23 = tk.StringVar()
pripdf23.set('Chronic toxicity: (e.g. carcinogenicity, neurotoxicity, teratogenicity,\n and reproductive toxicity associated with the reagent)')

def on_Cot_selected():
    value = Cot_value.get()

    if value == '1':
        value = 30
        value1 = 1
        pripdf23.set(
            'Non-toxic')
    if value == '3':
        value = 0
        value1 = 0.0
        pripdf23.set(
            'Acute toxicity: (e.g.  irritation and corrosiveness to the eyes,\nskin, and respiratory tract)')
    if value == '2':
        value = 15
        value1 = 0.5
        pripdf23.set(
            'Chronic toxicity: (e.g. carcinogenicity, neurotoxicity, teratogenicity,\n and reproductive toxicity associated with the reagent)')


    priscore23.set(value)
    pricolor23.set(value1)

    update_picture()


# Set the Radiobutton's callback function
Cot1.config(command=on_Cot_selected)
Cot2.config(command=on_Cot_selected)
Cot3.config(command=on_Cot_selected)
########################################Dosagetr###############
Dosagetr = Frame(reagentframe)
Dosagetrlal = Label(Dosagetr, text='24. Enter the dosage of\n toxic reagents\n( mg or µL )',bd=5, font=font_style)
Dosagetrlal.pack()


def validate_entry_text(text):
    # Verify that the input text is a floating point number or an integer
    try:
        float(text)
        return True
    except ValueError:
        return False


def handle_invalid_input():
    # Handle inputs that do not satisfy validation conditions
    # Reset the value of the input box
    Dosagetrentry.delete(0, tk.END)


Dosagetrname = StringVar()
# Default value setting
Dosagetrname.set("Unit: mg or µL")
Dosagetrentry = tk.Entry(Dosagetr, validate="key", textvariable=Dosagetrname, validatecommand=(validation, "%P"),
                       invalidcommand=(invalid_command), justify='center', font=('Times New Roman', 10))
priscore24 = tk.DoubleVar()
priscore24.set(0.0)
pricolor24 = tk.DoubleVar()
pricolor24.set(0.0)
pripdf24 = tk.StringVar()
pripdf24.set('0 mg/µL')

def Handle_Dosagetrvalue():
    # Get the value of the input box


    if Dosagetrentry.get() == '' or Dosagetrentry.get() == 'Unit: mg or µL':
        value = 0
    else:
        value = float(Dosagetrentry.get())
        pripdf24.set(Dosagetrentry.get() + ' mg/µL')
        if value > 100000:

            priscore24.set(0.0)
            pricolor24.set(0.0)


        elif value < 10:

            pricolor24.set(1.0)
            priscore24.set(20.0)

        elif value >= 10 and value <= 100000:

            pricolor24.set(round(np.log(1/value)*0.217+2.5, 2)/2)
            priscore24.set(round(np.log(1/value)*0.217+2.5, 2) *10)

    update_picture()


# Input box preselection function
def Dosagetrdelete():
    if Dosagetrname.get() == "Unit: mg or µL":
        Dosagetrentry.delete(0, 'end')


Dosagetrentry.bind('<FocusIn>', lambda x: Dosagetrdelete())
Dosagetrentry.pack()
# Create a button that gets the value of the input box when clicked
Dosagetrbutton = tk.Button(Dosagetr, text="Confirm", command=Handle_Dosagetrvalue, font=('Times New Roman', 10))
Dosagetrbutton.pack(pady=5)
Dosagetr.grid(row=2, column=0,columnspan=2,sticky='w')
#################################################################
Susframe =Frame(reagentframe)
Suslal = Label(Susframe, text='25. Sustainable and renewable reagents',bd=5, font=font_style)
Suslal.pack(anchor='nw')
Sus_value = tk.StringVar()
Sus_value.set(0.0)
Sus1 = Radiobutton(Susframe, text='75-100%', variable=Sus_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
Sus2 = Radiobutton(Susframe, text='50-75%', variable=Sus_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
Sus3 = Radiobutton(Susframe, text='25-50%', variable=Sus_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
Sus4 = Radiobutton(Susframe, text='0-25%', variable=Sus_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))
Sus1.pack(side='left',anchor='nw')
Sus2.pack(side='left',anchor='w')
Sus3.pack(side='left', anchor='w')
Sus4.pack( side='left',anchor='w')
Susframe .grid(row=2, column=1,columnspan=2,sticky='nw')
priscore25 = tk.StringVar()
priscore25.set(0.0)
pricolor25 = tk.StringVar()
pricolor25.set(0.0)
pripdf25 = tk.StringVar()
pripdf25.set('0-25%')
def on_Sus_selected():
    value = Sus_value.get()

    if value == '1':
        value = 30
        value1 = 1.0
        pripdf25.set('75-100%')
    if value == '2':
        value = 15
        value1 = 0.66
        pripdf25.set('50-75%')
    if value == '3':
        value = 10
        value1 = 0.33
        pripdf25.set('25-50%')
    if value == '4':
        value = 0
        value1 = 0.0
        pripdf25.set('0-25%')


    priscore25.set(value)
    pricolor25.set(value1)

    update_picture()
Sus1.config(command=on_Sus_selected)
Sus2.config(command=on_Sus_selected)
Sus3.config(command=on_Sus_selected)
Sus4.config(command=on_Sus_selected)


# 环境页面
environmentframe = Frame(notebook)
notebook.add(environmentframe, text='Waste')
notebook.pack(fill='both', expand=True)

##############################################################Wastedm##############################################################
Wastedm = Frame(environmentframe, pady=5)
Wastedmlal = Label(Wastedm, text='26. Emissions of greenhouse gases or toxic gases',bd=5, font=font_style)
Wastedmlal.pack()
Wastedm_value = tk.StringVar()
Wastedm_value.set(0.0)
Wastedm1 = Radiobutton(Wastedm, text='Yes', variable=Wastedm_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
Wastedm2 = Radiobutton(Wastedm, text='No', variable=Wastedm_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))


Wastedm1.pack(anchor='w', padx=20)
Wastedm2.pack(anchor='w', padx=20)


Wastedm.grid(row=1, column=0,sticky='w')
priscore26 = tk.StringVar()
priscore26.set(0.0)
pricolor26 = tk.StringVar()
pricolor26.set(0.0)
pripdf26 = tk.StringVar()
pripdf26.set('Yes')

def on_Wastedm_selected():
    value = Wastedm_value.get()

    if value == '1':
        value = 0
        value1 = 0
        pripdf26.set('Yes')
    if value == '2':
        value = 50
        value1 = 1
        pripdf26.set('No')
    priscore26.set(value)
    pricolor26.set(value1)

    update_picture()


# Set the Radiobutton's callback function
Wastedm1.config(command=on_Wastedm_selected)
Wastedm2.config(command=on_Wastedm_selected)
##############################################################Noisepollution##############################################################
Noise = Frame(environmentframe, pady=5)
Noiselal = Label(Noise, text='27. Waste disposal (Liquid or Solid)',bd=5, font=font_style)
Noiselal.pack()
Noise_value = tk.StringVar()
Noise_value.set(0.0)

Noise1 = Radiobutton(Noise, text='0-25%', variable=Noise_value, value=1, activeforeground='green',
                     font=('Times New Roman', 10))
Noise2 = Radiobutton(Noise, text='25-50%', variable=Noise_value, value=2, activeforeground='green',
                     font=('Times New Roman', 10))
Noise3 = Radiobutton(Noise, text='50-75%', variable=Noise_value, value=3, activeforeground='green',
                     font=('Times New Roman', 10))
Noise4 = Radiobutton(Noise, text='75-100%', variable=Noise_value, value=4, activeforeground='green',
                     font=('Times New Roman', 10))

Noise1.pack(anchor='w', padx=20)
Noise2.pack(anchor='w', padx=20)
Noise3.pack(anchor='w', padx=20)
Noise4.pack(anchor='w', padx=20)

Noise.grid(row=2, column=0,sticky='w')
priscore27 = tk.StringVar()
priscore27.set(0.0)
pricolor27= tk.StringVar()
pricolor27.set(0.0)
pripdf27 = tk.StringVar()
pripdf27.set('0-25%')

def on_Noise_selected():
    value = Noise_value.get()

    if value == '1':
        value = 0
        value1 = 0
        pripdf27.set('0-25%')
    if value == '2':
        value = 12.5
        value1 = 1
        pripdf27.set('25-50%')
    if value == '3':
        value = 25
        value1 = 0
        pripdf27.set('50-75%')
    if value == '4':
        value = 50
        value1 = 1
        pripdf27.set('75-100%')

    priscore27.set(value)
    pricolor27.set(value1)

    update_picture()


# Set the Radiobutton's callback function
Noise1.config(command=on_Noise_selected)
Noise2.config(command=on_Noise_selected)
Noise3.config(command=on_Noise_selected)
Noise4.config(command=on_Noise_selected)
def update_picture():
    # 右框架
    Score()
    right_frame = Frame(win)
    right_frame.place(relx=0.5, rely=0)
    global fig,SCcolor,SPcolor,Reagentcolor,Environmentcolor,Methodcolor,Economycolor,SAcolor,centercolor
    fig = Figure(figsize=(5, 5), dpi=100)

    ax = fig.add_subplot(111)

    start_color_hex = 'C5161B'
    end_color_hex = '#008843'

    start_color_rgb = hex_to_rgb(start_color_hex)
    end_color_rgb = hex_to_rgb(end_color_hex)

    # 更新颜色字典
    cdict = {
        'red': ((0.0, start_color_rgb[0], start_color_rgb[0]),
                (0.5, 1.0, 1.0),
                (1.0, end_color_rgb[0], end_color_rgb[0])),

        'green': ((0.0, start_color_rgb[1], start_color_rgb[1]),
                  (0.5, 1.0, 1.0),
                  (1.0, end_color_rgb[1], end_color_rgb[1])),

        'blue': ((0.0, start_color_rgb[2], start_color_rgb[2]),
                 (0.5, 1.0, 1.0),
                 (1.0, end_color_rgb[2], end_color_rgb[2]))
    }
    # cdict = {
    #     'red': ((0.0, 1.0, 1.0),  # yellow starting point
    #             (0.5, 1.0, 1.0),  # white starting point
    #             (1.0, 0.5, 0.5)),  # purple terminal point
    #
    #     'green': ((0.0, 1.0, 1.0),  # yellow starting point
    #               (0.5, 1.0, 1.0),  # white starting point
    #               (1.0, 0.0, 0.0)),  # purple terminal point
    #
    #     'blue': ((0.0, 0.0, 0.0),  # yellow starting point
    #              (0.5, 1.0, 1.0),  # white starting point
    #              (1.0, 0.5, 0.5))  # purple terminal point
    # }
    # cdict = {
    #     'red': ((0.0, 0.58, 0.58),  # violet starting point
    #             (0.5, 1.0, 1.0),    # white middle point
    #             (1.0, 0.5, 0.5)),   # yellow-green terminal point
    #
    #     'green': ((0.0, 0.0, 0.0),  # violet starting point
    #               (0.5, 1.0, 1.0),  # white middle point
    #               (1.0, 1.0, 1.0)), # yellow-green terminal point
    #
    #     'blue': ((0.0, 0.83, 0.83), # violet starting point
    #              (0.5, 1.0, 1.0),   # white middle point
    #              (1.0, 0.0, 0.0))   # yellow-green terminal point
    # }
    # cdict = {
    #     'red': ((0.0, 0.0, 0.0),  # black starting point
    #             (0.5, 0.5, 0.5),  # gray middle point
    #             (1.0, 1.0, 1.0)),  # white terminal point
    #
    #     'green': ((0.0, 0.0, 0.0),  # black starting point
    #               (0.5, 0.5, 0.5),  # gray middle point
    #               (1.0, 1.0, 1.0)),  # white terminal point
    #
    #     'blue': ((0.0, 0.0, 0.0),  # black starting point
    #              (0.5, 0.5, 0.5),  # gray middle point
    #              (1.0, 1.0, 1.0))   # white terminal point
    # }

    orange_blue_cmap = mcolors.LinearSegmentedColormap('OrangeBlue', cdict)
    centervmin = 0
    centervmax = 100
    centernorm = Normalize(vmin=centervmin, vmax=centervmax)

    centercolor = mcolors.to_rgb(orange_blue_cmap(centernorm(label_value)))



    # 主圆
    Maxcircle = Circle((0, 0), 5, edgecolor='black', facecolor='none', alpha=1, linewidth=0.5)
    small_circle_radius = 2

    # 主左半圆
    # 大圆参数
    center = (0, 0)
    radius = 5
    SCmin = 0
    SCmax = 100 * w1
    SCnorm = Normalize(vmin=SCmin, vmax=SCmax)
    SCcolor = mcolors.to_rgb(orange_blue_cmap(SCnorm(((float(priscore1.get()) + float(priscore2.get()) + float(
        priscore3.get()) + float(priscore4.get())) * float(w1)))))
    SPmin = 0
    SPmax = 100 * w2
    SPnorm = Normalize(vmin=SPmin, vmax=SPmax)
    SPcolor = mcolors.to_rgb(orange_blue_cmap(SPnorm(((float(priscore5.get()) + float(priscore6.get()) + float(
        priscore7.get()) + float(priscore9.get()) + float(priscore10.get()) + float(priscore8.get())) * float(w2)))))
    Environmentmin = 0
    Environmentmax = 100 * w8
    Environmentnorm = Normalize(vmin=Environmentmin, vmax=Environmentmax)
    Environmentcolor = mcolors.to_rgb(orange_blue_cmap(Environmentnorm(((float(Environmentsum.get()))))))
    Methodmin = 0
    Methodmax = 100 * w5
    Methodnorm = Normalize(vmin=Methodmin, vmax=Methodmax)
    Methodcolor = mcolors.to_rgb(
        orange_blue_cmap(Methodnorm(((float(priscore18.get()) + float(priscore19.get())) * float(w5)))))
    Reagentmin = 0
    Reagentmax = 100 * w7
    Reagentnorm = Normalize(vmin=Reagentmin, vmax=Reagentmax)
    Reagentcolor = mcolors.to_rgb(
        orange_blue_cmap(Reagentnorm(((float(priscore21.get()) + float(priscore22.get()) + float(
            priscore23.get()) + float(priscore24.get()) + float(priscore25.get())) * float(w7)))))
    Operatorcolor = mcolors.to_rgb(orange_blue_cmap(float(pricolor20.get())))

    SAmin = 0
    SAmax = 100 * w3
    SAnorm = Normalize(vmin=SAmin, vmax=SAmax)
    SAcolor = mcolors.to_rgb(orange_blue_cmap(SAnorm(((float(SAsum.get()))))))
    Economycolor = mcolors.to_rgb(orange_blue_cmap(float(pricolor17.get())))
    # 定义每个扇形的颜色列表
    colors = [SPcolor, SCcolor, Environmentcolor,Reagentcolor, Operatorcolor , Methodcolor,Economycolor , SAcolor]

    # 将圆分为8个等分
    num_segments = 8
    angle = 360 / num_segments

    # 存储扇形的列表
    sectors = []

    for i in range(num_segments):
        # 计算每个扇形的起始角度和结束角度
        theta1 = i * angle+22.5
        theta2 = theta1 + angle

        # 创建Wedge对象表示扇形并设置颜色
        sector = Wedge(center, radius, theta1, theta2, edgecolor='black', facecolor=colors[i], linewidth=0.5)
        sectors.append(sector)

    # 添加所有扇形到轴上
    for sector in sectors:
        ax.add_patch(sector)

    # 设置坐标轴范围以确保整个圆可见
    ax.set_xlim(-radius - 1, radius + 1)
    ax.set_ylim(-radius - 1, radius + 1)

    # 确保比例相同，避免变形
    ax.set_aspect('equal')
    small_circle = Circle(center, small_circle_radius, edgecolor='black', facecolor=centercolor, linewidth=0.5)
    ax.add_patch(small_circle)



    # 显示图形



    # 上梯形
    top_leftvertices = [(-2.7, 7), (-0.7, 7), (-0.7, 10), (-3.7, 10)]
    top_midleftvertices = [(-0.7, 7), (0.7, 7), (0.7, 10), (-0.7, 10)]
    top_midrightvertices = [(0.7, 7), (2.1, 7), (2.1, 10), (0.7, 10)]
    top_rightvertices = [(2.1, 7), (2.7, 7), (3.7, 10), (2.1, 10)]
    topvertices = [(-2.7, 7), (-3.7, 10), (3.7, 10), (2.7, 7)]
    # 右上梯形
    righttop_lefttopvertices = [
        (3.2, 6.8),
        (3.8, 6.2),
        (5.8, 8.2),
        (4.2, 9.8),
    ]
    righttop_leftbottomvertices = [
        (3.8, 6.2),
        (5.8, 8.2),
        (6.3, 7.7),
        (4.3, 5.7),
    ]
    righttop_righttopvertices = [
        (4.3, 5.7),
        (6.3, 7.7),
        (7.3, 6.7),
        (5.3, 4.7),
    ]
    righttop_rightmidtopvertices = [
        (5.3, 4.7),
        (7.3, 6.7),
        (8.3, 5.7),
        (6.3, 3.7),
    ]
    righttop_rightbottomvertices = [
        (6.3, 3.7),
        (8.3, 5.7),
        (8.8, 5.2),
        (6.8, 3.2),
    ]
    righttop_rightmidbottomvertices = [
        (6.8, 3.2),
        (8.8, 5.2),

        (9.8, 4.2),
        (6.8, 3.2)
    ]
    righttopvertices = [
        (3.2, 6.8),
        (4.2, 9.8),
        (9.8, 4.2),
        (6.8, 3.2),
    ]
    # 右梯形
    right_mtopvertices = [(7, 1.8), (10, 1.8), (10, 3.7), (7, 2.7)]
    right_topvertices = [(7, 1.8), (10, 1.8), (10, 1.2), (7,1.2)]
    right_midvertices = [(7,  1.2), (10, 1.2), (10, 0), (7,0)]
    right_bottomvertices = [(7, 0), (10,0), (10, -1.2), (7, -1.2)]
    right_mmbottomvertices = [(7, -1.2), (10,-1.2), (10, -1.8), (7, -1.8)]
    right_mbottomvertices = [(7, -1.8), (10, -1.8), (10, -3.7), (7, -2.7)]
    rightvertices = [(7, -2.7), (10, -3.7), (10, 3.7), (7, 2.7)]
    # 右下梯形
    # rightbottom_leftbottomvertices = [
    #     (3.2, -6.8),
    #     (4.1, -5.9),
    #     (6.1, -7.9),
    #     (4.2, -9.8),
    # ]
    # rightbottom_righttopvertices = [
    #     (5.9, -4.1),
    #     (7.9, -6.1),
    #     (9.8, -4.2),
    #     (6.8, -3.2),
    # ]
    # rightbottom_midvertices = [
    #     (4.1, -5.9),
    #     (6.1, -7.9),
    #     (7.9, -6.1),
    #     (5.9, -4.1),
    # ]
    rightbottomvertices = [
        (3.2, -6.8),
        (4.2, -9.8),
        (9.8, -4.2),
        (6.8, -3.2),

    ]
    # 下梯形
    bottom_leftvertices = [(-2.7, -7), (-3.7, -10), (0, -10), (0, -7)]
    bottom_rightvertices = [(2.7, -7), (3.7, -10), (0, -10), (0, -7)]
    bottomvertices = [(-2.7, -7), (-3.7, -10), (3.7, -10), (2.7, -7)]

    # 左上梯形
    lefttop_topvertices = [
        (-3.2, 6.8),
        (-4.2, 9.8),
        (-7, 7),
        (-5, 5),


    ]

    lefttop_midbottomvertices = [
        (-5, 5),
        (-7, 7),
        (-9.8, 4.2),
        (-6.8, 3.2),


    ]

    lefttopvertices = [
        (-3.2, 6.8),
        (-4.2, 9.8),
        (-9.8, 4.2),
        (-6.8, 3.2),

    ]
    # 左下梯形
    leftbottomvertices = [
        (-3.2, -6.8),
        (-4.2, -9.8),
        (-9.8, -4.2),
        (-6.8, -3.2),

    ]

    # 左梯形
    left_topvertices = [(-7, 1.6), (-10, 1.6), (-10, 3.7), (-7, 2.7)]
    left_midtopvertices = [(-7, 0), (-10, 0), (-10, 1.6), (-7, 1.6)]
    left_midvertices = [(-7, -0.8), (-10, -0.8), (-10, 0), (-7, 0)]
    left_midbottomvertices = [(-7, -1.6), (-10, -1.6), (-10, -0.8), (-7, -0.8)]
    left_bottomvertices = [(-7, -2.7), (-10, -3.7), (-10, -1.6), (-7, -1.6)]
    leftvertices = [(-7, -2.7), (-10, -3.7), (-10, 3.7), (-7, 2.7)]
    # 分数输出

    # 上梯形
    top_lefttrapezoid = Polygon(top_leftvertices, closed=True, edgecolor='black',
                                facecolor=orange_blue_cmap(float(pricolor1.get())), alpha=1,
                                linewidth=0.5)
    top_midlefttrapezoid = Polygon(top_midleftvertices, closed=True, edgecolor='black',
                               facecolor=orange_blue_cmap(float(pricolor2.get())), alpha=1,
                               linewidth=0.5)
    top_midrighttrapezoid = Polygon(top_midrightvertices, closed=True, edgecolor='black',
                                    facecolor=orange_blue_cmap(float(pricolor3.get())), alpha=1,
                                    linewidth=0.5)
    top_righttrapezoid = Polygon(top_rightvertices, closed=True, edgecolor='black',
                                 facecolor=orange_blue_cmap(float(pricolor4.get())), alpha=1,
                                 linewidth=0.5)
    toptrapezoid = Polygon(topvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=1)

    # 右上梯形
    righttop_lefttoptrapezoid = Polygon(righttop_lefttopvertices, closed=True, edgecolor='black',
                                        facecolor=orange_blue_cmap(float(pricolor5.get())), alpha=1, linewidth=0.5)
    righttop_leftbottomtrapezoid = Polygon(righttop_leftbottomvertices, closed=True, edgecolor='black',
                                           facecolor=orange_blue_cmap(float(pricolor6.get())), alpha=1, linewidth=0.5)
    righttop_righttoptrapezoid = Polygon(righttop_righttopvertices, closed=True, edgecolor='black',
                                         facecolor=orange_blue_cmap(float(pricolor7.get())), alpha=1, linewidth=0.5)
    righttop_midrighttoptrapezoid = Polygon(righttop_rightmidtopvertices, closed=True, edgecolor='black',
                                         facecolor=orange_blue_cmap(float(pricolor8.get())), alpha=1, linewidth=0.5)

    righttop_rightbottomtrapezoid = Polygon(righttop_rightbottomvertices, closed=True, edgecolor='black',
                                            facecolor=orange_blue_cmap(float(pricolor9.get())), alpha=1, linewidth=0.5)
    righttop_rightmidbottomtrapezoid = Polygon(righttop_rightmidbottomvertices, closed=True, edgecolor='black',
                                            facecolor=orange_blue_cmap(float(pricolor10.get())), alpha=1, linewidth=0.5)
    righttoptrapezoid = Polygon(righttopvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5,
                                linewidth=1)
    # 右梯形
    right_mtoptrapezoid = Polygon(right_mtopvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor11.get())), alpha=1,
                                  linewidth=0.5)
    right_toptrapezoid = Polygon(right_topvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor12.get())), alpha=1,
                                 linewidth=0.5)
    right_midtrapezoid = Polygon(right_midvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor13.get())), alpha=1,
                                 linewidth=0.5)
    right_bottomtrapezoid = Polygon(right_bottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor14.get())),
                                    alpha=1, linewidth=0.5)
    right_mbottomtrapezoid = Polygon(right_mbottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor16.get())),
                                     alpha=1, linewidth=0.5)
    right_mmbottomtrapezoid = Polygon(right_mmbottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor15.get())),
                                     alpha=1, linewidth=0.5)
    righttrapezoid = Polygon(rightvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=1)
    # 右下梯形
    # rightbottom_leftbottomtrapezoid = Polygon(rightbottom_leftbottomvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=0.5)
    # rightbottom_righttoptrapezoid = Polygon(rightbottom_righttopvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=0.5)
    # rightbottom_midtrapezoid= Polygon(rightbottom_midvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=0.5)
    rightbottomtrapezoid = Polygon(rightbottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor17.get())),
                                   alpha=1, linewidth=1)
    # 下梯形
    bottom_lefttrapezoid = Polygon(bottom_leftvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor19.get())),
                                   alpha=1, linewidth=0.5)
    bottom_righttrapezoid = Polygon(bottom_rightvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor18.get())),
                                    alpha=1, linewidth=0.5)
    bottomtrapezoid = Polygon(bottomvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=1)
    # 左下梯形
    leftbottomtrapezoid = Polygon(leftbottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor20.get())), alpha=1,
                                  linewidth=1)
    # 左梯形
    left_toptrapezoid = Polygon(left_topvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor25.get())), alpha=1,
                                linewidth=0.5)
    left_bottomtrapezoid = Polygon(left_bottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor21.get())),
                                   alpha=1, linewidth=0.5)
    left_midtoptrapezoid = Polygon(left_midtopvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor24.get())), alpha=1,
                                linewidth=0.5)
    left_midtrapezoid = Polygon(left_midvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor23.get())), alpha=1,
                                linewidth=0.5)
    left_midbottomtrapezoid = Polygon(left_midbottomvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor22.get())), alpha=1,
                                linewidth=0.5)
    lefttrapezoid = Polygon(leftvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5, linewidth=1)
    # 左上梯形
    lefttop_toptrapezoid = Polygon(lefttop_topvertices, closed=True, edgecolor='black', facecolor=orange_blue_cmap(float(pricolor27.get())),
                                   alpha=1, linewidth=0.5)

    lefttop_midbottomtrapezoid = Polygon(lefttop_midbottomvertices, closed=True, edgecolor='black',
                                         facecolor=orange_blue_cmap(float(pricolor26.get())), alpha=1, linewidth=0.5)


    lefttoptrapezoid = Polygon(lefttopvertices, closed=True, edgecolor='black', facecolor='none', alpha=0.5,
                               linewidth=1)

    # 添加形状到绘图区域

    # ax.add_patch(midcircle)


    ax.add_patch(Maxcircle)

    # 上
    ax.add_patch(top_lefttrapezoid)
    ax.add_patch(top_midlefttrapezoid)
    ax.add_patch(top_midrighttrapezoid)
    ax.add_patch(top_righttrapezoid)
    ax.add_patch(toptrapezoid)
    # 右上
    ax.add_patch(righttop_lefttoptrapezoid)
    ax.add_patch(righttop_leftbottomtrapezoid)
    ax.add_patch(righttop_righttoptrapezoid)
    ax.add_patch(righttop_midrighttoptrapezoid)

    ax.add_patch(righttop_rightbottomtrapezoid)
    ax.add_patch(righttop_rightmidbottomtrapezoid)

    ax.add_patch(righttoptrapezoid)
    # 右
    ax.add_patch(right_mtoptrapezoid)
    ax.add_patch(right_toptrapezoid)
    ax.add_patch(right_midtrapezoid)
    ax.add_patch(right_bottomtrapezoid)
    ax.add_patch(right_mbottomtrapezoid)
    ax.add_patch(right_mmbottomtrapezoid)
    ax.add_patch(righttrapezoid)
    # 右下
    # ax.add_patch(rightbottom_righttoptrapezoid)
    # ax.add_patch(rightbottom_leftbottomtrapezoid)
    # ax.add_patch(rightbottom_midtrapezoid)
    ax.add_patch(rightbottomtrapezoid)
    # 下
    ax.add_patch(bottom_lefttrapezoid)
    ax.add_patch(bottom_righttrapezoid)
    ax.add_patch(bottomtrapezoid)
    # 左下
    ax.add_patch(leftbottomtrapezoid)
    # 左
    ax.add_patch(left_toptrapezoid)
    ax.add_patch(left_midtoptrapezoid)
    ax.add_patch(left_midbottomtrapezoid)
    ax.add_patch(left_midtrapezoid)
    ax.add_patch(left_bottomtrapezoid)

    ax.add_patch(lefttrapezoid)
    # 左上
    ax.add_patch(lefttop_toptrapezoid)

    ax.add_patch(lefttop_midbottomtrapezoid)

    ax.add_patch(lefttoptrapezoid)
    # 序号添加
    tabfontsize = 9
    tabfontweight = 100

    ax.text(0, 3.5,SCsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(0.0, -3.5, Methodsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(2.7, 2.6,SPsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    #
    ax.text(0, 0, label_value, ha='center', va='center', fontsize=20, fontfamily='Times New Roman')
    ax.text(-2.7, 2.6, Environmentsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(2.7, -2.6,Economysum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')

    ax.text(-2.7, -2.6, Operatorsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(3.5, 0.0, SAsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')

    ax.text(-3.5, 0.0, Reagentsum.get(), ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(0, 6, 'C', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(4.2, 4.3, 'P', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(0, -6, 'M', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(-4.2, 4.3, 'W', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(6, 0.0, 'A', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(-4.2, -4.3, 'O', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(4.2, -4.3, 'E', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    ax.text(-6, 0.0, 'R', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    #
    # ax.text(0, 3.5, 'SC', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(2.6, 2.6, 'SP', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(3.5, 0.0, 'A', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(-3.5, 0.0, 'R', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(0, -3.5, 'M', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(-2.6, 2.6, 'SP', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(-2.6, -2.6, 'O', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')
    # ax.text(2.6, -2.6, 'E', ha='center', va='center', fontsize=13, fontfamily='Times New Roman')

    ax.text(-2, 8.5, '1', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(0, 8.5, '2', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(1.4, 8.5, '3', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(2.7, 8.5, '4', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(4.5, 7.8, '5', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(5.1, 7, '6', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(5.8, 6.2, '7', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(6.8, 5.2, '8', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(7.6, 4.5, '9', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(8.3, 4.0, '10', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(8.5, 2.5, '11', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial', fontweight=tabfontweight)
    ax.text(8.5, 1.4, '12', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(8.5, 0.4, '13', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(8.5, -0.8, '14', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)

    ax.text(8.5, -1.6, '15', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(8.5, -2.5, '16', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(6.1, -5.9, '17', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)

    ax.text(-1.5, -8.5, '19', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(1.5, -8.5, '18', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-6.1, -5.9, '20', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-8.5, -2.2, '21', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-8.5, -1.3, '22', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-8.5, -0.5, '23', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-8.5, 0.8, '24', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-8.5, 2.2, '25', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)
    ax.text(-7, 5, '26', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)


    ax.text(-5, 7, '27', ha='center', va='center', fontsize=tabfontsize, fontfamily='Arial',
            fontweight=tabfontweight)

    # 设置绘图区域的范围
    # ax.set_xlim(-12.1, 12.1)
    # ax.set_ylim(-12.1, 12.1)
    ax.set_xlim(-10.1, 10.1)
    ax.set_ylim(-10.1, 10.1)
    # 隐藏坐标轴
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    # 创建一个 FigureCanvasTkAgg 对象
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()

    # 将 FigureCanvasTkAgg 对象嵌入到 Tkinter 窗口中
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def create_colorbar_image():
    fig_colorbar, ax_colorbar = plt.subplots(figsize=(1,3))  # 设置颜色条的尺寸

    start_color_hex = 'C5161B'
    end_color_hex = '#008843'
    start_color_rgb = hex_to_rgb(start_color_hex)
    end_color_rgb = hex_to_rgb(end_color_hex)

    cdict = {
        'red': ((0.0, start_color_rgb[0], start_color_rgb[0]),
                (0.5, 1.0, 1.0),
                (1.0, end_color_rgb[0], end_color_rgb[0])),

        'green': ((0.0, start_color_rgb[1], start_color_rgb[1]),
                  (0.5, 1.0, 1.0),
                  (1.0, end_color_rgb[1], end_color_rgb[1])),

        'blue': ((0.0, start_color_rgb[2], start_color_rgb[2]),
                 (0.5, 1.0, 1.0),
                 (1.0, end_color_rgb[2], end_color_rgb[2]))
    }

    centervmin = 0
    centervmax = 100
    centernorm = Normalize(vmin=centervmin, vmax=centervmax)
    cmap = mcolors.LinearSegmentedColormap('OrangeBlue', cdict)

    # 创建颜色条
    colorbar = plt.colorbar(plt.cm.ScalarMappable(norm=centernorm, cmap=cmap), ax=ax_colorbar, pad=0.1, aspect=20)

    # 设置颜色条位置
    colorbar.ax.set_position([0.4, 0.1, 0.8, 0.8])  # 调整为颜色条的位置和大小
    ticks = [0, 50, 75, 100]
    labels = ['0%', '50%', '75%', '100%']
    colorbar.set_ticks(ticks)
    colorbar.ax.tick_params(labelsize=10)
    colorbar.set_ticklabels(labels)
    # 移除左侧的边框和刻度
    ax_colorbar.spines['left'].set_color('none')
    ax_colorbar.spines['left'].set_linewidth(0)
    ax_colorbar.spines['right'].set_color('none')
    ax_colorbar.spines['right'].set_linewidth(0)
    ax_colorbar.spines['top'].set_color('none')
    ax_colorbar.spines['top'].set_linewidth(0)
    ax_colorbar.spines['bottom'].set_color('none')
    ax_colorbar.spines['bottom'].set_linewidth(0)

    ax_colorbar.set_xticks([])
    ax_colorbar.set_yticks([])

    # Save colorbar with proper path handling
    colorbar_path = os.path.join(os.getcwd(), 'colorbar.png')
    fig_colorbar.savefig(colorbar_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig_colorbar)


def export_pdf():
    global fig

    # Select export path
    export_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

    if export_path:
        # Create the colorbar image
        create_colorbar_image()

        # 创建一个 fig 的深拷贝
        fig_copy = copy.deepcopy(fig)

        # Create a PDF document and specify the export path
        c = cs.Canvas(export_path)
        """
        标题部分
        """
        c.setFont("Times-Roman", 30)
        c.drawString(30, 820,
                     "ESAI")
        c.drawString(30, 790, "PDFreport")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d")
        c.drawString(400, 820, "Created time:")
        c.drawString(410, 790, f"{current_time}")
        
        # Use proper path handling for temporary files
        save_png_path = os.path.join(os.getcwd(), 'save.png')
        colorbar_path = os.path.join(os.getcwd(), 'colorbar.png')
        
        # Clean up old file if exists
        if os.path.exists(save_png_path):
            try:
                os.remove(save_png_path)
            except Exception as e:
                print(f"Warning: Could not remove old save.png: {e}")

        if not hasattr(fig_copy, '_colorbar_drawn'):
            # Your existing colorbar creation code...
            start_color_hex = 'C5161B'
            end_color_hex = '#008843'
            start_color_rgb = hex_to_rgb(start_color_hex)
            end_color_rgb = hex_to_rgb(end_color_hex)
            cdict = {
                'red': ((0.0, start_color_rgb[0], start_color_rgb[0]),
                        (0.5, 1.0, 1.0),
                        (1.0, end_color_rgb[0], end_color_rgb[0])),

                'green': ((0.0, start_color_rgb[1], start_color_rgb[1]),
                          (0.5, 1.0, 1.0),
                          (1.0, end_color_rgb[1], end_color_rgb[1])),

                'blue': ((0.0, start_color_rgb[2], start_color_rgb[2]),
                         (0.5, 1.0, 1.0),
                         (1.0, end_color_rgb[2], end_color_rgb[2]))
            }
            centervmin = 0
            centervmax = 100
            centernorm = Normalize(vmin=centervmin, vmax=centervmax)
            cmap = mcolors.LinearSegmentedColormap('OrangeBlue', cdict)
            # colorbar = plt.cm.ScalarMappable(norm=centernorm, cmap=cmap)
            #
            # # Create a new axis for the colorbar with adjusted position
            # cax = fig_copy.add_axes([0.85, 0.1, 0.03, 0.8])  # 调整这些值以适应你的布局
            # cbar = fig_copy.colorbar(colorbar, cax=cax, pad=0.1, aspect=10)

            # ticks = [0, 50, 75, 100]
            # labels = ['', '', '', '']
            # cbar.set_ticks(ticks)
            # cbar.ax.tick_params()
            # cbar.set_ticklabels(labels)



        fig_copy.tight_layout(pad=3.0)
        fig_copy.savefig(save_png_path, dpi=300, bbox_inches='tight')

        # Open the image file
        img = Image.open(save_png_path)
        img_width, img_height = img.size

        # Define the maximum width and height for the image in the PDF
        max_width = 200
        max_height = 250

        # Calculate the scaling factor to maintain the aspect ratio
        scaling_factor = min(max_width / img_width, max_height / img_height)

        # Calculate the new dimensions of the image
        new_width = img_width * scaling_factor
        new_height = img_height * scaling_factor

        # Draw the image on the canvas at the desired position
        c.drawImage(save_png_path, 130, 590, new_width, new_height)  # Adjust x and y position if needed
        
        # Draw colorbar if it exists
        if os.path.exists(colorbar_path):
            c.drawImage(colorbar_path, 390, 590, width=50, height=190)  # Adjust x and y position if needed
        else:
            print(f"Warning: Colorbar image not found at {colorbar_path}")
        weightdata = [
            ["Weights of each module", "", "", "", "", "", "", ""],
            ["SC", "SP", "SA", "Economy", "Method", "Operator Safety", "Reagent", "Environment"],
            ["%.2f"%w1, "%.2f"%w2, "%.2f"%w3, "%.2f"%w4, "%.2f"%w5, "%.2f"%w6, "%.2f"%w7, "%.2f"%w8 ],
            ["Score for each principle", "", "", "", "", "", "", ""],
            ["NO.", "Principle", "", "", "", "", "", "Score"],
            ["1", "Sample collection site", "", "", "", "", "", "%.2f"%(float(priscore1.get())*float(w1))],
            ["2", "Volume of sample collection ", "", "", "", "", "", "%.2f"%(float(priscore2.get())*float(w1))],
            ["3", "Throughput of sample collection", "", "", "", "", "", "%.2f"%(float(priscore3.get())*float(w1))],
            ["4", "Energy consumption for sample collection", "", "", "", "", "", "%.2f"%(float(priscore4.get())*float(w1))],
            ["5", "Method of sample preparation", "", "", "", "", "", "%.2f"%(float(priscore5.get())*float(w2))],
            ["6", "Throughput of sample preparation", "", "", "", "", "", "%.2f"%(float(priscore6.get())*float(w2))],
            ["7", "The amounts of wastes generated during sample preparation", "", "", "", "", "", "%.2f"%(float(priscore7.get())*float(w2))],
            ["8", "The number of steps and the degree of automation in sample preparation", "", "", "", "", "", "%.2f"%(float(priscore8.get())*float(w2))],
            ["9", "Energy consumption for sample preparation", "", "", "", "", "", "%.2f"%(float(priscore9.get())*float(w2))],
            ["10", "Volume consumed for sample preparation", "", "", "", "", "","%.2f"%(float(priscore10.get())*float(w2))],
            ["11", "Instrument", "", "", "", "", "", "%.2f"%(float(priscore11.get())*float(w3))],
            ["12", "Volume of injection", "", "", "", "", "","%.2f"%(float(priscore12.get())*float(w3))],
            ["13", "Throughput of analysis", "", "", "", "", "", "%.2f"%(float(priscore13.get())*float(w3))],
            ["14", "The amounts of wastes generated during analysis", "", "", "", "", "", "%.2f"%(float(priscore14.get())*float(w3))],
            ["15", "The degree of automation for analysis", "", "", "", "", "", "%.2f"%(float(priscore15.get())*float(w3))],
            ["16", "Consumption of energy during analysis", "", "", "", "", "", "%.2f"%(float(priscore16.get())*float(w3))],
            ["17", "Number of types of reagents used in analysis process", "", "", "", "", "", "%.2f"%(float(priscore17.get())*float(w4))],
            ["18", "The amounts of reagents used during analytical procedures", "", "", "", "", "", "%.2f"%(float(priscore17.get())*float(w5))],
            ["19", "Toxicity of reagents", "", "", "", "", "", "%.2f"%(float(priscore19.get())*float(w5))],
            ["20", "The quantity of toxic reagents used in the analysis process", "", "", "", "", "", "%.2f"%(float(priscore20.get())*float(w6))],
            ["21", "Sustainable and renewable reagents", "", "", "", "", "", "%.2f"%(float(priscore21.get())*float(w7))],
            ["22", "Type of analysis", "", "", "", "", "","%.2f"%(float(priscore22.get())*float(w7))],
            ["23", "Multiple or single-element analysis", "", "", "", "", "", "%.2f"%(float(priscore23.get())*float(w7))],
            ["24", "The number of safety factors involved in the experiment", "", "", "", "", "",
             "%.2f" % (float(priscore24.get()) * float(w7))],
            ["25", "The cost of analysis for per sample", "", "", "", "", "",
             "%.2f" % (float(priscore21.get()) * float(w7))],
            ["26", "Emissions of greenhouse gases or toxic gases", "", "", "", "", "", "%.2f" % (float(priscore22.get()) * float(w8))],
            ["27", "Waste disposal", "", "", "", "", "",
             "%.2f" % (float(priscore23.get()) * float(w8))],
        ]
        mpl_color1 = mcolors.to_rgb(orange_blue_cmap(float(pricolor1.get())))
        mpl_color2 = mcolors.to_rgb(orange_blue_cmap(float(pricolor2.get())))
        mpl_color3 = mcolors.to_rgb(orange_blue_cmap(float(pricolor3.get())))
        mpl_color4 = mcolors.to_rgb(orange_blue_cmap(float(pricolor4.get())))
        mpl_color5 = mcolors.to_rgb(orange_blue_cmap(float(pricolor5.get())))
        mpl_color6 = mcolors.to_rgb(orange_blue_cmap(float(pricolor6.get())))
        mpl_color7 = mcolors.to_rgb(orange_blue_cmap(float(pricolor7.get())))
        mpl_color8 = mcolors.to_rgb(orange_blue_cmap(float(pricolor8.get())))
        mpl_color9 = mcolors.to_rgb(orange_blue_cmap(float(pricolor9.get())))
        mpl_color10 = mcolors.to_rgb(orange_blue_cmap(float(pricolor10.get())))
        mpl_color11 = mcolors.to_rgb(orange_blue_cmap(float(pricolor11.get())))
        mpl_color12 = mcolors.to_rgb(orange_blue_cmap(float(pricolor12.get())))
        mpl_color13 = mcolors.to_rgb(orange_blue_cmap(float(pricolor13.get())))
        mpl_color14 = mcolors.to_rgb(orange_blue_cmap(float(pricolor14.get())))
        mpl_color15 = mcolors.to_rgb(orange_blue_cmap(float(pricolor15.get())))
        mpl_color16 = mcolors.to_rgb(orange_blue_cmap(float(pricolor16.get())))
        mpl_color17 = mcolors.to_rgb(orange_blue_cmap(float(pricolor17.get())))
        mpl_color18 = mcolors.to_rgb(orange_blue_cmap(float(pricolor18.get())))
        mpl_color19 = mcolors.to_rgb(orange_blue_cmap(float(pricolor19.get())))
        mpl_color20 = mcolors.to_rgb(orange_blue_cmap(float(pricolor20.get())))
        mpl_color21 = mcolors.to_rgb(orange_blue_cmap(float(pricolor21.get())))
        mpl_color22 = mcolors.to_rgb(orange_blue_cmap(float(pricolor22.get())))
        mpl_color23 = mcolors.to_rgb(orange_blue_cmap(float(pricolor23.get())))
        mpl_color24 = mcolors.to_rgb(orange_blue_cmap(float(pricolor24.get())))
        mpl_color25 = mcolors.to_rgb(orange_blue_cmap(float(pricolor25.get())))
        mpl_color26 = mcolors.to_rgb(orange_blue_cmap(float(pricolor26.get())))
        mpl_color27 = mcolors.to_rgb(orange_blue_cmap(float(pricolor27.get())))
        SCmin = 0
        SCmax = 100*w1
        SCnorm = Normalize(vmin=SCmin, vmax=SCmax)

        SCcolor = mcolors.to_rgb(orange_blue_cmap(SCnorm(((float(priscore1.get())+float(priscore2.get())+float(priscore3.get())+float(priscore4.get()))*float(w1)))))

        SPmin = 0
        SPmax = 100 * w2
        SPnorm = Normalize(vmin=SPmin, vmax=SPmax)
        SPcolor = mcolors.to_rgb(orange_blue_cmap(SPnorm(((float(priscore5.get())+float(priscore6.get())+float(priscore7.get())+float(priscore9.get())+float(priscore10.get())+float(priscore8.get()))*float(w2)))))







        Environmentmin = 0
        Environmentmax = 100 * w8
        Environmentnorm = Normalize(vmin=Environmentmin, vmax=Environmentmax)
        Environmentcolor = mcolors.to_rgb(orange_blue_cmap( Environmentnorm(((float( Environmentsum.get()))))))



        weightstyle = TableStyle([
            ("BACKGROUND", (7, 5), (7, 5),mpl_color1),
            ("BACKGROUND", (7, 6), (7, 6), mpl_color2),
            ("BACKGROUND", (7, 7), (7, 7), mpl_color3),
            ("BACKGROUND", (7, 8), (7, 8), mpl_color4),
            ("BACKGROUND", (7, 9), (7, 9), mpl_color5),
            ("BACKGROUND", (7, 10), (7, 10), mpl_color6),
            ("BACKGROUND", (7, 11), (7, 11), mpl_color7),
            ("BACKGROUND", (7, 12), (7, 12), mpl_color8),
            ("BACKGROUND", (7, 13), (7, 13), mpl_color9),
            ("BACKGROUND", (7, 14), (7, 14), mpl_color10),
            ("BACKGROUND", (7, 15), (7, 15), mpl_color11),
            ("BACKGROUND", (7, 16), (7, 16), mpl_color12),
            ("BACKGROUND", (7, 17), (7, 17), mpl_color13),
            ("BACKGROUND", (7, 18), (7, 18), mpl_color14),
            ("BACKGROUND", (7, 19), (7, 19), mpl_color15),
            ("BACKGROUND", (7, 20), (7, 20), mpl_color16),
            ("BACKGROUND", (7, 21), (7, 21), mpl_color17),
            ("BACKGROUND", (7, 22), (7, 22), mpl_color18),
            ("BACKGROUND", (7, 23), (7, 23), mpl_color19),
            ("BACKGROUND", (7, 24), (7, 24), mpl_color20),
            ("BACKGROUND", (7, 25), (7, 25), mpl_color21),
            ("BACKGROUND", (7, 26), (7, 26), mpl_color22),
            ("BACKGROUND", (7, 27), (7, 27), mpl_color23),
            ("BACKGROUND", (7, 28), (7, 28), mpl_color24),
            ("BACKGROUND", (7, 29), (7, 29), mpl_color25),
            ("BACKGROUND", (7, 30), (7, 30), mpl_color26),
            ("BACKGROUND", (7, 31), (7, 31), mpl_color27),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
            ('SPAN', (0, 0), (7, 0)),
            ('SPAN', (0, 3), (7, 3)),
            ('SPAN', (1, 4), (6, 4)),
            ('SPAN', (1, 5), (6, 5)),
            ('SPAN', (1, 6), (6, 6)),
            ('SPAN', (1, 7), (6, 7)),
            ('SPAN', (1, 8), (6, 8)),
            ('SPAN', (1, 9), (6, 9)),
            ('SPAN', (1, 10), (6,10)),
            ('SPAN', (1, 11), (6, 11)),
            ('SPAN', (1, 12), (6, 12)),
            ('SPAN', (1, 13), (6, 13)),
            ('SPAN', (1, 14), (6, 14)),
            ('SPAN', (1, 15), (6, 15)),
            ('SPAN', (1, 16), (6, 16)),
            ('SPAN', (1, 17), (6, 17)),
            ('SPAN', (1, 18), (6, 18)),
            ('SPAN', (1, 19), (6, 19)),
            ('SPAN', (1, 20), (6, 20)),
            ('SPAN', (1, 21), (6, 21)),
            ('SPAN', (1, 22), (6, 22)),
            ('SPAN', (1, 23), (6, 23)),
            ('SPAN', (1, 24), (6, 24)),
            ('SPAN', (1, 25), (6, 25)),
            ('SPAN', (1, 26), (6, 26)),
            ('SPAN', (1, 27), (6, 27)),
            ('SPAN', (1, 28), (6, 28)),
            ('SPAN', (1, 29), (6, 29)),
            ('SPAN', (1, 30), (6, 30)),
            ('SPAN', (1, 31), (6, 31)),
            ("FONTSIZE", (1, 4), (6, 4), 12),
            ("FONTSIZE", (0, 3), (-1, 3), 12),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ])

        weightcol_widths = [30, 30, 30, 60, 60,100,60,100]
        weighttable = Table(weightdata,colWidths=weightcol_widths)

        weighttable.setStyle(weightstyle)
        weighttable.wrapOn(c, 400, 200)
        weighttable.drawOn(c, 60, 10)
        c.showPage()

        beforecol_widths = [117.5,117.5,117.5,117.5]
        beforedata=[
            ['\nESAI PDF\n','','',''],

            ['\nSample collection\n', '', '', ''],
            ['1. Sample collection site', '2. Volume of sample\ncollection', '3. Throughput of\nsample collection', '4. Energy consumption\nfor sample collection'],
            ['%s'%pripdf1.get(), '%s'%pripdf2.get(),'%s'%pripdf3.get(), '%s'%pripdf4.get()],
            ['SC score', '', '%0.2f'%((float(priscore1.get())+float(priscore2.get())+float(priscore3.get()))*float(w1)), ''],
            ['\nSample preparation\n', '', '', ''],
            ['5. Method of sample preparation ', '', '', ''],
            ['%s'%pripdf5.get(), '', '', ''],
            ['6. Throughput\nof sample\npreparation', '7. The amount of\nwaste generated\nduring sample\npreparation', '8(1). The number of\nsteps in sample\npreparation', '8(2). The degree of\nautomation in sample\npreparation'],
            ['%s'%pripdf6.get(), '%s'%pripdf7.get(), '%s'%pripdf81.get(), '%s'%pripdf82.get()],
            ['9. Energy consumption for sample preparation', '', '10. Volume consumed for sample preparation', ''],
            ['%s' % pripdf9.get(), '', '%s' % pripdf10.get(), ''],
            ['SP score', '', '%0.2f'%((float(priscore5.get())+float(priscore6.get())+float(priscore9.get())+float(priscore10.get())+float(priscore7.get())+float(priscore8.get()))*float(w2)), ''],

            ['\nAnalysis technology\n', '', '', ''],
            ['11. Sample analysis instrument', '', '', ''],
            ['%s' % pripdf11.get(), '', '', ''],
            ['12. Volume of injection', '13. Throughput of analysis',
             '14. The amount of waste generated\n during sample analysis',
             '15. The degree\nof automation\nfor analysis'],
            ['%s' % pripdf12.get(), '%s' % pripdf13.get(), '%s' % pripdf14.get(), ''],
            ['15. The degree\nof automation\nfor analysis', '', '16. Consumption of energy during analysis', '', ],
            ['%s' % pripdf15.get(), '', '%s' % pripdf16.get(), ''],
            ['AT score', '', '%.2f' % float(SAsum.get()), ''],

            ['\nEconomy\n', '', '', ''],
            ['17. The cost of analysis for per sample', '', '', ''],
            ['%s' % pripdf17.get(), '', '', ''],
            ['Economy score', '', '%.2f' % float(priscore17.get()), ''],


            ]
        beforestyle= TableStyle([
            ('SPAN', (0, 0), (3, 0)),  # 合并第一行的所有单元格

            # 合并第二行的单元格





            ("BACKGROUND", (2, 4), (2, 4), SCcolor),
            ("BACKGROUND", (0, 7), (0, 7), mpl_color5),
            ("BACKGROUND", (0, 9), (0, 9), mpl_color6),
            ("BACKGROUND", (1, 9), (1, 9), mpl_color7),
            ("BACKGROUND", (2, 9), (2, 9), mpl_color8),
            ("BACKGROUND", (3, 9), (3, 9), mpl_color8),
            ("BACKGROUND", (0, 11), (0, 11), mpl_color9),
            ("BACKGROUND", (2, 11), (2, 11), mpl_color8),
            ("BACKGROUND", (2, 12), (2, 12), SPcolor),

            ("BACKGROUND", (0, 15), (0, 15), mpl_color11),
            ("BACKGROUND", (0, 17), (0, 17), mpl_color12),
            ("BACKGROUND", (1, 17), (1, 17), mpl_color13),
            ("BACKGROUND", (2, 17), (2, 17), mpl_color14),
            ("BACKGROUND", (0, 19), (0,19), mpl_color15),
            ("BACKGROUND", (2, 19), (2, 19), mpl_color16),
            ("BACKGROUND", (2, 20), (2, 20), SAcolor),

            ("BACKGROUND", (0, 23), (0, 23), mpl_color17),
            ("BACKGROUND", (2, 24), (2, 24), mpl_color17),



            ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),

            ('SPAN', (0, 1), (3, 1)),

            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (2, 4), (3, 4)),

            ('SPAN', (0, 5), (3, 5)),
            ('SPAN', (0, 6), (3, 6)),
            ('SPAN', (0, 7), (3, 7)),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (2, 10), (3, 10)),
            ('SPAN', (0, 11), (1, 11)),
            ('SPAN', (2, 11), (3, 11)),

            ('SPAN', (0, 12), (1, 12)),
            ('SPAN', (2, 12), (3, 12)),

            ('SPAN', (0, 13), (3, 13)),
            ('SPAN', (0, 14), (3, 14)),
            ('SPAN', (0, 15), (3, 15)),
            ('SPAN', (2, 16), (3, 16)),
            ('SPAN', (2, 17), (3, 17)),
            ('SPAN', (0, 18), (1, 18)),
            ('SPAN', (2, 18), (3, 18)),
            ('SPAN', (0, 19), (1, 19)),
            ('SPAN', (2, 19), (3, 19)),
            ('SPAN', (0, 20), (1, 20)),
            ('SPAN', (2, 20), (3, 20)),

            ('SPAN', (0, 21), (3, 21)),
            ('SPAN', (0, 22), (3, 22)),
            ('SPAN', (0, 23), (3, 23)),

            ('SPAN', (0, 24), (1, 24)),
            ('SPAN', (2, 24), (3, 24)),






            ("FONTSIZE", (0, 21), (3, 21), 12),
            ("FONTSIZE", (0, 13), (3, 13), 12),
            ("FONTSIZE", (0, 5), (3, 5), 12),
            ("FONTSIZE", (0, 1), (3, 1), 12),
            ("FONTSIZE", (0, 0), (0, 0), 14),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        beforetable = Table(beforedata, colWidths=beforecol_widths, rowHeights=[30] + [None] * (len(beforedata) - 1))

        beforetable.setStyle(beforestyle)
        beforetable.wrapOn(c, 400, 200)
        beforetable.drawOn(c, 60, 80)
        c.showPage()
        aftercol_widths = [117.5, 117.5, 117.5, 117.5]
        afterdata = [

            ['\nMethod\n', '', '', ''],
            ['18. Type of analysis', '', '19. Multiple or single-element analysis', ''],
            ['%s'%pripdf18.get(), '', '%s'%pripdf19.get(), ''],
            ['Method score', '', '%0.2f' % ((float(priscore18.get()) + float(priscore19.get())) * float(w5)), ''],

            ['\nSafety of operator\n', '', '', ''],
            ['20. The number of safety factors involved in the experiment', '', '', ''],
            ['%s' % pripdf20.get(), '', '', ''],
            ['Operator score', '', '%.2f' % float(priscore20.get()), ''],

            ['\nReagent\n', '', '', ''],
            ['21. Number of types of reagents\nused in analysis process', '', '22. The amounts of reagents used\nduring analytical procedures', ''],
            ['%s'%pripdf21.get(), '', '%s'%pripdf22.get(), ''],
            ['23. Toxicity of reagents', '', '', ''],
            ['%s'%pripdf23.get(), '', '', ''],
            ['24. The quantity of toxic reagents\nused in the analysis process', '',
             '25. Sustainable and renewable reagents', ''],
            ['%s' % pripdf24.get(), '', '%s' % pripdf25.get(), ''],
            ['Reagent score', '', '%0.2f'%((float(priscore21.get())+float(priscore22.get())+float(priscore23.get())+float(priscore24.get())+float(priscore25.get()))*float(w7)), ''],



            ['\nWaste disposal\n', '', '', ''],
            ['26. Emissions of\n greenhouse gases or\n toxic gases', '', '27. Waste disposal ', ''],
            ['%s'%pripdf26.get(), '', '%s'%pripdf27.get(), ''],
            ['Waste score', '', '%.2f'%float(Environmentsum.get()), ''],
            ['Total', '', '%.2f'%float(label_value),''],
            ]

        afterstyle = TableStyle([
            ('SPAN', (0, 0), (3, 0)),  # 合并第一行的所有单元格
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (2, 1), (3,1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (2, 2), (3, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (2, 3), (3, 3)),

            ('SPAN', (0, 4), (3, 4)),
            ('SPAN', (0, 5), (3, 5)),
            ('SPAN', (0, 6), (3, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('SPAN', (2, 7), (3, 7)),

            ('SPAN', (0, 8), (3, 8)),
            ('SPAN', (0, 9), (1, 9)),
            ('SPAN', (2, 9), (3, 9)),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (2, 10), (3, 10)),

            ('SPAN', (0, 11), (3, 11)),
            ('SPAN', (0, 12), (3, 12)),

            ('SPAN', (0, 13), (1, 13)),
            ('SPAN', (2, 13), (3, 13)),
            ('SPAN', (0, 14), (1, 14)),
            ('SPAN', (2, 14), (3, 14)),
            ('SPAN', (0, 15), (1, 15)),
            ('SPAN', (2, 15), (3, 15)),





            ('SPAN', (0, 16), (3, 16)),
            ('SPAN', (0, 17), (1, 17)),
            ('SPAN', (2, 17), (3, 17)),
            ('SPAN', (0, 18), (1, 18)),
            ('SPAN', (2, 18), (3, 18)),
            ('SPAN', (0, 19), (1, 19)),
            ('SPAN', (2, 19), (3, 19)),
            ('SPAN', (0, 20), (1, 20)),
            ('SPAN', (2, 20), (3, 20)),

            ("BACKGROUND", (0, 2), (0, 2), mpl_color18),
            ("BACKGROUND", (2, 2), (2, 2), mpl_color19),
            ("BACKGROUND", (2, 3), (2, 3), Methodcolor),
            ("BACKGROUND", (2, 7), (2, 7), mpl_color20),

            ("BACKGROUND", (0, 10), (0, 10), mpl_color21),
            ("BACKGROUND", (2, 10), (2, 10), mpl_color22),
            ("BACKGROUND", (0, 12), (0, 12), mpl_color23),
            ("BACKGROUND", (0, 14), (0, 14), mpl_color24),
            ("BACKGROUND", (2, 14), (2, 14), mpl_color25),
            ("BACKGROUND", (2, 15), (2, 15), Reagentcolor),


            ("BACKGROUND", (0, 18), (0, 18), mpl_color26),

            ("BACKGROUND", (2, 18), (2, 18), mpl_color27),

            ("BACKGROUND", (2, 19), (2, 19), Environmentcolor),
            ("BACKGROUND", (2, 20), (2, 20), centercolor),


            ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 4), (3, 4), 12),
            ("FONTSIZE", (0, 16), (3, 16), 12),
            ("FONTSIZE", (0, 8), (3, 8), 12),
            ("FONTSIZE", (0, 20), (3, 20), 12),
            ("FONTSIZE", (0, 0), (0, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
        aftertable = Table(afterdata, colWidths=aftercol_widths, rowHeights=[30] + [None] * (len(afterdata) - 1))

        aftertable.setStyle(afterstyle)
        aftertable.wrapOn(c, 400, 200)
        aftertable.drawOn(c, 60, 200)
        c.save()

        tk.messagebox.showinfo("Export pdf", f"PDF exported to: {export_path}")


if not Exportpdf:
    filemenu.add(itemType="command", label="Generate reports", command=export_pdf)
    Exportpdf = True




update_picture()
Score()

# Apply styling based on availability of ttkbootstrap
if USE_TTKBOOTSTRAP:
    try:
        style = ttkbootstrap.Style("yeti")
        style.configure('TNotebook.Tab', font=('Times New Roman', 10))
    except Exception as e:
        print(f"Warning: Failed to apply ttkbootstrap style: {e}")
        # Fallback to standard ttk styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Times New Roman', 10))
else:
    # Use standard ttk styling
    style = ttk.Style()
    try:
        style.theme_use('clam')  # Use a modern-looking theme if available
    except:
        pass
    style.configure('TNotebook.Tab', font=('Times New Roman', 10))

win.mainloop()
