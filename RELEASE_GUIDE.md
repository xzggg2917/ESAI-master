# GitHub Release Guide for ESAI

This guide walks you through creating a GitHub Release to distribute ESAI installation packages.

## 📦 What to Upload

You should prepare two distribution options:

### Option 1: Portable Version (Recommended for Quick Start)
- **File**: `dist/ESAI/` folder → Compress as `ESAI-v1.0.0-Portable-Windows.zip`
- **Size**: ~10-15 MB
- **Usage**: Extract and run `ESAI.exe` directly
- **Advantages**: No installation required, works immediately

### Option 2: Windows Installer (Professional Distribution)
- **File**: `installer_output/ESAI-Setup-v1.0.0.exe`
- **Size**: ~10-15 MB
- **Usage**: Double-click to install
- **Advantages**: Start menu integration, desktop shortcut, uninstaller

## 🚀 Step-by-Step Release Process

### Step 1: Prepare Distribution Files

**Create Portable ZIP:**
```powershell
# Compress the portable version
Compress-Archive -Path "dist\ESAI\*" -DestinationPath "ESAI-v1.0.0-Portable-Windows.zip" -Force
```

**Create Installer (Optional):**
```powershell
# Build installer if not already done
.\build_and_package.ps1
```

After this, you should have:
- ✅ `ESAI-v1.0.0-Portable-Windows.zip` (~10-15 MB)
- ✅ `installer_output\ESAI-Setup-v1.0.0.exe` (~10-15 MB) - if created

### Step 2: Commit and Push All Changes

```powershell
# Check current status
git status

# Add all new files
git add .

# Commit with descriptive message
git commit -m "Add build scripts and packaging configuration for v1.0.0"

# Push to GitHub
git push origin main
```

### Step 3: Create GitHub Release

#### Method A: Using GitHub Web Interface (Recommended)

1. **Navigate to GitHub Repository**
   - Go to: https://github.com/xzggg2917/ESAI-master

2. **Access Releases Section**
   - Click on **"Releases"** in the right sidebar
   - Or go to: https://github.com/xzggg2917/ESAI-master/releases

3. **Create New Release**
   - Click **"Draft a new release"** or **"Create a new release"**

4. **Configure Release Details**

   **Tag version:**
   ```
   v1.0.0
   ```
   - Check **"Create new tag: v1.0.0 on publish"**

   **Release title:**
   ```
   ESAI v1.0.0 - Initial Release
   ```

   **Description:** (Use the template below)

   ```markdown
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
   
   **Option 1: Windows Installer (Recommended)**
   - Download: `ESAI-Setup-v1.0.0.exe`
   - Size: ~10-15 MB
   - Features: Desktop shortcut, Start menu integration, Uninstaller
   - Installation: Double-click and follow the wizard
   
   **Option 2: Portable Version**
   - Download: `ESAI-v1.0.0-Portable-Windows.zip`
   - Size: ~10-15 MB
   - Features: No installation required, run directly
   - Usage: Extract ZIP → Run `ESAI.exe`
   
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
   
   ## 📚 Documentation
   
   - **README**: See [README.md](https://github.com/xzggg2917/ESAI-master/blob/main/README.md)
   - **Installation Guide**: Detailed instructions in repository
   - **Troubleshooting**: Check README for common issues
   
   ## 🐛 Known Issues
   
   None reported in this release.
   
   ## 📝 Changelog
   
   ### Added
   - Initial release with full functionality
   - 8 assessment dimensions (SC, SP, AT, Reagent, Method, Operator, Economy, Waste)
   - Interactive GUI with tooltips and help system
   - PDF report generation
   - English-only interface (language-independent)
   - Build scripts for Windows executable creation
   - Professional installer with Inno Setup
   
   ## 👥 Authors
   
   Jiye Tian, Hongwei Zheng, Yongshan Ai, Tong Xin, Jiansong You, Hongyu Xue, Lei Yin, Meiyun Shi
   
   **Correspondence**: shimy@dlut.edu.cn, leiyin@dlut.edu.cn
   
   ## 📄 License
   
   MIT License - See [LICENSE](https://github.com/xzggg2917/ESAI-master/blob/main/LICENSE)
   
   ## 🆘 Support
   
   - **Issues**: https://github.com/xzggg2917/ESAI-master/issues
   - **Email**: shimy@dlut.edu.cn
   ```

5. **Upload Distribution Files**
   - Drag and drop or click **"Attach binaries by dropping them here or selecting them."**
   - Upload:
     - ✅ `ESAI-v1.0.0-Portable-Windows.zip`
     - ✅ `ESAI-Setup-v1.0.0.exe` (if created)

