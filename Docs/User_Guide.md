# User Guide

This guide shows you how to use the Astronomy Starter Kit for your daily astronomy work.

---

## Quick Start

After installation, you have one main command: `astro`

```bash
astro              # Show menu and available commands
astro jupyter      # Start Jupyter Lab
astro topcat       # Open TOPCAT
astro ds9          # Open DS9 image viewer
```

That's the basics. Read on for complete details.

---

## Command Reference

### Overview Table

| Command | What It Does |
|---------|--------------|
| `astro` | Show quick menu |
| `astro jupyter` | Launch Jupyter Lab |
| `astro topcat` | Launch TOPCAT catalog viewer |
| `astro ds9` | Launch DS9 image viewer |
| `astro python` | Start Python with astronomy packages |
| `astro status` | Check what's installed |
| `astro doctor` | Find and diagnose problems |
| `astro repair` | Fix common problems |
| `astro update` | Update all packages |
| `astro uninstall` | Remove everything |
| `astro help` | Show help information |
| `astro-activate` | Activate Python environment manually |

---

### Launch Commands

#### astro jupyter

Opens Jupyter Lab in your web browser.

```bash
astro jupyter
```

**What happens:**
1. Activates the astronomy Python environment
2. Opens your default browser
3. Shows Jupyter Lab interface at `http://localhost:8888`

**To stop Jupyter:** Press `Ctrl+C` in the terminal, then type `y` to confirm.

---

#### astro topcat

Opens TOPCAT for catalog and table analysis.

```bash
# Open TOPCAT with no file
astro topcat

# Open TOPCAT with a specific file
astro topcat my_catalog.fits
astro topcat data.csv
astro topcat table.vot
```

**Supported file formats:** FITS, CSV, TSV, VOTable, ASCII tables

**Note:** On Wayland systems (Ubuntu 22.04+), the launcher automatically configures display settings. If you see display errors, see the [Troubleshooting Guide](TROUBLESHOOTING.md).

---

#### astro ds9

Opens DS9 for viewing FITS images.

```bash
# Open DS9 with no file
astro ds9

# Open DS9 with an image
astro ds9 my_image.fits
```

**Tip:** You can drag and drop FITS files into the DS9 window after it opens.

---

#### astro python

Starts an interactive Python session with all astronomy packages loaded.

```bash
astro python
```

**What's available immediately:**

```python
>>> import numpy as np
>>> import scipy
>>> import matplotlib.pyplot as plt
>>> import pandas as pd
>>> from astropy.io import fits
>>> from astropy.table import Table
>>> from astropy import units as u
>>> from astropy.coordinates import SkyCoord
```

**To exit Python:** Type `exit()` or press `Ctrl+D`

---

### Management Commands

#### astro status

Shows what's installed and working.

```bash
astro status
```

**Example output:**

```
╔══════════════════════════════════════════════════════════════╗
║          ASTRONOMY ENVIRONMENT - Status                       ║
╚══════════════════════════════════════════════════════════════╝

✓ Python Environment    installed    ~/.astro/env/
✓ TOPCAT               installed    ~/.astro/bin/topcat
✓ DS9                  installed    /usr/bin/ds9
✓ Jupyter Lab          installed    
✓ Shell Configuration  configured   ~/.zshrc

All systems operational
```

**Status symbols:**
- ✓ = Working correctly
- ✗ = Not installed or broken
- ⚠ = Installed but has issues

---

#### astro doctor

Runs diagnostic tests to find problems.

```bash
astro doctor
```

**What it checks:**
- Python environment integrity
- Package installation status
- Java installation (for TOPCAT)
- Display configuration
- File permissions
- Shell configuration

**Example output:**

```
Running diagnostics...

✓ Python environment exists
✓ Core packages installed
✓ Java found (version 21)
✓ TOPCAT jar file present
✓ Display configuration correct
✓ Shell integration working

All checks passed
```

---

#### astro repair

Automatically fixes common problems.

```bash
astro repair
```

**What it fixes:**
- Reinstalls missing Python packages
- Reconfigures display settings
- Resets shell configuration
- Re-downloads corrupted files

**When to use:** Run this if `astro doctor` shows errors.

---

#### astro update

Updates all packages to latest versions.

```bash
astro update
```

