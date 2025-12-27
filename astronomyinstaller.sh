#!/bin/bash
#
# Astronomy Starter Kit - Bootstrap Installer
# https://github.com/RedChaosWolf92/astronomy-starter-kit
#
# One-line installation:
#   curl -sSL https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh | bash
#
# Or download and run:
#   wget https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astronomyinstaller.sh
#   bash install.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
LAUNCHER_URL="https://raw.githubusercontent.com/RedChaosWolf92/astronomy-starter-kit/main/astro"
INSTALL_DIR="$HOME/.local/bin"

# Print header
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}          ${BLUE}ASTRONOMY STARTER KIT${NC} - Bootstrap               ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo -e ""

# Check system
if [ ! -f /etc/os-release ]; then
    echo -e "${RED}✗ Cannot detect Linux distribution${NC}"
    exit 1
fi

. /etc/os-release

if [[ "$ID" != "ubuntu" && "$ID_LIKE" != *"ubuntu"* && "$ID" != "debian" ]]; then
    echo -e "${YELLOW}⚠ Warning: This installer is optimized for Ubuntu/Debian${NC}"
    echo -e "${YELLOW}  Detected: $PRETTY_NAME${NC}"
    echo -e ""
fi

echo -e "${GREEN}✓${NC} System: $PRETTY_NAME"

# Detect shell configuration file (matches astro script method)
user_shell=$(basename "$SHELL")
case "$user_shell" in
    zsh)
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    bash)
        SHELL_CONFIG="$HOME/.bashrc"
        ;;
    *)
        SHELL_CONFIG="$HOME/.profile"
        ;;
esac

echo -e "${GREEN}✓${NC} Shell: $user_shell ($SHELL_CONFIG)"

# Check for curl
if ! command -v curl >/dev/null 2>&1; then
    echo -e "${BLUE}Installing curl...${NC}"
    sudo apt update -qq
    sudo apt install -y curl
fi

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download launcher
echo -e ""
echo -e "${BLUE}Downloading astro launcher...${NC}"
if ! curl -sSL "$LAUNCHER_URL" -o "$INSTALL_DIR/astro"; then
    echo -e "${RED}✗ Failed to download launcher${NC}"
    echo -e "  URL: $LAUNCHER_URL"
    exit 1
fi

chmod +x "$INSTALL_DIR/astro"
echo -e "${GREEN}✓${NC} Launcher downloaded to $INSTALL_DIR/astro"

# Add to PATH if needed
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo -e ""
    echo -e "${BLUE}Adding $INSTALL_DIR to PATH...${NC}"
    
    # Add PATH configuration to shell config
    cat >> "$SHELL_CONFIG" << 'EOFPATH'

# Astronomy Starter Kit - PATH configuration
export PATH="$HOME/.local/bin:$PATH"
EOFPATH
    
    # Export for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    echo -e "${GREEN}✓${NC} Added to PATH in $SHELL_CONFIG"
else
    echo -e "${GREEN}✓${NC} $INSTALL_DIR already in PATH"
fi

# Success message
echo -e ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}Bootstrap complete!${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e ""
echo -e "${BOLD}Next steps:${NC}"
echo -e ""
echo -e "1. ${YELLOW}Reload your shell:${NC}"
echo -e "   source $SHELL_CONFIG"
echo -e "   # Or close and reopen your terminal"
echo -e ""
echo -e "2. ${YELLOW}Run full installation (installs Python, TOPCAT, etc.):${NC}"
echo -e "   astro"
echo -e ""
echo -e "3. ${YELLOW}After installation, use these commands:${NC}"
echo -e "   astro jupyter      # Launch Jupyter Lab"
echo -e "   astro topcat       # Launch TOPCAT catalog tool"
echo -e "   astro ds9          # Launch DS9 FITS viewer"
echo -e "   astro python       # Python with astronomy libraries"
echo -e "   astro status       # Check installation status"
echo -e "   astro help         # Show all commands"
echo -e ""
echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"
echo -e "Documentation: https://github.com/RedChaosWolf92/astronomy-starter-kit"
echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"
echo -e ""
