# Development Guide

Welcome to the Astronomy Starter Kit development documentation. This guide helps you understand the codebase and contribute to the project.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Contributing Guidelines](#3-contributing-guidelines)
4. [Development Setup](#4-development-setup)
5. [Code Style](#5-code-style)
6. [Adding New Features](#6-adding-new-features)
7. [Release Process](#7-release-process)

---

## 1. Project Overview

### Purpose

The Astronomy Starter Kit provides a complete, ready-to-use astronomy development environment for Linux. It removes the complexity of setting up Python, installing astronomy tools, and configuring display systems.

### Target Users

- Astronomy students learning data analysis
- Researchers who need a quick, working environment
- Educators teaching astronomy computing
- Anyone new to Linux-based astronomy tools

### Design Philosophy

The project follows three core principles:

**Zero Configuration**

Users should not need to configure anything. The installer detects the system, chooses appropriate settings, and handles edge cases automatically. A user runs one command and gets a working environment.

**Self-Healing**

When things break (and they will), the toolkit should fix itself. The `astro doctor` command diagnoses problems, and `astro repair` fixes them automatically. Users should rarely need to troubleshoot manually.

**Accessibility First**

All tools, documentation, and interfaces prioritize clarity. This means large fonts in visualizations, high-contrast color schemes, clear error messages, and documentation that assumes no prior Linux experience.

---

## 2. Repository Structure

```
astronomy-starter-kit/
│
├── astro                       # Main launcher script (bash)
├── astronomyinstaller.sh       # Bootstrap installer
├── README.md                   # Project landing page
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines (brief)
├── CODE_OF_CONDUCT.md          # Community standards
├── .gitignore                  # Git ignore rules
│
├── docs/                       # Documentation
│   ├── INSTALLATION.md         # Detailed install guide
│   ├── USER_GUIDE.md           # How to use the toolkit
│   ├── TROUBLESHOOTING.md      # Problem solutions
│   ├── DEVELOPMENT.md          # This file
│   └── FAQ.md                  # Common questions
│
├── scripts/                    # Python helper scripts
│   ├── visual_foundations.py   # Visualization library
│   ├── foundation_dashboard.py # Interactive dashboard
│   └── test_foundation.py      # Environment tests
│
├── examples/                   # Example notebooks
│   └── notebooks/
│       ├── 01_getting_started.ipynb
│       ├── 02_visual_basics.ipynb
│       └── 03_data_analysis.ipynb
│
├── tests/                      # Test scripts
│   ├── test_install.sh         # Installation tests
│   └── test_environment.sh     # Environment validation
│
└── .github/                    # GitHub configuration
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── workflows/
        └── test.yml            # CI/CD pipeline
```

### Key Files Explained

#### astro (Main Launcher)

The heart of the project. This bash script handles:

- First-run detection and automatic installation
- Command routing (`astro jupyter`, `astro topcat`, etc.)
- State management for tracking installed components
- Self-repair capabilities

Location after installation: `~/.local/bin/astro`

#### astronomyinstaller.sh (Bootstrap Installer)

Downloads and sets up the `astro` launcher. This is what users run first:

```bash
curl -sSL https://raw.githubusercontent.com/.../astronomyinstaller.sh | bash
```

It only downloads the launcher and configures PATH. The actual tool installation happens on first `astro` run.

#### scripts/ Directory

Python files that extend functionality:

| File | Purpose |
|------|---------|
| `visual_foundations.py` | Library for accessible visualizations |
| `foundation_dashboard.py` | Interactive data exploration tool |
| `test_foundation.py` | Tests Python environment health |

### How Components Interact

```
User runs "astro jupyter"
         │
         ▼
    ┌─────────┐
    │  astro  │ ◄── Main launcher (bash)
    └────┬────┘
         │
         ▼
   Check state file
   (~/.astro/.state)
         │
         ├── Not installed? ──► Run installation
         │
         ▼
   Route to command
         │
         ├── jupyter ──► Activate env, launch Jupyter
         ├── topcat  ──► Set display vars, launch Java
         ├── doctor  ──► Run test_foundation.py
         └── repair  ──► Reinstall components
```

---

## 3. Contributing Guidelines

### First Time Contributors

New to open source? Welcome! Here's the process:

1. **Find something to work on**
   - Check [Issues](https://github.com/RedChaosWolf92/astronomy-starter-kit/issues) for `good first issue` labels
   - Or propose your own improvement

2. **Discuss before coding**
   - Comment on the issue to say you're working on it
   - For new features, open an issue first to discuss

3. **Make your changes**
   - Fork, clone, branch, code, test, push, PR (details below)

### Fork and Clone

```bash
# Fork on GitHub first (click the Fork button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/astronomy-starter-kit.git
cd astronomy-starter-kit

# Add upstream remote
git remote add upstream https://github.com/RedChaosWolf92/astronomy-starter-kit.git

# Keep your fork updated
git fetch upstream
git merge upstream/main
```

### Making Changes

```bash
# Create a branch for your work
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Test your changes (see Testing section)
./tests/test_install.sh

# Commit with a clear message
git add .
git commit -m "Add feature: description of what you did"

# Push to your fork
git push origin feature/your-feature-name
```

### Commit Message Format

Write clear commit messages:

```
Add feature: brief description

- Detail about what changed
- Why this change was needed
- Any important notes

Fixes #123
```

Examples of good commit messages:

- `Fix: TOPCAT display on Wayland with multiple monitors`
- `Add: astro backup command for exporting notebooks`
- `Docs: clarify XAUTHORITY troubleshooting steps`
- `Test: add coverage for Python 3.12 environment`

### Pull Request Process

1. **Before submitting:**
   - Test on a fresh Ubuntu VM if possible
   - Update documentation if needed
   - Run the test scripts

2. **Create the PR:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **After submitting:**
   - Respond to review comments
   - Make requested changes
   - Keep the PR updated with main branch

### Testing Requirements

All changes must pass these tests:

| Change Type | Required Tests |
|-------------|----------------|
| `astro` script changes | `test_install.sh`, `test_environment.sh` |
| Python script changes | `test_foundation.py` |
| Documentation changes | Manual review, link checking |
| New commands | All tests + new test for the command |

---

## 4. Development Setup

### Local Development Environment

You need:

- Ubuntu 22.04 or 24.04 (or VM)
- Git
- Text editor (VS Code, vim, etc.)

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/astronomy-starter-kit.git
cd astronomy-starter-kit

# Make scripts executable
chmod +x astro astronomyinstaller.sh
chmod +x tests/*.sh
```

### Testing on Fresh Ubuntu VM

For reliable testing, use a fresh VM:

**Using Multipass (recommended):**

```bash
# Install Multipass
sudo snap install multipass

# Create Ubuntu 24.04 VM
multipass launch 24.04 --name astro-test --memory 4G --disk 20G

# Enter the VM
multipass shell astro-test

# Inside VM: test the installation
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/astronomy-starter-kit/YOUR_BRANCH/astronomyinstaller.sh | bash
```

**Using VirtualBox:**

1. Download Ubuntu 24.04 ISO
2. Create VM with 4GB RAM, 20GB disk
3. Install Ubuntu
4. Test the installation inside the VM

### Running Tests

```bash
# Run installation tests
./tests/test_install.sh

# Run environment tests (after installation)
./tests/test_environment.sh

# Run Python tests
source ~/.astro/env/bin/activate
python scripts/test_foundation.py
```

### Testing Your Changes

Before submitting a PR:

```bash
# 1. Test on your development machine
./tests/test_environment.sh

# 2. Test on a fresh VM
multipass launch 24.04 --name test-vm
multipass transfer astro test-vm:/home/ubuntu/
multipass shell test-vm
# Inside VM:
chmod +x astro
./astro
./astro doctor
```

---

## 5. Code Style

### Bash Script Conventions

The `astro` script follows these patterns:

#### File Header

```bash
#!/bin/bash
#
# ASTRONOMY STARTER KIT - Component Name
# Brief description of what this script does
#
# Usage:
#   command [options]
#
```

#### Color Codes

Use these standard colors throughout:

```bash
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'  # No Color
```

#### Section Headers

Organize code into sections:

```bash
#==============================================================================
# SECTION NAME
#==============================================================================
```

#### Function Naming

```bash
# Use snake_case for function names
install_python_environment() {
    # ...
}

# Prefix with cmd_ for command handlers
cmd_jupyter() {
    # ...
}

# Prefix with is_ or check_ for boolean functions
is_installed() {
    # ...
}
```

#### Output Functions

Use consistent output helpers:

```bash
log() {
    echo -e "${BLUE}[$(date +%T)]${NC} $*"
}

success() {
    echo -e "${GREEN}✓${NC} $*"
}

error() {
    echo -e "${RED}✗${NC} $*"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}
```

### Error Handling Patterns

Always handle errors gracefully:

```bash
# Use set -e at the top (exit on error)
set -e

# For commands that might fail, handle explicitly
if ! command -v java >/dev/null; then
    error "Java not found"
    echo "Install with: sudo apt install openjdk-21-jdk"
    exit 1
fi

# For optional failures, use || true
some_command || true

# For downloads, always check success
if ! curl -sSL "$URL" -o "$OUTPUT"; then
    error "Download failed: $URL"
    exit 1
fi
```

### Comment Standards

```bash
# Single line comments explain what
# Use for brief explanations

# Multi-line comments for complex logic
# Explain WHY something is done, not just what
# Include context that isn't obvious from the code

# TODO: prefix for future work
# FIXME: prefix for known issues
# NOTE: prefix for important information
```

### Python Code Style

Python scripts in `scripts/` follow:

- PEP 8 style guide
- Docstrings for all functions
- Type hints where helpful
- Clear variable names

```python
def create_accessible_plot(
    data: np.ndarray,
    title: str,
    xlabel: str = "X",
    ylabel: str = "Y"
) -> plt.Figure:
    """
    Create a plot with accessibility features.
    
    Args:
        data: Array of values to plot
        title: Plot title (displayed in large font)
        xlabel: X-axis label
        ylabel: Y-axis label
    
    Returns:
        Matplotlib figure object
    """
    # Implementation...
```

---

## 6. Adding New Features

### Adding a New Command to astro

To add a new command like `astro backup`:

**Step 1: Add the command handler function**

```bash
#==============================================================================
# COMMAND: BACKUP
#==============================================================================

cmd_backup() {
    log "Creating backup..."
    
    local backup_dir="$HOME/astro-backup-$(date +%Y%m%d)"
    mkdir -p "$backup_dir"
    
    # Copy notebooks
    if [ -d "$ASTRO_HOME/notebooks" ]; then
        cp -r "$ASTRO_HOME/notebooks" "$backup_dir/"
        success "Notebooks backed up"
    fi
    
    # Copy configuration
    cp "$ASTRO_HOME/.state" "$backup_dir/" 2>/dev/null || true
    
    success "Backup created: $backup_dir"
}
```

**Step 2: Add to the command router**

Find the `main()` function and add your command:

```bash
main() {
    # ... existing code ...
    
    case "${1:-}" in
        jupyter)
            shift
            cmd_jupyter "$@"
            ;;
        backup)        # <-- Add your new command
            cmd_backup
            ;;
        # ... other commands ...
    esac
}
```

**Step 3: Add to help text**

Update the `show_menu()` or help function:

```bash
echo -e "  ${YELLOW}astro backup${NC}       Create backup of notebooks"
```

**Step 4: Add tests**

Add a test in `tests/test_environment.sh`:

```bash
test_backup_command() {
    echo "Testing backup command..."
    if astro backup; then
        success "Backup command works"
    else
        error "Backup command failed"
        return 1
    fi
}
```

**Step 5: Update documentation**

Add to `docs/USER_GUIDE.md` command reference.

### Adding a New Tool

To add a new astronomy tool (like Aladin):

**Step 1: Create installation function**

```bash
install_aladin() {
    if is_installed "aladin"; then
        return 0
    fi
    
    log "Installing Aladin..."
    
    # Download
    mkdir -p "$ASTRO_HOME/tools/aladin"
    wget -q "http://aladin.u-strasbg.fr/java/Aladin.jar" \
        -O "$ASTRO_HOME/tools/aladin/Aladin.jar"
    
    # Create launcher
    cat > "$ASTRO_BIN/aladin" << 'EOF'
#!/bin/bash
java -jar "$HOME/.astro/tools/aladin/Aladin.jar" "$@"
EOF
    chmod +x "$ASTRO_BIN/aladin"
    
    mark_installed "aladin"
    success "Aladin installed"
}
```

**Step 2: Add to installation flow**

In the main installation function, add:

```bash
run_full_install() {
    # ... existing installations ...
    install_aladin
    # ...
}
```

**Step 3: Add launch command**

```bash
cmd_aladin() {
    if ! is_installed "aladin"; then
        error "Aladin not installed. Run 'astro repair'"
        exit 1
    fi
    
    log "Launching Aladin..."
    exec "$ASTRO_BIN/aladin" "$@"
}
```

**Step 4: Add to doctor checks**

```bash
cmd_doctor() {
    # ... existing checks ...
    
    # Check Aladin
    if [ -f "$ASTRO_HOME/tools/aladin/Aladin.jar" ]; then
        success "Aladin jar present"
    else
        error "Aladin jar missing"
    fi
}
```

### State Management System

The toolkit tracks installation state in `~/.astro/.state`:

```bash
# Example .state file contents
fully_installed=true
installed_python_env=true
installed_topcat=true
installed_aladin=true
install_date=2024-01-15
```

**Reading state:**

```bash
get_state() {
    local key=$1
    [ -f "$STATE_FILE" ] && grep "^${key}=" "$STATE_FILE" | cut -d'=' -f2
}

# Usage
if [ "$(get_state fully_installed)" == "true" ]; then
    echo "Already installed"
fi
```

**Writing state:**

```bash
set_state() {
    local key=$1
    local value=$2
    mkdir -p "$ASTRO_HOME"
    
    # Remove existing entry
    if [ -f "$STATE_FILE" ]; then
        sed -i "/^${key}=/d" "$STATE_FILE"
    fi
    
    # Add new entry
    echo "${key}=${value}" >> "$STATE_FILE"
}

# Usage
set_state "installed_aladin" "true"
```

**Component tracking:**

```bash
is_installed() {
    local component=$1
    [ "$(get_state "installed_${component}")" == "true" ]
}

mark_installed() {
    local component=$1
    set_state "installed_${component}" "true"
}

# Usage
if ! is_installed "topcat"; then
    install_topcat
fi
mark_installed "topcat"
```

---

## 7. Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

Examples:
1.0.0 - Initial release
1.1.0 - New feature added
1.1.1 - Bug fix
2.0.0 - Breaking changes
```

**When to increment:**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fixes | PATCH | 1.0.0 → 1.0.1 |
| New features (backward compatible) | MINOR | 1.0.1 → 1.1.0 |
| Breaking changes | MAJOR | 1.1.0 → 2.0.0 |

### Creating a Release

**Step 1: Update version number**

Edit `astro` script:

```bash
VERSION="1.2.0"  # Update this line
```

**Step 2: Update CHANGELOG**

Create or update `CHANGELOG.md`:

```markdown
## [1.2.0] - 2024-XX-XX

### Added
- New `astro backup` command
- Aladin sky atlas integration

### Fixed
- TOPCAT display on multi-monitor Wayland setups

### Changed
- Improved error messages for Java detection
```

**Step 3: Commit the release**

```bash
git add .
git commit -m "Release v1.2.0"
git tag -a v1.2.0 -m "Version 1.2.0"
git push origin main --tags
```

**Step 4: Create GitHub Release**

1. Go to repository → Releases → "Create a new release"
2. Choose the tag you just created
3. Title: "Astronomy Starter Kit v1.2.0"
4. Description: Copy from CHANGELOG
5. Attach `astro` script as an asset
6. Publish

### Updating Documentation

When releasing, ensure these are updated:

- [ ] README.md (if features changed)
- [ ] docs/USER_GUIDE.md (new commands)
- [ ] docs/INSTALLATION.md (if requirements changed)
- [ ] docs/TROUBLESHOOTING.md (new issues/solutions)
- [ ] docs/FAQ.md (common questions about new features)

### Post-Release

After releasing:

1. Announce on relevant channels (if any)
2. Monitor issues for bug reports
3. Update any external documentation
4. Consider a blog post for major releases

---

## Questions?

- Open an issue for questions about contributing
- Check existing issues and PRs for examples
- Read through the codebase — it's well-commented

Thank you for contributing to making astronomy tools more accessible! 🔭