**What gets updated:**
- pip (Python package manager)
- numpy, scipy, matplotlib, pandas
- astropy
- jupyter, jupyterlab
- plotly, seaborn

**How long:** Usually 2-5 minutes depending on internet speed.

---

#### astro uninstall

Removes the entire astronomy environment.

```bash
astro uninstall
```

**Warning:** This deletes everything in `~/.astro/` including any notebooks or data you saved there.

**What happens:**
1. Asks for confirmation (you must type `yes`)
2. Removes `~/.astro/` directory
3. Removes shell configuration entries
4. Tells you to reload your shell

**To reinstall later:** Run the original installation command again.

---

#### astro help

Shows help and available commands.

```bash
astro help
```

---

#### astro-activate

Manually activates the Python environment without launching any tool.

```bash
astro-activate
```

**When to use:** When you want to run Python scripts directly or use pip.

**Your prompt changes to show activation:**

```
(astro) user@computer:~$
```

**To deactivate:** Type `deactivate` or close the terminal.

---

## Directory Structure

Everything lives in `~/.astro/` (a hidden folder in your home directory).

```
~/.astro/
│
├── bin/                    # Command launchers
│   ├── topcat              # TOPCAT launcher script
│   ├── astro-jupyter       # Jupyter launcher
│   └── astro-python        # Python launcher
│
├── env/                    # Python virtual environment
│   ├── bin/                # Python executables
│   ├── lib/                # Installed packages
│   └── share/              # Jupyter data
│
├── cache/                  # Downloaded files
│   └── topcat-full.jar     # TOPCAT application
│
├── notebooks/              # Your Jupyter notebooks
│   └── (your work here)
│
├── scripts/                # Helper scripts
│   ├── visual_foundations.py
│   └── foundation_dashboard.py
│
├── config/                 # Configuration files
│   └── state.json          # Installation state
│
└── logs/                   # Log files (if any)
```

**Important locations:**
- Save your notebooks in `~/.astro/notebooks/`
- Your Python environment is in `~/.astro/env/`
- TOPCAT is stored in `~/.astro/cache/`

---

## Using Jupyter Lab

Jupyter Lab is where you write and run Python code interactively.

### Starting Jupyter

```bash
astro jupyter
```

Your browser opens automatically. If it doesn't, look in the terminal for a URL like:

```
http://localhost:8888/lab?token=abc123...
```

Copy and paste this URL into your browser.

### Creating a New Notebook

1. Click the **Python 3** or **Astronomy Python** icon under "Notebook"
2. A new notebook opens with an empty cell
3. Type code in the cell
4. Press `Shift+Enter` to run the cell

### Example: Load and Plot Data

```python
# Cell 1: Import libraries
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Cell 2: Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Cell 3: Make a plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.xlabel('X axis', fontsize=14)
plt.ylabel('Y axis', fontsize=14)
plt.title('Sine Wave', fontsize=16)
plt.grid(True)
plt.show()
```

### Saving Your Work

- Press `Ctrl+S` to save
- Notebooks are saved as `.ipynb` files
- Default location: `~/.astro/notebooks/`

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run cell | `Shift+Enter` |
| Run cell, stay in cell | `Ctrl+Enter` |
| Add cell below | `B` (in command mode) |
| Add cell above | `A` (in command mode) |
| Delete cell | `D D` (press D twice) |
| Save notebook | `Ctrl+S` |
| Enter command mode | `Esc` |
| Enter edit mode | `Enter` |

### Stopping Jupyter

In the terminal where Jupyter is running:
1. Press `Ctrl+C`
2. Type `y` when asked to confirm
3. Jupyter shuts down

---

## Using TOPCAT

TOPCAT is for analyzing astronomical catalogs and tables.

### Starting TOPCAT

```bash
# Open empty
astro topcat

# Open with a file
astro topcat catalog.fits
```

### Loading Data

**Method 1: Command line**
```bash
astro topcat your_file.fits
```

**Method 2: Inside TOPCAT**
1. Click **File** → **Load Table**
2. Browse to your file
3. Click **OK**

### Supported Formats

| Format | Extensions |
|--------|------------|
| FITS | `.fits`, `.fit` |
| CSV | `.csv` |
| Tab-separated | `.tsv` |
| VOTable | `.vot`, `.xml` |
| ASCII | `.txt`, `.dat` |

