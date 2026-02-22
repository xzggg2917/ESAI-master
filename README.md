# ESAI - Environmental Suitability Assessment Index

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive software tool for evaluating the environmental suitability and greenness of analytical methods based on Green Analytical Chemistry (GAC) principles.

> **中文文档**: 查看 [README-CN.md](README-CN.md) 获取中文版本文档  
> **Chinese Version**: See [README-CN.md](README-CN.md) for Chinese documentation

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Installation](#step-by-step-installation)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [GUI Overview](#gui-overview)
- [Documentation](#documentation)
- [Dependencies](#dependencies)
- [License](#license)
- [Citation](#citation)
- [Contributors](#contributors)
- [Support](#support)

## 🔬 Overview

**ESAI (Environmental Suitability Assessment Index)** is a new metric for assessing the greenness of analytical methods. Green analytical chemistry (GAC) seeks to reduce the environmental and health impacts of analytical procedures. Evaluating the greenness of analytical methods requires a holistic approach, considering reagents, energy use, waste generation, instrumentation, and cost.

This software integrates:
- **12 Green Analytical Chemistry (GAC) principles**
- **10 Sample Preparation principles**
- **Eight-dimensional evaluation framework**:
  1. Sample Collection (SC)
  2. Sample Preparation (SP)
  3. Analytical Technique (AT)
  4. Reagents
  5. Method Performance
  6. Operational Safety
  7. Economic Evaluation
  8. Waste Disposal

The assessment results are visualized through an **octagonal radar chart** with color gradients and quantitative scores representing greenness levels.

### Authors

Jiye Tian<sup>a#</sup>, Hongwei Zheng<sup>a#</sup>, Yongshan Ai<sup>a#</sup>, Tong Xin<sup>a#</sup>, Jiansong You<sup>c</sup>, Hongyu Xue<sup>b*</sup>, Lei Yin<sup>b**</sup>, Meiyun Shi<sup>a,b,c*</sup>

<sup>a</sup> Cancer Hospital of Dalian University of Technology, Dalian University of Technology, Shenyang, 110042, China  
<sup>b</sup> School of Chemical Engineering, Ocean and Life Sciences, Dalian University of Technology, Panjin, P.R. China  
<sup>c</sup> Aim Honesty Biopharmaceutical Co. LTD, Dalian, P.R. China

**Correspondence:**
- Meiyun Shi: shimy@dlut.edu.cn
- Lei Yin: leiyin@dlut.edu.cn

## ✨ Features

- **Comprehensive Assessment**: 27 weighted criteria across 8 dimensions
- **Interactive GUI**: User-friendly graphical interface built with tkinter
- **Visual Results**: Octagonal radar charts with color-coded greenness indicators
- **PDF Reports**: Automated generation of detailed assessment reports
- **Customizable Weights**: Adjust importance of different assessment dimensions
- **Tooltips & Help**: Context-sensitive help throughout the interface
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer, included with Python)
- **tkinter** (usually pre-installed with Python)

### Step-by-Step Installation

#### 1. Verify Python Installation

Open a terminal/command prompt and check your Python version:

```bash
python --version
```

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

#### 2. Clone or Download the Repository

```bash
git clone https://github.com/xzggg2917/ESAI-master.git
cd ESAI-master
```

Or download the ZIP file and extract it.

#### 3. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- **Pillow** (≥10.0.0) - Image processing
- **numpy** (≥1.24.0) - Numerical computations
- **matplotlib** (≥3.7.0) - Data visualization
- **reportlab** (≥4.0.0) - PDF generation

#### 5. Verify Installation

Run the test suite to ensure everything is set up correctly:

```bash
python test_exec_removal.py
python test_font_compatibility.py
python test_locale_compatibility.py
```

All tests should pass without errors.

## 📖 Usage

### Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd ESAI-master
   ```

2. **Activate the virtual environment** (if created):
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. **Launch the application:**
   ```bash
   python run_esai.py
   ```

4. **Follow the GUI workflow:**
   - Set dimension weights in the "Weight" tab
   - Answer questions in each assessment tab (SC, SP, AT, etc.)
   - View real-time radar chart updates
   - Export PDF reports

### GUI Overview

The application consists of the following tabs:

| Tab | Description |
|-----|-------------|
| **Weight** | Configure importance weights for 8 assessment dimensions |
| **SC** | Sample Collection evaluation |
| **SP** | Sample Preparation assessment |
| **AT** | Analytical Technique evaluation |
| **Reagent** | Reagent usage and environmental impact |
| **Method** | Method performance characteristics |
| **Operator** | Operational safety considerations |
| **Economy** | Economic evaluation and cost analysis |
| **Waste** | Waste disposal and management |

**Key Features:**
- **Hover over any element** to see tooltips with helpful information
- **"?" buttons** provide detailed help for each section
- **Real-time visualization**: Radar chart updates as you input data
- **Export function**: Generate comprehensive PDF reports

## 📚 Documentation

### File Structure

```
ESAI-master/
├── esai/                  # Main package directory
│   ├── tabs/              # Individual assessment tabs
│   ├── ui/                # UI components and styling
│   ├── config.py          # Configuration management
│   ├── main.py            # Application entry point
│   ├── scoring.py         # Score calculation logic
│   ├── visualization.py   # Radar chart generation
│   └── report.py          # PDF report generation
├── run_esai.py            # Application launcher
├── requirements.txt       # Package dependencies
├── LICENSE                # MIT License
├── README.md              # This file
└── test_*.py              # Test suite files
```

### Assessment Scoring

Each dimension is scored on a scale based on:
- **Question responses**: Radio buttons and numerical inputs
- **Weighted importance**: User-defined or default weights
- **Color coding**: Red (poor) → Yellow → Green (excellent)

Final scores are displayed both numerically and visually in the radar chart.

### PDF Report Contents

Generated reports include:
- Assessment date and metadata
- Octagonal radar chart visualization
- Dimension weights table
- Detailed scores for all 27 principles
- Color-coded performance indicators

## 📦 Dependencies

This project requires the following Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| **Pillow** | ≥10.0.0 | Image processing and manipulation |
| **numpy** | ≥1.24.0 | Numerical computations and arrays |
| **matplotlib** | ≥3.7.0 | Data visualization and plotting |
| **reportlab** | ≥4.0.0 | PDF document generation |

**Note:** `tkinter` is part of the Python standard library and does not require separate installation.

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

Under the conditions:
- 📋 License and copyright notice must be included
- ❌ No warranty provided

## 📖 Citation

If you use ESAI in your research, please cite:

```
Tian, J., Zheng, H., Ai, Y., Xin, T., You, J., Xue, H., Yin, L., & Shi, M. (2026).
Environmental Suitability Assessment Index (ESAI) and Software: A New Metric for 
Assessing the Greenness of Analytical Methods. [Journal Name], [Volume], [Pages].
```

## 👥 Contributors

- **Jiye Tian** - Cancer Hospital, Dalian University of Technology
- **Hongwei Zheng** - Cancer Hospital, Dalian University of Technology
- **Yongshan Ai** - Cancer Hospital, Dalian University of Technology
- **Tong Xin** - Cancer Hospital, Dalian University of Technology
- **Jiansong You** - Aim Honesty Biopharmaceutical Co. LTD
- **Hongyu Xue** - School of Chemical Engineering, DUT
- **Lei Yin** - School of Chemical Engineering, DUT
- **Meiyun Shi** - School of Chemical Engineering, DUT

## 🆘 Support

### Getting Help

- **Tooltips**: Hover over any GUI element for context help
- **Help Buttons**: Click "?" icons for detailed information
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/xzggg2917/ESAI-master/issues)
- **Email**: Contact shimy@dlut.edu.cn or leiyin@dlut.edu.cn

### Troubleshooting

**Common Issues:**

1. **"tkinter not found" error**
   - Usually pre-installed with Python
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On macOS: Reinstall Python from python.org

2. **Font rendering issues**
   - Run `python test_font_compatibility.py` to check available fonts
   - The application includes fallback font support

3. **Import errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **PDF export fails**
   - Check write permissions in the output directory
   - Verify reportlab is installed: `pip show reportlab`

### Feature Requests

We welcome suggestions for improvements! Please open an issue on GitHub with:
- Clear description of the proposed feature
- Use case explanation
- Expected behavior

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Repository:** https://github.com/xzggg2917/ESAI-master