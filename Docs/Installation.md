# Installation Guide

Welcome to the Astronomy Starter Kit! This guide walks you through installing your complete astronomy development environment on Ubuntu Linux.

---

## System Requirements

Before installing, ensure your system meets these requirements:

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Operating System** | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB |
| **Disk Space** | 3 GB free | 5 GB free |
| **Display Server** | X11 or Wayland | Either works |
| **Internet** | Required for installation | — |

The toolkit also works on Debian-based distributions (Linux Mint, Pop!_OS, etc.), though Ubuntu is the primary tested platform.

---

## Quick Installation

### One-Line Install (Recommended)

Open a terminal and run:

```bash
    curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh | bash
```

This single command downloads and runs the bootstrap installer, which sets up everything automatically.

### What Happens During Installation

The installer performs these steps in sequence:

1. Downloads the `astro` launcher to `~/.local/bin/`
2. Adds the launcher to your system PATH
3. Creates the astronomy environment directory at `~/.astro/`
4. Prompts you to reload your shell or open a new terminal

The first time you run `astro`, it completes the full setup by installing all astronomy tools. This takes approximately 10-15 minutes depending on your internet speed.

---

## Manual Installation

If you prefer more control over the installation process, follow these steps.

### Step 1: Download the Launcher

```bash
mkdir -p ~/.local/bin
curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astro -o ~/.local/bin/astro
chmod +x ~/.local/bin/astro
```

### Step 2: Add to PATH

For **zsh** users (check with `echo $SHELL`):

```bash
echo '' >> ~/.zshrc
echo '# Astronomy Starter Kit' >> ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For **bash** users:

```bash
echo '' >> ~/.bashrc
echo '# Astronomy Starter Kit' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Run Initial Setup

```bash
astro
```

On first run, the launcher automatically installs all astronomy tools. You'll see a progress display as each component installs.

---

## What Gets Installed

The Astronomy Starter Kit sets up a complete development environment with these components:

### Core Python Environment

A dedicated Python virtual environment with scientific computing libraries:

- **NumPy** — Numerical computing and array operations
- **SciPy** — Scientific algorithms and mathematics
- **Matplotlib** — Plotting and visualization
- **Pandas** — Data manipulation and analysis
- **Astropy** — Astronomy-specific tools and utilities

### Astronomy Applications

| Tool | Purpose | How to Launch |
|------|---------|---------------|
| **TOPCAT** | Catalog and table analysis | `astro topcat` |
| **DS9** | FITS image viewer | `astro ds9` |
| **Jupyter Lab** | Interactive notebooks | `astro jupyter` |

### Visual Development Tools

Custom scripts designed for accessibility and visual learning:

- `visual_foundations.py` — Enhanced visualization library with large fonts and high contrast
- `foundation_dashboard.py` — Interactive data exploration interface

---

## Installation Location

All components install to a single directory structure:

```
~/.astro/
├── bin/                    # Executable scripts and launchers
├── environments/
│   └── astro-foundation/   # Python virtual environment
├── scripts/                # Visual development tools
├── tools/
│   └── topcat/             # TOPCAT installation
└── config/                 # Configuration files
```

This self-contained structure keeps your system clean and makes uninstallation simple.

---

## Post-Installation Verification

After installation completes, verify everything works correctly.

### Check Installation Status

```bash
astro status
```

This displays the status of each component with visual indicators:

```
✓ Python Environment    installed
✓ TOPCAT               installed  
✓ DS9                  installed
✓ Jupyter Lab          installed
```

### Run Diagnostic Tests

```bash
astro doctor
```

The doctor command performs comprehensive checks and reports any issues found.

### Test Individual Tools

Launch each tool to confirm it works:

```bash
astro jupyter    # Opens Jupyter Lab in your browser
astro topcat     # Opens TOPCAT catalog viewer
astro ds9        # Opens DS9 image viewer
```

### Verify Python Environment

Activate the environment and test imports:

```bash
astro-activate
python -c "import numpy, scipy, matplotlib, astropy; print('All packages loaded successfully!')"
```

---

## Common Installation Issues

### Issue: "command not found: astro"

**Cause:** The PATH wasn't updated or the shell wasn't reloaded.

**Solution:** Either open a new terminal window, or reload your shell configuration:

```bash
source ~/.zshrc    # for zsh users
source ~/.bashrc   # for bash users
```

### Issue: "Permission denied" during installation

**Cause:** The script lacks execute permissions.

**Solution:** Add execute permission manually:

```bash
chmod +x ~/.local/bin/astro
```

### Issue: TOPCAT fails to start on Wayland

**Cause:** TOPCAT uses Java Swing, which requires additional configuration for Wayland display servers.

**Solution:** The `astro` launcher handles this automatically by setting the correct environment variables. If you're launching TOPCAT directly, use:

```bash
GDK_BACKEND=x11 topcat
```

See the [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed Wayland solutions.

### Issue: "curl: command not found"

**Cause:** curl isn't installed on your system.

**Solution:** Install curl first:

```bash
sudo apt update
sudo apt install curl
```

### Issue: Installation hangs or times out

**Cause:** Network issues or slow connection.

**Solution:** 

1. Check your internet connection
2. Try again — the installer resumes where it left off
3. If behind a proxy, configure your proxy settings before running the installer

### Issue: "No space left on device"

**Cause:** Insufficient disk space.

**Solution:** Free up at least 3 GB of disk space and retry:

```bash
df -h ~    # Check available space
```

### Issue: Python package installation fails

**Cause:** Missing system dependencies for compiling Python packages.

**Solution:** Install build essentials:

```bash
sudo apt install build-essential python3-dev
astro repair    # Re-runs package installation
```

---

## Updating the Toolkit

To update to the latest version:

```bash
astro update
```

This downloads the newest versions of all components while preserving your configurations.

---

## Uninstallation

To completely remove the Astronomy Starter Kit:

```bash
astro uninstall
```

Or remove manually:

```bash
rm -rf ~/.astro
rm ~/.local/bin/astro
```

Then remove the PATH lines from your shell configuration file (`~/.zshrc` or `~/.bashrc`).

---

## Getting Help

If you encounter issues not covered here:

1. Run `astro doctor` for automated diagnostics
2. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Review the [FAQ](FAQ.md)
4. [Open an issue](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) on GitHub

---

## Next Steps

Once installation is complete, you're ready to start exploring:

- **New to the toolkit?** Read the [User Guide](USER_GUIDE.md)
- **Ready to analyze data?** Launch Jupyter with `astro jupyter`
- **Have catalog files?** Open them with `astro topcat your_catalog.fits`

Happy observing! 🔭