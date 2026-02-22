# ESAI v1.0.0 - Environmental Suitability Assessment Index

## 🎉 Initial Release

This is the first stable release of ESAI (Environmental Suitability Assessment Index) - A comprehensive tool for evaluating the environmental suitability and greenness of analytical methods based on Green Analytical Chemistry (GAC) principles.

## ✨ Features

- **Comprehensive Assessment**: 27 weighted criteria across 8 dimensions
- **Interactive GUI**: User-friendly graphical interface
- **Visual Results**: Octagonal radar charts with color-coded indicators
- **PDF Reports**: Automated generation of detailed assessment reports
- **English Interface**: Fully English interface, language-independent
- **Cross-Platform**: Support for Windows, macOS, and Linux

## 📥 Download Options

### For Windows Users:

**Portable Version (Recommended for Quick Start)**
- Download: `ESAI-v1.0.0-Portable-Windows.zip`
- Size: ~44 MB
- Features: No installation required, run directly
- Usage: 
  1. Download and extract ZIP file
  2. Run `ESAI.exe`
  3. Start using immediately

### For macOS/Linux Users:

Install from source:
```bash
git clone https://github.com/xzggg2917/ESAI-master.git
cd ESAI-master
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_esai.py
```

## 📋 System Requirements

- **Windows**: Windows 7 SP1 or later (64-bit)
- **macOS**: macOS 10.13 or later
- **Linux**: Most modern distributions
- **Python** (source installation): Python 3.8+

## 🔐 File Verification

Verify your download using SHA256 checksums:

```
ESAI-v1.0.0-Portable-Windows.zip
SHA256: D8C9A06A0A842EABCD1E6185618E21304D8D32D8CCC3CA893E33B5C64BA2C714
```

**How to verify on Windows:**
```powershell
Get-FileHash "ESAI-v1.0.0-Portable-Windows.zip" -Algorithm SHA256
```

## 📚 Documentation

- **README**: See [README.md](https://github.com/xzggg2917/ESAI-master/blob/main/README.md)
- **Installation Guide**: Detailed instructions in repository
- **Build Guide**: See [RELEASE_GUIDE.md](https://github.com/xzggg2917/ESAI-master/blob/main/RELEASE_GUIDE.md)
- **Troubleshooting**: Check README for common issues

## 🐛 Known Issues

None reported in this release.

If you encounter any issues, please report them at: https://github.com/xzggg2917/ESAI-master/issues

## 📝 Changelog

### Added
- Initial release with full functionality
- 8 assessment dimensions (SC, SP, AT, Reagent, Method, Operator, Economy, Waste)
- 27 evaluation principles with weighted scoring
- Interactive GUI with tooltips and context-sensitive help
- Real-time radar chart visualization
- PDF report generation with detailed scores
- English-only interface (language-independent)
- Build scripts for Windows executable creation
- Comprehensive documentation and user guide

### Technical Highlights
- Object-oriented architecture with proper encapsulation
- No global variables - modern Python design patterns
- Type hints throughout codebase
- Modular package structure for maintainability
- Cross-platform compatibility

## 👥 Authors

Jiye Tian<sup>a#</sup>, Hongwei Zheng<sup>a#</sup>, Yongshan Ai<sup>a#</sup>, Tong Xin<sup>a#</sup>, Jiansong You<sup>c</sup>, Hongyu Xue<sup>b*</sup>, Lei Yin<sup>b**</sup>, Meiyun Shi<sup>a,b,c*</sup>

<sup>a</sup> Cancer Hospital of Dalian University of Technology, Dalian University of Technology, Shenyang, 110042, China  
<sup>b</sup> School of Chemical Engineering, Ocean and Life Sciences, Dalian University of Technology, Panjin, P.R. China  
<sup>c</sup> Aim Honesty Biopharmaceutical Co. LTD, Dalian, P.R. China

**Correspondence**: shimy@dlut.edu.cn, leiyin@dlut.edu.cn

## 📄 License

MIT License - See [LICENSE](https://github.com/xzggg2917/ESAI-master/blob/main/LICENSE)

Copyright (c) 2026 Hongwei Zheng and contributors

## 🆘 Support

- **Bug Reports**: https://github.com/xzggg2917/ESAI-master/issues
- **Email Support**: shimy@dlut.edu.cn
- **Documentation**: https://github.com/xzggg2917/ESAI-master

## 🙏 Acknowledgments

This software was developed at Dalian University of Technology to support research in Green Analytical Chemistry and environmental assessment methodologies.

---

**Full Changelog**: https://github.com/xzggg2917/ESAI-master/commits/v1.0.0
