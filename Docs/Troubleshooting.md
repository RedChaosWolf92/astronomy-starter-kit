# Troubleshooting Guide

This guide helps you solve common problems with the Astronomy Starter Kit. Each section shows the error you might see and provides copy-paste solutions.

---

## Quick Fixes

Before diving into specific issues, try these commands:

```bash
# Check what's working and what's not
astro doctor

# Automatically fix common problems
astro repair

# Reload your shell configuration
source ~/.zshrc    # for zsh
source ~/.bashrc   # for bash
```

---

## Table of Contents

1. [Installation Problems](#1-installation-problems)
2. [TOPCAT Issues](#2-topcat-issues)
3. [Jupyter Problems](#3-jupyter-problems)
4. [DS9 Issues](#4-ds9-issues)
5. [Python Environment Issues](#5-python-environment-issues)
6. [General Issues](#6-general-issues)
7. [Using astro doctor and astro repair](#7-using-astro-doctor-and-astro-repair)

---

## 1. Installation Problems

### curl or wget not found

**Error message:**
```
bash: curl: command not found
```
or
```
bash: wget: command not found
```

**Solution:**
```bash
sudo apt update
sudo apt install curl wget
```

Then run the installation command again.

---

### Permission denied during installation

**Error message:**
```
Permission denied
```
or
```
cannot create directory '/home/user/.astro': Permission denied
```

**Solution:**

Check ownership of your home directory:
```bash
ls -la ~ | head -5
```

Fix permissions if needed:
```bash
sudo chown -R $USER:$USER ~/.astro
chmod -R 755 ~/.astro
```

If installing to `/usr/local/bin`:
```bash
sudo chown $USER:$USER /usr/local/bin/astro
```

---

### Python version issues

**Error message:**
```
Python 3.x is required, but Python 2.x was found
```
or
```
python3: command not found
```

**Solution:**

Install Python 3:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-dev python3-pip
```

Check your version:
```bash
python3 --version
```

You need Python 3.10 or newer. Ubuntu 22.04 has Python 3.10, Ubuntu 24.04 has Python 3.12.

---

### Network/download failures

**Error message:**
```
curl: (6) Could not resolve host
```
or
```
wget: unable to resolve host address
```
or
```
Connection timed out
```

**Solution:**

1. Check your internet connection:
```bash
ping -c 3 google.com
```

2. If behind a proxy, set proxy variables:
```bash
export http_proxy="http://proxy.example.com:8080"
export https_proxy="http://proxy.example.com:8080"
```

3. Try the installation again. It will resume where it stopped.

4. If a specific download fails, try manually:
```bash
# For TOPCAT
wget https://www.star.bris.ac.uk/~mbt/topcat/topcat-full.jar -O ~/.astro/cache/topcat-full.jar
```

---

### No space left on device

**Error message:**
```
No space left on device
```

**Solution:**

Check available space:
```bash
df -h ~
```

You need at least 3 GB free. Clear space by:
```bash
# Remove old packages
sudo apt autoremove

# Clear apt cache
sudo apt clean

# Find large files in home directory
du -sh ~/* | sort -h | tail -10
```

---

## 2. TOPCAT Issues

TOPCAT on Ubuntu with Wayland requires special configuration. The `astro` launcher handles this automatically, but if you have problems, read this section.

### TOPCAT won't launch (no window appears)

**Error message:**
```
No display found
```
or
```
Exception in thread "main" java.awt.HeadlessException
```
or TOPCAT just doesn't open with no error message.

**Cause:** Wayland display server doesn't work directly with Java Swing applications like TOPCAT.

**Solution:**

The `astro topcat` command should handle this automatically. If it doesn't work:

1. First, verify XWayland is installed:
```bash
sudo apt install xwayland
```

2. Check if you're running Wayland:
```bash
echo $XDG_SESSION_TYPE
```
If it says `wayland`, continue with the fixes below.

3. Set the display variables manually and try again:
```bash
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)

# Now try launching TOPCAT
java -Djava.awt.headless=false -jar ~/.astro/cache/topcat-full.jar
```

4. If that works, add these lines to your `~/.zshrc` or `~/.bashrc`:
```bash
# Display configuration for GUI tools
export DISPLAY=${DISPLAY:-:0}
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)
```

Then reload:
```bash
source ~/.zshrc
```

---

### Java not found

**Error message:**
```
java: command not found
```
or
```
Error: JAVA_HOME is not set
```

**Solution:**

Install Java:
```bash
sudo apt update
sudo apt install openjdk-21-jdk openjdk-21-jre
```

Verify installation:
```bash
java -version
```

You should see output like:
```
openjdk version "21.0.x" 2024-xx-xx
```

---

### TOPCAT jar file not found

**Error message:**
```
Error: Unable to access jarfile
```
or
```
topcat-full.jar: No such file or directory
```

**Solution:**

Download TOPCAT manually:
```bash
mkdir -p ~/.astro/cache
wget https://www.star.bris.ac.uk/~mbt/topcat/topcat-full.jar -O ~/.astro/cache/topcat-full.jar
```

Verify download:
```bash
ls -la ~/.astro/cache/topcat-full.jar
```

File should be approximately 50 MB.

---

### TOPCAT window appears but is blank or corrupted

**Error message:**
No specific error, but TOPCAT window shows grey areas or doesn't render properly.

**Solution:**

Try forcing software rendering:
```bash
export _JAVA_AWT_WM_NONREPARENTING=1
java -Dsun.java2d.xrender=false -jar ~/.astro/cache/topcat-full.jar
```

Or try with a specific display backend:
```bash
GDK_BACKEND=x11 java -jar ~/.astro/cache/topcat-full.jar
```

---

### TOPCAT crashes immediately

**Error message:**
```
Segmentation fault
```
or
```
SIGBUS
```

**Solution:**

This is usually a Java/display driver conflict. Try:

1. Update your graphics drivers:
```bash
sudo apt update
sudo ubuntu-drivers autoinstall
```

2. Reboot your system.

3. Try running TOPCAT with Mesa software rendering:
```bash
export LIBGL_ALWAYS_SOFTWARE=1
astro topcat
```

---

### XAUTHORITY error

**Error message:**
```
Invalid MIT-MAGIC-COOKIE-1
```
or
```
Xlib: connection to ":0" refused by server
```

**Solution:**

The XAUTHORITY file location varies. Find yours:
```bash
ls /run/user/$(id -u)/.mutter-Xwaylandauth*
```

If no file is found, you might need to:
1. Log out and log back in
2. Or restart your display manager:
```bash
sudo systemctl restart gdm3
```

After logging back in, run:
```bash
astro repair
```

---

## 3. Jupyter Problems

### Kernel not found

**Error message in Jupyter:**
```
Kernel not found
```
or
```
No kernel named 'astro' found
```

**Solution:**

Reinstall the Jupyter kernel:
```bash
# Activate the environment
source ~/.astro/env/bin/activate

# Install the kernel
python -m ipykernel install --user --name=astro --display-name="Astronomy Python"

# Verify it's installed
jupyter kernelspec list

# Deactivate
deactivate
```

You should see `astro` in the kernel list.

---

### Jupyter won't start

**Error message:**
```
jupyter: command not found
```

**Solution:**

Jupyter should be installed in the astronomy environment. Use the launcher:
```bash
astro jupyter
```

If that fails, reinstall Jupyter:
```bash
source ~/.astro/env/bin/activate
pip install --upgrade jupyter jupyterlab
deactivate
```

---

### Port already in use

**Error message:**
```
Port 8888 is already in use
```
or
```
OSError: [Errno 98] Address already in use
```

**Solution:**

Option 1: Find and stop the existing Jupyter:
```bash
# Find what's using port 8888
lsof -i :8888

# Kill the process (replace PID with the actual number)
kill PID
```

Option 2: Use a different port:
```bash
source ~/.astro/env/bin/activate
jupyter lab --port=8889
```

---

### Jupyter opens but notebooks don't run

**Error message:**
```
Dead kernel
```
or cells just show `[*]` forever without completing.

**Solution:**

1. Restart the kernel: Click **Kernel** → **Restart Kernel**

2. If that doesn't work, check memory usage:
```bash
free -h
```

If memory is low, close other applications or restart the computer.

3. Reinstall the kernel:
```bash
astro repair
```

---

### Cannot save notebooks

**Error message:**
```
Permission denied: ~/.astro/notebooks/
```

**Solution:**

Fix permissions:
```bash
sudo chown -R $USER:$USER ~/.astro/notebooks
chmod -R 755 ~/.astro/notebooks
```

---

## 4. DS9 Issues

### DS9 display errors on Wayland

**Error message:**
```
couldn't connect to display
```
or DS9 window doesn't appear.

**Solution:**

DS9 needs the same display configuration as TOPCAT:
```bash
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)

ds9
```

Or use the launcher which sets these automatically:
```bash
astro ds9
```

---

### DS9 won't open FITS files

**Error message:**
```
Unable to open file
```
or
```
Error reading FITS file
```

**Solution:**

1. Check the file exists and is readable:
```bash
ls -la your_file.fits
```

2. Check if it's a valid FITS file:
```bash
# Using astropy
astro-activate
python -c "from astropy.io import fits; fits.info('your_file.fits')"
```

3. If the file is compressed, decompress it:
```bash
gunzip your_file.fits.gz
```

4. Try opening from command line with full path:
```bash
astro ds9 /full/path/to/your_file.fits
```

---

### DS9 not installed

**Error message:**
```
ds9: command not found
```

**Solution:**

Install DS9:
```bash
sudo apt update
sudo apt install saods9
```

Verify:
```bash
which ds9
```

---

## 5. Python Environment Issues

### Import errors

**Error message:**
```python
ModuleNotFoundError: No module named 'numpy'
```
or similar for astropy, matplotlib, etc.

**Solution:**

Make sure the environment is activated:
```bash
# Check if environment is active
echo $VIRTUAL_ENV

# If empty, activate it
astro-activate

# Or directly
source ~/.astro/env/bin/activate
```

If activated but still getting errors, reinstall the package:
```bash
pip install numpy scipy matplotlib pandas astropy
```

---

### Package conflicts

**Error message:**
```
ERROR: pip's dependency resolver does not currently take into account...
```
or
```
Requirement already satisfied but wrong version
```

**Solution:**

Reset the problematic packages:
```bash
source ~/.astro/env/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Reinstall core packages
pip install --upgrade --force-reinstall numpy scipy matplotlib pandas astropy

deactivate
```

---

### Corrupted environment

**Symptoms:**
- Multiple import errors
- Python crashes immediately
- `pip` doesn't work

**Solution:**

Rebuild the environment completely:
```bash
# Remove the old environment
rm -rf ~/.astro/env

# Recreate it
python3 -m venv ~/.astro/env

# Activate and install packages
source ~/.astro/env/bin/activate
pip install --upgrade pip setuptools wheel
pip install numpy scipy matplotlib pandas astropy jupyter jupyterlab plotly seaborn

# Reinstall Jupyter kernel
python -m ipykernel install --user --name=astro --display-name="Astronomy Python"

deactivate
```

Or use:
```bash
astro repair
```

---

### Wrong Python version in environment

**Error message:**
```
This module requires Python 3.10+
```

**Solution:**

Check which Python is being used:
```bash
astro-activate
python --version
which python
```

If it's the wrong version, recreate the environment with the correct Python:
```bash
rm -rf ~/.astro/env
python3.12 -m venv ~/.astro/env  # or python3.10 on Ubuntu 22.04
```

---

## 6. General Issues

### Commands not found after installation

**Error message:**
```
astro: command not found
```
or
```
astro-activate: command not found
```

**Cause:** The PATH wasn't updated or shell wasn't reloaded.

**Solution:**

1. Reload your shell:
```bash
source ~/.zshrc    # for zsh
source ~/.bashrc   # for bash
```

2. Or close the terminal and open a new one.

3. If still not working, add to PATH manually:
```bash
export PATH="$HOME/.local/bin:$HOME/.astro/bin:$PATH"
```

4. Make this permanent by adding to your shell config:
```bash
echo 'export PATH="$HOME/.local/bin:$HOME/.astro/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### Shell configuration problems

**Symptoms:**
- Environment variables not set
- Aliases not working
- PATH not updated

**Solution:**

Check your shell:
```bash
echo $SHELL
```

Edit the correct config file:
- For zsh: `~/.zshrc`
- For bash: `~/.bashrc`

Look for the astronomy configuration block:
```bash
grep -A 10 "ASTRO ENVIRONMENT" ~/.zshrc
```

If missing or corrupted, add it manually:
```bash
cat >> ~/.zshrc << 'EOF'

# ==== ASTRO ENVIRONMENT ====
export ASTRO_HOME="$HOME/.astro"
export PATH="$ASTRO_HOME/bin:$HOME/.local/bin:$PATH"
alias astro-activate='source "$ASTRO_HOME/env/bin/activate"'

# Display configuration for GUI tools
export DISPLAY=${DISPLAY:-:0}
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0}
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)
# ==== END ASTRO ====
EOF

source ~/.zshrc
```

---

### Environment variables not set

**Check current values:**
```bash
echo "ASTRO_HOME: $ASTRO_HOME"
echo "DISPLAY: $DISPLAY"
echo "WAYLAND_DISPLAY: $WAYLAND_DISPLAY"
echo "XAUTHORITY: $XAUTHORITY"
```

**If any are empty, set them:**
```bash
export ASTRO_HOME="$HOME/.astro"
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XAUTHORITY=$(ls /run/user/$(id -u)/.mutter-Xwaylandauth* 2>/dev/null | head -1)
```

---

## 7. Using astro doctor and astro repair

### astro doctor

The `doctor` command checks your installation for problems.

**Run it:**
```bash
astro doctor
```

**What it checks:**
| Check | What it means |
|-------|---------------|
| Python environment | Virtual environment exists and works |
| Core packages | numpy, scipy, matplotlib, pandas installed |
| Astropy | Astronomy library installed |
| Java | Java runtime for TOPCAT |
| TOPCAT | TOPCAT jar file present |
| DS9 | DS9 image viewer installed |
| Display config | Wayland/X11 configuration correct |
| Shell integration | PATH and aliases configured |

**Reading the output:**

```
✓ Python environment    OK
✓ Core packages         OK
✗ Java                  NOT FOUND
⚠ Display config        PARTIAL
```

- ✓ = Working correctly
- ✗ = Not installed or broken (needs fixing)
- ⚠ = Partially working (may cause problems)

---

### astro repair

The `repair` command automatically fixes common problems.

**Run it:**
```bash
astro repair
```

**What it fixes:**
- Reinstalls missing Python packages
- Re-downloads missing files (TOPCAT jar)
- Reconfigures shell settings
- Resets display environment variables
- Reinstalls Jupyter kernel

**When to use:**
- After `astro doctor` shows problems
- After system updates break something
- When tools stop working for unknown reasons
- After changing your shell (bash to zsh, etc.)

**Output example:**
```
Repairing astronomy environment...

✓ Python packages reinstalled
✓ TOPCAT jar verified
✓ Shell configuration updated
✓ Display variables reset
✓ Jupyter kernel reinstalled

Repair complete. Run 'astro doctor' to verify.
```

---

## Still Having Problems?

If none of the solutions above work:

1. **Collect diagnostic information:**
```bash
astro doctor > ~/astro-doctor-output.txt
echo "---" >> ~/astro-doctor-output.txt
echo "System info:" >> ~/astro-doctor-output.txt
lsb_release -a >> ~/astro-doctor-output.txt
echo "Shell: $SHELL" >> ~/astro-doctor-output.txt
echo "Display: $XDG_SESSION_TYPE" >> ~/astro-doctor-output.txt
```

2. **Open an issue on GitHub:**
   
   Go to: [github.com/RedChaosWolf92/astronomy-starter-kit/issues](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues)
   
   Include:
   - What you were trying to do
   - The exact error message
   - The output from the diagnostic commands above
   - Your Ubuntu version (22.04 or 24.04)

3. **Check existing issues:**
   
   Someone might have already solved your problem:
   [github.com/RedChaosWolf92/astronomy-starter-kit/issues](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues)

---

## Quick Reference: Common Error → Solution

| Error | Quick Fix |
|-------|-----------|
| `command not found: astro` | `source ~/.zshrc` or open new terminal |
| `java: command not found` | `sudo apt install openjdk-21-jdk` |
| `No display found` | Use `astro topcat` instead of `topcat` |
| `Port 8888 in use` | `lsof -i :8888` then `kill PID` |
| `ModuleNotFoundError` | `astro-activate` then `pip install module_name` |
| `Permission denied` | `sudo chown -R $USER:$USER ~/.astro` |
| `curl: command not found` | `sudo apt install curl` |
| Kernel not found in Jupyter | `astro repair` |
| TOPCAT won't launch | `astro repair` then `astro topcat` |

---

Happy troubleshooting! 🔧