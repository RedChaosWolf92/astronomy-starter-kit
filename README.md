# 🔭 Astronomy Starter Kit

> A complete, zero-configuration astronomy development environment for Linux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20|%2024.04-orange)](https://ubuntu.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## ✨ Features

- 🐍 **Python Environment** - Scientific computing with numpy, scipy, matplotlib, pandas
- 📊 **TOPCAT** - Powerful catalog and table analysis tool
- 🖼️ **DS9** - FITS image viewer
- 📓 **Jupyter Lab** - Interactive notebooks for astronomy
- 🎨 **Visual Tools** - Enhanced visualization with large fonts and high contrast
- 🚀 **One-Command Setup** - Everything installs automatically
- 🔧 **Self-Healing** - Built-in diagnostics and repair tools

## 🚀 Quick Start

### Installation (30 seconds)
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/astronomy-starter-kit/main/install.sh | bash
```

That's it! The installer will:
1. Download the `astro` launcher
2. Set up your environment
3. Install all astronomy tools (takes ~10 minutes on first run)

### Usage
```bash
astro              # First run: auto-installs everything
astro jupyter      # Launch Jupyter Lab
astro topcat       # Launch TOPCAT
astro status       # Check installation
astro doctor       # Diagnose issues
```

## 📋 What's Included

| Tool | Purpose | Documentation |
|------|---------|---------------|
| **Python Environment** | Scientific computing and data analysis | [User Guide](docs/USER_GUIDE.md) |
| **Astropy** | Core astronomy library | [astropy.org](https://www.astropy.org/) |
| **TOPCAT** | Catalog analysis and visualization | [TOPCAT Guide](https://www.star.bris.ac.uk/~mbt/topcat/) |
| **DS9** | FITS image viewer | [DS9 Manual](https://sites.google.com/cfa.harvard.edu/saoimageds9) |
| **Jupyter Lab** | Interactive development environment | [jupyter.org](https://jupyter.org/) |
| **Plotly/Seaborn** | Advanced data visualization | Included |

## 💻 System Requirements

- **OS**: Ubuntu 22.04+ or Debian-based Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 3GB free space
- **Display**: Works with both X11 and Wayland

## 📚 Documentation

- 📖 [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- 🎓 [User Guide](docs/USER_GUIDE.md) - How to use the environment
- 🔧 [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- ❓ [FAQ](docs/FAQ.md) - Frequently asked questions
- 🛠️ [Development](docs/DEVELOPMENT.md) - Contributing to the project

## 🎯 Quick Examples

### Launch Jupyter and Create Your First Notebook
```bash
astro jupyter
```

### Analyze a Catalog with TOPCAT
```bash
astro topcat your_catalog.fits
```

### Activate Python Environment
```bash
astro-activate
python
>>> import numpy as np
>>> import astropy
>>> # Start analyzing!
```

## 🐛 Troubleshooting

### TOPCAT won't launch on Wayland?

See our comprehensive [TOPCAT Troubleshooting Guide](docs/TROUBLESHOOTING.md) specifically for Ubuntu Wayland issues.

### Environment not working?
```bash
astro doctor    # Diagnoses issues
astro repair    # Fixes common problems
```

### Need help?

- [Open an issue](https://github.com/YOUR_USERNAME/astronomy-starter-kit/issues)
- Check [FAQ](docs/FAQ.md)
- Read [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star this repository

## 🎓 For Educators

This toolkit is perfect for:
- Astronomy courses
- Research groups
- Student projects
- Workshops and tutorials

See [Using in Education](docs/EDUCATION.md) for tips on classroom use.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TOPCAT](https://www.star.bris.ac.uk/~mbt/topcat/) by Mark Taylor
- [Astropy Project](https://www.astropy.org/)
- [SAOImage DS9](https://sites.google.com/cfa.harvard.edu/saoimageds9)
- All contributors to this project

## 📊 Project Status

- ✅ Core functionality complete
- ✅ Ubuntu 22.04 & 24.04 tested
- ✅ Wayland support verified
- 🚧 Additional tools being added

## 🔗 Links

- [Project Website](https://YOUR_USERNAME.github.io/astronomy-starter-kit)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/YOUR_USERNAME/astronomy-starter-kit/issues)
- [Releases](https://github.com/YOUR_USERNAME/astronomy-starter-kit/releases)

---

**Made with ❤️ for the astronomy community**

If this project helped you, please ⭐ star the repository!
