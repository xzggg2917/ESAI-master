# ESAI - 环境适宜性评估指数

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

一个基于绿色分析化学(GAC)原则评估分析方法环境适宜性和绿色程度的综合软件工具。

> **注意**: 完整的英文文档请参见 [README.md](README.md)

## 📋 目录

- [概述](#概述)
- [主要特性](#主要特性)
- [安装说明](#安装说明)
  - [前置要求](#前置要求)
  - [安装步骤](#安装步骤)
- [使用方法](#使用方法)
- [依赖列表](#依赖列表)
- [许可证](#许可证)
- [引用](#引用)
- [技术支持](#技术支持)

## 🔬 概述

**ESAI（环境适宜性评估指数）** 是一个用于评估分析方法绿色程度的新指标。本软件整合了：

- **12条绿色分析化学(GAC)原则**
- **10条样品制备原则**
- **八维评估框架**：
  1. 样品采集 (SC)
  2. 样品制备 (SP)
  3. 分析技术 (AT)
  4. 试剂使用
  5. 方法性能
  6. 操作安全
  7. 经济评价
  8. 废物处理

评估结果通过**八角雷达图**可视化展示，颜色渐变和定量分数表示绿色程度。

### 作者单位

<sup>a</sup> 大连理工大学肿瘤医院，沈阳，110042，中国  
<sup>b</sup> 大连理工大学化工与环境生命学部，盘锦，中国  
<sup>c</sup> 大连艾姆诚信生物制药有限公司，大连，中国

**通讯作者：**
- 石美云：shimy@dlut.edu.cn
- 尹雷：leiyin@dlut.edu.cn

## ✨ 主要特性

- **全面评估**: 覆盖8个维度的27项加权标准
- **交互式GUI**: 基于tkinter构建的用户友好图形界面
- **可视化结果**: 带颜色编码的八角雷达图显示绿色程度
- **PDF报告**: 自动生成详细的评估报告
- **自定义权重**: 可调整不同评估维度的重要性
- **工具提示和帮助**: 界面中提供上下文相关的帮助信息
- **跨平台**: 支持Windows、macOS和Linux

## 🚀 安装说明

### 前置要求

- **Python 3.8或更高版本** ([下载Python](https://www.python.org/downloads/))
- **pip** (Python包管理器，Python自带)
- **tkinter** (通常随Python预装)

### 安装步骤

#### 1. 验证Python安装

打开终端或命令提示符，检查Python版本：

```bash
python --version
```

#### 2. 克隆或下载仓库

```bash
git clone https://github.com/xzggg2917/ESAI-master.git
cd ESAI-master
```

或直接下载ZIP文件并解压。

#### 3. 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. 安装依赖

安装所有必需的包：

```bash
pip install -r requirements.txt
```

这将安装：
- **Pillow** (≥10.0.0) - 图像处理
- **numpy** (≥1.24.0) - 数值计算
- **matplotlib** (≥3.7.0) - 数据可视化
- **reportlab** (≥4.0.0) - PDF生成

#### 5. 验证安装

运行测试套件以确保一切设置正确：

```bash
python test_exec_removal.py
python test_font_compatibility.py
python test_locale_compatibility.py
```

所有测试应该都能通过。

## 📖 使用方法

### 快速开始

1. **导航到项目目录：**
   ```bash
   cd ESAI-master
   ```

2. **激活虚拟环境**（如果创建了）：
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. **启动应用程序：**
   ```bash
   python run_esai.py
   ```

4. **按照GUI工作流程操作：**
   - 在"Weight"标签页中设置维度权重
   - 在各个评估标签页(SC, SP, AT等)中回答问题
   - 查看实时更新的雷达图
   - 导出PDF报告

### GUI界面说明

应用程序包含以下标签页：

| 标签页 | 说明 |
|--------|------|
| **Weight** | 配置8个评估维度的重要性权重 |
| **SC** | 样品采集评估 |
| **SP** | 样品制备评估 |
| **AT** | 分析技术评估 |
| **Reagent** | 试剂使用和环境影响 |
| **Method** | 方法性能特征 |
| **Operator** | 操作安全考虑 |
| **Economy** | 经济评价和成本分析 |
| **Waste** | 废物处理和管理 |

**主要功能：**
- **工具提示**: 将鼠标悬停在任何元素上可查看帮助信息
- **"?"按钮**: 提供每个部分的详细帮助
- **实时可视化**: 雷达图随输入数据实时更新
- **导出功能**: 生成全面的PDF报告

## 📦 依赖列表

本项目需要以下Python包：

| 包名称 | 版本要求 | 用途 |
|--------|----------|------|
| **Pillow** | ≥10.0.0 | 图像处理和操作 |
| **numpy** | ≥1.24.0 | 数值计算和数组处理 |
| **matplotlib** | ≥3.7.0 | 数据可视化和图表绘制 |
| **reportlab** | ≥4.0.0 | PDF文档生成 |

**注意：** `tkinter`是Python标准库的一部分，无需单独安装。

更新依赖：
```bash
pip install --upgrade -r requirements.txt
```

## 📄 许可证

本项目采用 **MIT许可证** - 详见 [LICENSE](LICENSE) 文件。

您可以自由地：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用

前提条件：
- 📋 必须包含许可证和版权声明
- ❌ 不提供任何担保

## 📖 引用

如果您在研究中使用ESAI，请引用：

```
Tian, J., Zheng, H., Ai, Y., Xin, T., You, J., Xue, H., Yin, L., & Shi, M. (2026).
Environmental Suitability Assessment Index (ESAI) and Software: A New Metric for 
Assessing the Greenness of Analytical Methods. [期刊名称], [卷号], [页码].
```

## 🆘 技术支持

### 获取帮助

- **工具提示**: 将鼠标悬停在任何GUI元素上可获得上下文帮助
- **帮助按钮**: 点击"?"图标获取详细信息
- **问题报告**: 通过 [GitHub Issues](https://github.com/xzggg2917/ESAI-master/issues) 报告错误或请求功能
- **邮件联系**: shimy@dlut.edu.cn 或 leiyin@dlut.edu.cn

### 常见问题

1. **"找不到tkinter"错误**
   - 通常随Python预装
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - macOS: 从python.org重新安装Python

2. **字体渲染问题**
   - 运行 `python test_font_compatibility.py` 检查可用字体
   - 应用程序包含后备字体支持

3. **导入错误**
   - 确保虚拟环境已激活
   - 重新安装依赖: `pip install -r requirements.txt`

4. **PDF导出失败**
   - 检查输出目录的写入权限
   - 验证reportlab已安装: `pip show reportlab`

---

**版本:** 1.0.0  
**最后更新:** 2026年2月  
**代码仓库:** https://github.com/xzggg2917/ESAI-master

**完整英文文档请参见:** [README.md](README.md)