### Common Tasks

**View table contents:**
1. Load a table
2. Click the table name in the left panel
3. Click **Views** → **Table Browser**

**Make a scatter plot:**
1. Load your data
2. Click **Graphics** → **Plane Plot**
3. Select X and Y columns
4. Click **Plot**

**Cross-match two catalogs:**
1. Load both tables
2. Click **Joins** → **Pair Match**
3. Select matching columns (usually RA, Dec)
4. Set match radius
5. Click **Go**

### Saving Results

1. Select the table you want to save
2. Click **File** → **Save Table**
3. Choose format and location
4. Click **Save**

---

## Using DS9

DS9 is for viewing FITS images.

### Starting DS9

```bash
# Open empty
astro ds9

# Open with an image
astro ds9 image.fits
```

### Basic Navigation

| Action | How |
|--------|-----|
| Zoom in | Scroll wheel up |
| Zoom out | Scroll wheel down |
| Pan | Click and drag |
| Reset view | Click **Zoom** → **Fit** |

### Adjusting Display

**Change color scale:**
1. Click **Scale** menu
2. Choose: Linear, Log, Sqrt, etc.

**Change color map:**
1. Click **Color** menu
2. Choose: Grey, Heat, Cool, Rainbow, etc.

### Measuring

**Read coordinates:**
- Move mouse over image
- Coordinates show in bottom bar

**Measure distance:**
1. Click **Edit** → **Region**
2. Draw a line between two points
3. Region info shows distance

### Saving Images

**Save as PNG/JPEG:**
1. Click **File** → **Save Image**
2. Choose format
3. Enter filename
4. Click **Save**

---

## Daily Workflow Examples

### Example 1: Quick Data Analysis

```bash
# Start Jupyter
astro jupyter

# In notebook:
from astropy.table import Table
data = Table.read('my_catalog.fits')
print(data.info())
```

### Example 2: Inspect a Catalog

```bash
# Open directly in TOPCAT
astro topcat survey_results.csv
```

### Example 3: View a FITS Image

```bash
# Open in DS9
astro ds9 galaxy_image.fits
```

### Example 4: Python Scripting

```bash
# Activate environment
astro-activate

# Run your script
python analyze_lightcurve.py

# When done
deactivate
```

### Example 5: Morning Setup

```bash
# Check everything is working
astro status

# Start your work
astro jupyter
```

---

## Tips for Success

### Organize Your Files

Create folders for different projects:

```bash
mkdir -p ~/.astro/notebooks/project1
mkdir -p ~/.astro/notebooks/project2
```

### Keep Notebooks Clean

- One notebook per analysis
- Use markdown cells for notes
- Clear output before saving to reduce file size

### Regular Updates

Update packages monthly:

```bash
astro update
```

### Backup Your Work

Your notebooks are in `~/.astro/notebooks/`. Back up this folder regularly:

```bash
cp -r ~/.astro/notebooks/ ~/Backups/astronomy-notebooks-$(date +%Y%m%d)/
```

### If Something Breaks

1. First try: `astro doctor`
2. If issues found: `astro repair`
3. Still broken: Check [Troubleshooting Guide](TROUBLESHOOTING.md)
4. Need help: [Open an issue](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues)

---

## Learning Resources

### Python for Astronomy

- [Astropy Tutorials](https://learn.astropy.org) — Official astropy learning materials
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) — Free online book

### TOPCAT

- [TOPCAT Documentation](https://www.star.bris.ac.uk/~mbt/topcat/) — Official manual
- Search "TOPCAT tutorial" on YouTube for video guides

### DS9

- [DS9 Documentation](https://sites.google.com/cfa.harvard.edu/saoimageds9) — Official manual
- [DS9 Quick Reference](https://sites.google.com/cfa.harvard.edu/saoimageds9/documentation)

### FITS Format

- [FITS Standard](https://fits.gsfc.nasa.gov) — NASA FITS documentation

---

## Getting Help

- Run `astro help` for command reference
- Check [FAQ](FAQ.md) for common questions
- See [Troubleshooting](TROUBLESHOOTING.md) for problem solutions
- [Open an issue](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) on GitHub

---

Happy observing! 🔭