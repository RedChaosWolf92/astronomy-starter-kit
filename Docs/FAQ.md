# Frequently Asked Questions

Quick answers to common questions about the Astronomy Starter Kit.

---

## Table of Contents

1. [Installation Questions](#1-installation-questions)
2. [Usage Questions](#2-usage-questions)
3. [Tool-Specific Questions](#3-tool-specific-questions)
4. [Troubleshooting Questions](#4-troubleshooting-questions)
5. [Project Questions](#5-project-questions)

---

## 1. Installation Questions

### How long does installation take?

**First-time installation: 10-15 minutes**

The time breaks down roughly as:
- Downloading the launcher: ~30 seconds
- Python environment setup: 3-5 minutes
- Installing Python packages: 5-8 minutes
- Downloading TOPCAT: 1-2 minutes

After installation, all commands run instantly.

---

### Can I install without sudo?

**Partially.** The initial launcher downloads without sudo, but the full installation needs sudo for:

- Installing system packages (Java, DS9, XWayland)
- Installing Python development headers

If you're on a system without sudo access, you can still use the Python environment, but TOPCAT and DS9 won't install automatically. Contact your system administrator to install these packages:

```bash
# Packages that need sudo
openjdk-21-jdk openjdk-21-jre saods9 xwayland python3-venv python3-dev
```

---

### Will this affect my existing Python?

**No.** Everything installs into an isolated virtual environment at `~/.astro/env/`. Your system Python remains completely untouched.

You can verify this after installation:

```bash
# System Python (unchanged)
/usr/bin/python3 --version

# Astronomy environment Python (isolated)
~/.astro/env/bin/python --version
```

The two never interfere with each other. You can safely delete `~/.astro/` at any time without affecting your system.

---

### Does it work on Raspberry Pi?

**Experimental.** The toolkit should work on Raspberry Pi 4 or 5 running Ubuntu 22.04+ (64-bit ARM), but it's not officially tested.

Known considerations:
- Installation takes longer on Pi hardware (~25-30 minutes)
- Some visualization features may be slower
- TOPCAT works but may feel sluggish
- We recommend at least 4GB RAM

If you try it on a Pi, please [report your experience](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) so we can improve support.

---

### Can I install on WSL (Windows Subsystem for Linux)?

**Yes, with limitations.** WSL2 with Ubuntu works for the Python environment and Jupyter notebooks.

GUI applications (TOPCAT, DS9) require additional setup:

1. Install WSLg (included in Windows 11) or an X server like VcXsrv
2. The display configuration may need manual adjustment

```bash
# In WSL, you may need to set:
export DISPLAY=:0
```

For the best experience with GUI tools, we recommend a native Ubuntu installation or VM.

---

### Does it work on other Linux distributions?

**Officially supported:** Ubuntu 22.04 and 24.04 LTS

**Should work:** Debian 11+, Linux Mint 21+, Pop!_OS 22.04+

**Untested:** Fedora, Arch, openSUSE (contributions welcome!)

For non-Ubuntu distributions, you may need to adjust package names. The installer will warn you if it detects an unsupported distribution.

---

## 2. Usage Questions

### How do I update the tools?

```bash
astro update
```

This updates all Python packages to their latest versions. It takes 2-5 minutes.

To update the `astro` launcher itself, reinstall it:

```bash
curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh | bash
```

---

### Where are my notebooks saved?

**Default location:** `~/.astro/notebooks/`

When you create notebooks in Jupyter Lab, they save to this directory. You can organize them into subfolders:

```bash
~/.astro/notebooks/
├── my_analysis.ipynb
├── project1/
│   └── data_exploration.ipynb
└── project2/
    └── results.ipynb
```

**Tip:** Back up this folder regularly:

```bash
cp -r ~/.astro/notebooks/ ~/Backups/astronomy-notebooks-$(date +%Y%m%d)/
```

---

### Can I add my own Python packages?

**Yes!** Activate the environment and use pip:

```bash
# Activate the environment
astro-activate

# Install any package you need
pip install photutils
pip install specutils
pip install lightkurve

# Verify it's installed
pip list | grep photutils
```

Your custom packages persist across sessions. They're stored in `~/.astro/env/`.

---

### How do I use my own data files?

You have several options:

**Option 1: Open directly from any location**

```bash
astro topcat /path/to/your/catalog.fits
astro ds9 ~/Downloads/image.fits
```

**Option 2: Copy to the data directory**

```bash
cp your_data.fits ~/.astro/data/
```

Then access it in Python:

```python
from astropy.io import fits
data = fits.open('~/.astro/data/your_data.fits')
```

**Option 3: Use symbolic links**

```bash
ln -s /path/to/your/data/folder ~/.astro/data/my_project
```

---

### Can I have multiple environments?

**Not with the standard setup**, but you can create additional environments manually:

```bash
# Create a second environment
python3 -m venv ~/.astro/env-project2

# Activate it manually
source ~/.astro/env-project2/bin/activate

# Install packages for this specific project
pip install your-special-packages
```

The `astro` commands will always use the main `~/.astro/env/` environment. For project-specific environments, activate them manually.

---

### Can I change where things are installed?

**Yes.** Set the `ASTRO_HOME` environment variable before installation:

```bash
export ASTRO_HOME="$HOME/my-custom-location"
curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh | bash
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

---

## 3. Tool-Specific Questions

### Why won't TOPCAT open?

This is almost always a display configuration issue on Wayland systems (Ubuntu 22.04+ default).

**Quick fix:**

```bash
# Use the astro launcher instead of calling topcat directly
astro topcat
```

The `astro topcat` command sets the necessary display variables automatically.

**If that doesn't work:**

```bash
# Run the repair command
astro repair

# Then try again
astro topcat
```

**Still not working?** See the detailed [TOPCAT Troubleshooting Guide](TROUBLESHOOTING.md#2-topcat-issues).

---

### How do I open FITS files?

**For images (viewing):**

```bash
astro ds9 your_image.fits
```

**For tables/catalogs (analysis):**

```bash
astro topcat your_catalog.fits
```

**In Python:**

```python
from astropy.io import fits
from astropy.table import Table

# For image data
with fits.open('image.fits') as hdul:
    data = hdul[0].data
    header = hdul[0].header

# For table data
table = Table.read('catalog.fits')
print(table)
```

**In Jupyter:**

```python
# Astropy is pre-installed
from astropy.io import fits
import matplotlib.pyplot as plt

data = fits.getdata('your_image.fits')
plt.imshow(data, cmap='gray')
plt.colorbar()
plt.show()
```

---

### Can I use VS Code instead of Jupyter?

**Yes!** The Python environment works with any editor.

**Setup for VS Code:**

1. Install the Python extension in VS Code
2. Open VS Code
3. Press `Ctrl+Shift+P` → "Python: Select Interpreter"
4. Choose: `~/.astro/env/bin/python`

Now VS Code uses the astronomy environment with all packages available.

**For notebooks in VS Code:**

1. Install the Jupyter extension
2. Open a `.ipynb` file
3. Select the `~/.astro/env/bin/python` kernel

---

### Can I use the Python environment in a terminal without launching tools?

**Yes.** Use the activation command:

```bash
astro-activate
```

Your prompt changes to show the environment is active:

```
(astro) user@computer:~$
```

Now you can run Python scripts, use pip, or start an interactive Python session:

```bash
python your_script.py
python -c "import astropy; print(astropy.__version__)"
```

Type `deactivate` when finished.

---

### How do I use TOPCAT with large catalogs?

TOPCAT can handle millions of rows, but may need more memory:

```bash
# Launch with 4GB of memory
java -Xmx4g -jar ~/.astro/cache/topcat-full.jar your_huge_catalog.fits
```

For extremely large files (100M+ rows), consider:
- Using TOPCAT's "Load Rows" feature to load a subset
- Pre-filtering with Python before loading
- Using STILTS (command-line TOPCAT) for batch processing

---

## 4. Troubleshooting Questions

### What does "astro doctor" do?

The `doctor` command runs diagnostic checks on your installation:

```bash
astro doctor
```

**It checks:**
- Python environment exists and works
- All required packages are installed
- Java is available (for TOPCAT)
- TOPCAT jar file is present
- DS9 is installed
- Display configuration is correct
- Shell integration is set up

**Output shows:**
- ✓ = Working correctly
- ✗ = Broken or missing
- ⚠ = Partial issues

After running doctor, you'll know exactly what needs fixing.

---

### How do I completely reset everything?

**Option 1: Use the uninstall command**

```bash
astro uninstall
```

This removes `~/.astro/` and the shell configuration entries. Then reinstall fresh.

**Option 2: Manual removal**

```bash
# Remove the installation directory
rm -rf ~/.astro

# Remove the launcher
rm ~/.local/bin/astro

# Edit your shell config to remove the astronomy section
nano ~/.zshrc  # or ~/.bashrc
# Delete lines between "# ==== ASTRO ENVIRONMENT ====" and "# ==== END ASTRO ===="

# Reload shell
source ~/.zshrc
```

**Then reinstall:**

```bash
curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh | bash
```

---

### Why is my terminal slow after installation?

The installation adds a few lines to your shell configuration. These should not cause slowdown, but if you notice issues:

**Check 1: Complex XAUTHORITY lookup**

The display configuration includes a file search. If this is slow, simplify it:

```bash
# Edit your shell config
nano ~/.zshrc

# Find this line:
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)

# Replace with a static path if you know it, or remove if not using Wayland GUI apps
```

**Check 2: Environment activation**

The installation does NOT auto-activate the Python environment on every terminal. If you added that yourself, it will slow things down. Remove any `source ~/.astro/env/bin/activate` from your shell config.

**Check 3: Other shell plugins**

The astronomy toolkit is unlikely to be the cause. Check for:
- Oh-my-zsh plugins that scan files
- NVM (Node Version Manager) slow initialization
- Other environment managers

---

### Why do I get "command not found" errors?

Your PATH wasn't updated. Fix it:

```bash
# Reload your shell configuration
source ~/.zshrc  # or ~/.bashrc

# Or just open a new terminal window
```

If still not working:

```bash
# Check if the file exists
ls -la ~/.local/bin/astro

# Add to PATH manually (temporary)
export PATH="$HOME/.local/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### Jupyter shows "Kernel not found" - how do I fix it?

Reinstall the Jupyter kernel:

```bash
astro-activate
python -m ipykernel install --user --name=astro --display-name="Astronomy Python"
deactivate
```

Then restart Jupyter:

```bash
astro jupyter
```

Select "Astronomy Python" as your kernel.

---

## 5. Project Questions

### Is this free to use?

**Yes, completely free.** The Astronomy Starter Kit is released under the MIT License. You can:

- Use it for any purpose (personal, academic, commercial)
- Modify it to suit your needs
- Share it with others
- Include it in your own projects

No attribution required, though it's appreciated.

---

### Can I use this for teaching?

**Absolutely!** The toolkit was designed with education in mind. 

**For instructors:**

- Students can install independently with one command
- Consistent environment across all students
- No "it works on my machine" problems
- Includes example notebooks to get started

**Suggested workflow:**

1. Have students run the installation command
2. Distribute your course notebooks
3. Students open with `astro jupyter`

**Tips for classroom use:**

- Test on the same Ubuntu version your students will use
- Run `astro doctor` to verify installations
- Keep the [Troubleshooting Guide](TROUBLESHOOTING.md) handy

Feel free to adapt the toolkit for your course. If you make improvements, consider contributing them back!

---

### How do I contribute?

We welcome contributions! Here's how:

**Report bugs or suggest features:**
- [Open an issue](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues)

**Improve documentation:**
- Fork the repository
- Edit the docs
- Submit a pull request

**Fix bugs or add features:**
- See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed instructions
- Fork → Clone → Branch → Code → Test → Pull Request

**Other ways to help:**
- Star the repository
- Share with colleagues
- Test on different systems and report results
- Answer questions in issues

---

### Who maintains this project?

The Astronomy Starter Kit is maintained by [RedChaosWolf92](https://github.com/RedChaosWolf92) and community contributors.

**Contact:**
- GitHub Issues (preferred for technical questions)
- Pull requests for contributions

**Response time:**
- Issues are typically reviewed within a few days
- Pull requests may take 1-2 weeks for review

---

### Can I use this in a research paper?

**Yes.** If the toolkit helped with your research, you're welcome to acknowledge it, but it's not required.

If you do want to cite it:

```
Astronomy Starter Kit. https://github.com/RedChaosWolf92/astronomy-starter-kit
```

---

### What's the roadmap for future development?

Planned features (no specific timeline):

- [ ] Support for more Linux distributions
- [ ] Additional astronomy tools (Aladin, Stellarium integration)
- [ ] Cloud/container deployment options
- [ ] More example notebooks
- [ ] ARM64 (Raspberry Pi, Apple Silicon) official support

Want to help with any of these? Check the [issues page](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) or open a new one to discuss.

---

## Still Have Questions?

- Check the [Troubleshooting Guide](TROUBLESHOOTING.md) for technical issues
- Read the [User Guide](USER_GUIDE.md) for detailed usage instructions
- [Open an issue](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) for anything not covered here

Happy observing! 🔭