6. **Publish Release**
   - Check **"Set as the latest release"**
   - Click **"Publish release"**

#### Method B: Using GitHub Desktop

1. **Commit Changes**
   - Open GitHub Desktop
   - Review changes
   - Write commit message: "Add build scripts and v1.0.0 release files"
   - Click **"Commit to main"**

2. **Push to GitHub**
   - Click **"Push origin"**

3. **Create Release via Web**
   - Follow "Method A" steps 2-6 above

#### Method C: Using Git Command Line + Web

```powershell
# Tag the release
git tag -a v1.0.0 -m "ESAI v1.0.0 - Initial Release"

# Push tag to GitHub
git push origin v1.0.0
```

Then go to GitHub web interface to complete the release and upload files.

## 📊 After Publishing

Your release will be available at:
```
https://github.com/xzggg2917/ESAI-master/releases/tag/v1.0.0
```

Users can download files directly from:
```
https://github.com/xzggg2917/ESAI-master/releases/latest
```

### Update README with Download Link

Add to your README.md:

```markdown
## 📥 Download

**Latest Release:** [v1.0.0](https://github.com/xzggg2917/ESAI-master/releases/latest)

### Quick Install (Windows)

1. Download [ESAI-Setup-v1.0.0.exe](https://github.com/xzggg2917/ESAI-master/releases/download/v1.0.0/ESAI-Setup-v1.0.0.exe)
2. Run the installer
3. Launch ESAI from Start Menu or Desktop

### Portable Version (Windows)

1. Download [ESAI-v1.0.0-Portable-Windows.zip](https://github.com/xzggg2917/ESAI-master/releases/download/v1.0.0/ESAI-v1.0.0-Portable-Windows.zip)
2. Extract the ZIP file
3. Run `ESAI.exe`
```

## 🔄 Future Releases

For version updates (v1.0.1, v1.1.0, etc.):

1. **Update version number** in:
   - `ESAI.spec` (version info)
   - `version_info.txt` (file version)
   - `installer.iss` (MyAppVersion)

2. **Rebuild packages**:
   ```powershell
   .\build_and_package.ps1
   ```

3. **Create new release** following the steps above with new version number

## 📈 Tracking Downloads

GitHub automatically tracks download statistics:
- View in your repository's **Insights → Traffic**
- Each release shows download counts for each asset

## ⚠️ Important Notes

### File Size Limits
- GitHub allows files up to **2 GB** per file
- Your files (~10-15 MB each) are well within limits

### Virus Scanning
- GitHub automatically scans uploaded files
- Windows Defender may flag unsigned executables as "Unknown Publisher"
- **Solution**: Consider code signing for production releases

### Digital Signing (Optional for Future)
For production distribution, consider signing your executables:
```powershell
# Using SignTool (requires certificate)
signtool sign /f "certificate.pfx" /p "password" /t "http://timestamp.digicert.com" "ESAI.exe"
```

### Checksum Verification (Recommended)
Generate checksums for users to verify downloads:
```powershell
# Generate SHA256 checksums
Get-FileHash "ESAI-v1.0.0-Portable-Windows.zip" -Algorithm SHA256 | Format-List
Get-FileHash "ESAI-Setup-v1.0.0.exe" -Algorithm SHA256 | Format-List
```

Add checksums to release notes for security verification.

## ✅ Checklist

Before publishing:
- [ ] All code changes committed and pushed
- [ ] Version numbers updated consistently
- [ ] Built and tested executable
- [ ] Created portable ZIP file
- [ ] Created installer (optional)
- [ ] Prepared release notes
- [ ] Generated checksums (optional)
- [ ] Reviewed all files for sensitive information

## 🎯 Quick Command Summary

```powershell
# 1. Build everything
.\build_and_package.ps1

# 2. Create portable ZIP
Compress-Archive -Path "dist\ESAI\*" -DestinationPath "ESAI-v1.0.0-Portable-Windows.zip" -Force

# 3. Generate checksums
Get-FileHash "ESAI-v1.0.0-Portable-Windows.zip" -Algorithm SHA256
Get-FileHash "installer_output\ESAI-Setup-v1.0.0.exe" -Algorithm SHA256

# 4. Commit and push
git add .
git commit -m "Release v1.0.0"
git push origin main

# 5. Create release on GitHub web interface and upload files
```

That's it! Your users can now easily download and install ESAI.
