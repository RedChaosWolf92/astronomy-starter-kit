#!/usr/bin/env python3
"""
Astronomy Foundation Environment Test
=====================================
Comprehensive testing of the astronomy development environment setup.

This script verifies that all required packages are installed and working
correctly, checks environment configuration, and runs functional tests
to ensure the astronomy starter kit is ready for use.

Part of the Astronomy Starter Kit
https://github.com/RedChaosWolf92/astronomy-starter-kit

Author: Greg (RedChaosWolf92)
License: MIT

Usage:
------
    python test_foundation.py
    
    # Or via the astro command (if configured):
    astro doctor

Exit Codes:
-----------
    0 - All critical tests passed
    1 - One or more critical tests failed
"""

import sys
import os
import importlib
import traceback
from datetime import datetime

# =============================================================================
# TERMINAL COLOR SUPPORT
# =============================================================================

class Colors:
    """ANSI color codes for terminal output."""
    
    # Check if terminal supports colors
    ENABLED = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    # Color codes
    RESET = '\033[0m' if ENABLED else ''
    BOLD = '\033[1m' if ENABLED else ''
    DIM = '\033[2m' if ENABLED else ''
    
    # Foreground colors
    RED = '\033[91m' if ENABLED else ''
    GREEN = '\033[92m' if ENABLED else ''
    YELLOW = '\033[93m' if ENABLED else ''
    BLUE = '\033[94m' if ENABLED else ''
    MAGENTA = '\033[95m' if ENABLED else ''
    CYAN = '\033[96m' if ENABLED else ''
    WHITE = '\033[97m' if ENABLED else ''
    
    @classmethod
    def success(cls, text):
        return f"{cls.GREEN}{text}{cls.RESET}"
    
    @classmethod
    def error(cls, text):
        return f"{cls.RED}{text}{cls.RESET}"
    
    @classmethod
    def warning(cls, text):
        return f"{cls.YELLOW}{text}{cls.RESET}"
    
    @classmethod
    def info(cls, text):
        return f"{cls.CYAN}{text}{cls.RESET}"
    
    @classmethod
    def header(cls, text):
        return f"{cls.BOLD}{cls.BLUE}{text}{cls.RESET}"


# =============================================================================
# TEST RESULT TRACKING
# =============================================================================

class TestResult:
    """Track individual test results."""
    
    PASS = 'pass'
    FAIL = 'fail'
    WARN = 'warn'
    SKIP = 'skip'
    
    def __init__(self, name, status, message, details=None, fix_hint=None):
        self.name = name
        self.status = status
        self.message = message
        self.details = details
        self.fix_hint = fix_hint
    
    def __str__(self):
        if self.status == self.PASS:
            icon = Colors.success("✓")
        elif self.status == self.FAIL:
            icon = Colors.error("✗")
        elif self.status == self.WARN:
            icon = Colors.warning("?")
        else:
            icon = Colors.info("○")
        
        return f"{icon} {self.message}"


class TestResults:
    """Collection of test results."""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add(self, result):
        self.results.append(result)
    
    @property
    def passed(self):
        return sum(1 for r in self.results if r.status == TestResult.PASS)
    
    @property
    def failed(self):
        return sum(1 for r in self.results if r.status == TestResult.FAIL)
    
    @property
    def warnings(self):
        return sum(1 for r in self.results if r.status == TestResult.WARN)
    
    @property
    def total(self):
        return len(self.results)
    
    @property
    def success_rate(self):
        if self.total == 0:
            return 0
        return (self.passed / self.total) * 100
    
    @property
    def duration(self):
        return (datetime.now() - self.start_time).total_seconds()


# =============================================================================
# PACKAGE TESTING FUNCTIONS
# =============================================================================

def test_import(package_name, import_name=None, min_version=None):
    """
    Test if a package can be imported.
    
    Parameters:
    -----------
    package_name : str
        Display name of the package
    import_name : str, optional
        Actual import name (if different from package_name)
    min_version : str, optional
        Minimum required version
        
    Returns:
    --------
    TestResult
    """
    if import_name is None:
        import_name = package_name.lower()
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        
        # Check version if specified
        if min_version and version != 'unknown':
            from packaging import version as pkg_version
            if pkg_version.parse(version) < pkg_version.parse(min_version):
                return TestResult(
                    package_name,
                    TestResult.WARN,
                    f"{package_name} v{version} (recommend >= {min_version})",
                    fix_hint=f"pip install --upgrade {import_name}"
                )
        
        return TestResult(
            package_name,
            TestResult.PASS,
            f"{package_name} v{version}"
        )
    except ImportError as e:
        return TestResult(
            package_name,
            TestResult.FAIL,
            f"{package_name} not found",
            details=str(e),
            fix_hint=f"pip install {import_name}"
        )


def test_package_group(group_name, packages):
    """
    Test a group of related packages.
    
    Parameters:
    -----------
    group_name : str
        Name of the package group
    packages : list of tuples
        Each tuple: (display_name, import_name, min_version)
        
    Returns:
    --------
    list of TestResult
    """
    results = []
    for pkg_info in packages:
        if isinstance(pkg_info, str):
            results.append(test_import(pkg_info))
        elif len(pkg_info) == 1:
            results.append(test_import(pkg_info[0]))
        elif len(pkg_info) == 2:
            results.append(test_import(pkg_info[0], pkg_info[1]))
        else:
            results.append(test_import(pkg_info[0], pkg_info[1], pkg_info[2]))
    return results


# =============================================================================
# MAIN TEST CATEGORIES
# =============================================================================

def test_core_scientific_stack():
    """Test core scientific computing packages."""
    packages = [
        ('NumPy', 'numpy', '1.20.0'),
        ('SciPy', 'scipy', '1.7.0'),
        ('Matplotlib', 'matplotlib', '3.4.0'),
        ('Pandas', 'pandas', '1.3.0'),
    ]
    return test_package_group("Core Scientific Stack", packages)


def test_astronomy_libraries():
    """Test astronomy-specific packages."""
    packages = [
        ('Astropy', 'astropy', '5.0'),
    ]
    results = test_package_group("Astronomy Libraries", packages)
    
    # Additional astropy submodule tests
    try:
        import astropy.units as u
        import astropy.coordinates as coord
        results.append(TestResult(
            'Astropy Units',
            TestResult.PASS,
            "Astropy units & coordinates modules working"
        ))
    except ImportError as e:
        results.append(TestResult(
            'Astropy Units',
            TestResult.FAIL,
            "Astropy submodules failed",
            details=str(e)
        ))
    
    return results


def test_visualization_tools():
    """Test visualization packages."""
    packages = [
        ('Plotly', 'plotly', '5.0.0'),
        ('Seaborn', 'seaborn', '0.11.0'),
    ]
    results = test_package_group("Visualization Tools", packages)
    
    # Bokeh is optional
    try:
        import bokeh
        results.append(TestResult(
            'Bokeh',
            TestResult.PASS,
            f"Bokeh v{bokeh.__version__} (optional)"
        ))
    except ImportError:
        results.append(TestResult(
            'Bokeh',
            TestResult.WARN,
            "Bokeh not installed (optional)",
            fix_hint="pip install bokeh"
        ))
    
    return results


def test_jupyter_components():
    """Test Jupyter ecosystem packages."""
    results = []
    
    # JupyterLab
    try:
        import jupyterlab
        results.append(TestResult(
            'JupyterLab',
            TestResult.PASS,
            f"JupyterLab v{jupyterlab.__version__}"
        ))
    except ImportError:
        results.append(TestResult(
            'JupyterLab',
            TestResult.WARN,
            "JupyterLab not installed (optional for notebooks)",
            fix_hint="pip install jupyterlab"
        ))
    
    # IPython widgets
    try:
        import ipywidgets
        results.append(TestResult(
            'IPyWidgets',
            TestResult.PASS,
            f"IPyWidgets v{ipywidgets.__version__}"
        ))
    except ImportError:
        results.append(TestResult(
            'IPyWidgets',
            TestResult.WARN,
            "IPyWidgets not installed (optional for interactive notebooks)",
            fix_hint="pip install ipywidgets"
        ))
    
    return results


def test_development_tools():
    """Test development and testing packages."""
    results = []
    
    # Pytest
    try:
        import pytest
        results.append(TestResult(
            'Pytest',
            TestResult.PASS,
            f"Pytest v{pytest.__version__}"
        ))
    except ImportError:
        results.append(TestResult(
            'Pytest',
            TestResult.WARN,
            "Pytest not installed (optional for testing)",
            fix_hint="pip install pytest"
        ))
    
    # h5py for HDF5 files
    try:
        import h5py
        results.append(TestResult(
            'h5py',
            TestResult.PASS,
            f"h5py v{h5py.__version__}"
        ))
    except ImportError:
        results.append(TestResult(
            'h5py',
            TestResult.WARN,
            "h5py not installed (optional for HDF5 files)",
            fix_hint="pip install h5py"
        ))
    
    # scikit-learn (optional)
    try:
        import sklearn
        results.append(TestResult(
            'Scikit-learn',
            TestResult.PASS,
            f"Scikit-learn v{sklearn.__version__}"
        ))
    except ImportError:
        results.append(TestResult(
            'Scikit-learn',
            TestResult.WARN,
            "Scikit-learn not installed (optional for ML)",
            fix_hint="pip install scikit-learn"
        ))
    
    return results


def test_environment_config():
    """Test environment configuration."""
    results = []
    
    # Check ASTRO_HOME environment variable
    astro_home = os.environ.get('ASTRO_HOME')
    if astro_home:
        if os.path.isdir(astro_home):
            results.append(TestResult(
                'ASTRO_HOME',
                TestResult.PASS,
                f"ASTRO_HOME set: {astro_home}"
            ))
        else:
            results.append(TestResult(
                'ASTRO_HOME',
                TestResult.WARN,
                f"ASTRO_HOME directory not found: {astro_home}",
                fix_hint="mkdir -p $ASTRO_HOME"
            ))
    else:
        # Check alternative names
        alt_names = ['ASTRO_DEV_HOME', 'ASTRONOMY_HOME']
        found = False
        for alt in alt_names:
            val = os.environ.get(alt)
            if val:
                results.append(TestResult(
                    'ASTRO_HOME',
                    TestResult.PASS,
                    f"{alt} set: {val}"
                ))
                found = True
                break
        
        if not found:
            results.append(TestResult(
                'ASTRO_HOME',
                TestResult.WARN,
                "ASTRO_HOME not set (optional)",
                fix_hint="export ASTRO_HOME=~/.astro"
            ))
    
    # Check Python environment isolation
    executable = sys.executable
    venv_indicators = ['astro', 'env', 'venv', '.astro']
    in_venv = any(ind in executable.lower() for ind in venv_indicators)
    
    if in_venv or hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        env_name = os.path.basename(os.path.dirname(executable))
        results.append(TestResult(
            'Virtual Environment',
            TestResult.PASS,
            f"Using isolated environment: {env_name}"
        ))
    else:
        results.append(TestResult(
            'Virtual Environment',
            TestResult.WARN,
            f"Using system Python: {executable}",
            details="Recommend using a virtual environment for isolation",
            fix_hint="python -m venv ~/.astro/env && source ~/.astro/env/bin/activate"
        ))
    
    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 9):
        results.append(TestResult(
            'Python Version',
            TestResult.PASS,
            f"Python {py_version.major}.{py_version.minor}.{py_version.micro}"
        ))
    elif py_version >= (3, 8):
        results.append(TestResult(
            'Python Version',
            TestResult.WARN,
            f"Python {py_version.major}.{py_version.minor} (recommend 3.9+)"
        ))
    else:
        results.append(TestResult(
            'Python Version',
            TestResult.FAIL,
            f"Python {py_version.major}.{py_version.minor} (requires 3.8+)",
            fix_hint="Install Python 3.9 or later"
        ))
    
    return results


def test_visual_foundations():
    """Test the visual_foundations library."""
    results = []
    
    # Try to import from same directory first, then from path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    try:
        from visual_foundations import VisualFoundations
        vf = VisualFoundations()
        results.append(TestResult(
            'Visual Foundations Import',
            TestResult.PASS,
            "visual_foundations.py loaded successfully"
        ))
        
        # Test data generation
        try:
            x, y, title = vf.create_sample_data('spectrum', 50)
            assert len(x) == 50, "Data length mismatch"
            results.append(TestResult(
                'Visual Foundations Data',
                TestResult.PASS,
                "Sample data generation working"
            ))
        except Exception as e:
            results.append(TestResult(
                'Visual Foundations Data',
                TestResult.FAIL,
                f"Data generation failed: {e}"
            ))
        
        # Test color scheme
        try:
            color = vf.get_color('primary')
            assert color.startswith('#'), "Invalid color format"
            results.append(TestResult(
                'Visual Foundations Colors',
                TestResult.PASS,
                f"Color scheme available ({len(vf.colors)} colors)"
            ))
        except Exception as e:
            results.append(TestResult(
                'Visual Foundations Colors',
                TestResult.WARN,
                f"Color scheme issue: {e}"
            ))
            
    except ImportError as e:
        results.append(TestResult(
            'Visual Foundations Import',
            TestResult.WARN,
            "visual_foundations.py not found (optional)",
            details=str(e),
            fix_hint="Ensure visual_foundations.py is in the scripts/ directory"
        ))
    
    return results


# =============================================================================
# FUNCTIONAL TESTS
# =============================================================================

def test_numpy_operations():
    """Test basic NumPy operations."""
    results = []
    
    try:
        import numpy as np
        
        # Array creation
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x) * np.exp(-x / 4)
        
        # Basic operations
        mean_val = np.mean(y)
        std_val = np.std(y)
        max_val = np.max(y)
        
        results.append(TestResult(
            'NumPy Array Operations',
            TestResult.PASS,
            f"Array ops working (mean={mean_val:.4f}, std={std_val:.4f})"
        ))
        
        # FFT test
        fft_result = np.fft.fft(y)
        results.append(TestResult(
            'NumPy FFT',
            TestResult.PASS,
            f"FFT working (output shape: {fft_result.shape})"
        ))
        
    except Exception as e:
        results.append(TestResult(
            'NumPy Operations',
            TestResult.FAIL,
            f"NumPy test failed: {e}"
        ))
    
    return results


def test_matplotlib_plotting():
    """Test matplotlib plotting capability (without display)."""
    results = []
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend for testing
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create a test figure
        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'b-', linewidth=2)
        ax.set_title('Test Plot')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Save to temp file to verify it works
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_path = f.name
        
        fig.savefig(temp_path, dpi=72)
        plt.close(fig)
        
        # Verify file was created
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            os.unlink(temp_path)  # Clean up
            results.append(TestResult(
                'Matplotlib Plotting',
                TestResult.PASS,
                "Plot generation and saving working"
            ))
        else:
            results.append(TestResult(
                'Matplotlib Plotting',
                TestResult.FAIL,
                "Plot file not created properly"
            ))
            
    except Exception as e:
        results.append(TestResult(
            'Matplotlib Plotting',
            TestResult.FAIL,
            f"Plotting test failed: {e}"
        ))
    
    return results


def test_astropy_units():
    """Test Astropy units conversion."""
    results = []
    
    try:
        import astropy.units as u
        from astropy.coordinates import SkyCoord
        
        # Unit conversion
        distance_pc = 10 * u.pc
        distance_ly = distance_pc.to(u.lyr)
        
        results.append(TestResult(
            'Astropy Unit Conversion',
            TestResult.PASS,
            f"10 pc = {distance_ly.value:.2f} ly"
        ))
        
        # Coordinate system
        coord = SkyCoord(ra=10.68458*u.degree, dec=41.26917*u.degree, frame='icrs')
        results.append(TestResult(
            'Astropy Coordinates',
            TestResult.PASS,
            f"SkyCoord working (M31 position parsed)"
        ))
        
    except Exception as e:
        results.append(TestResult(
            'Astropy Functions',
            TestResult.FAIL,
            f"Astropy test failed: {e}"
        ))
    
    return results


# =============================================================================
# VISUAL TEST (OPTIONAL)
# =============================================================================

def run_visual_test(show_plot=True):
    """
    Create and optionally display a visual test plot.
    
    Parameters:
    -----------
    show_plot : bool
        If True, display the plot interactively
        
    Returns:
    --------
    bool : True if successful
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Don't use Agg backend for visual test
        if show_plot:
            import matplotlib
            # Try to use an interactive backend
            try:
                matplotlib.use('TkAgg')
            except:
                try:
                    matplotlib.use('Qt5Agg')
                except:
                    pass  # Use whatever is available
        
        # Set dark style for accessibility
        plt.style.use('dark_background')
        
        # Create test data
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x) * np.exp(-x / 4)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Main plot
        ax.plot(x, y, 'b-', linewidth=3, label='sin(x) × exp(-x/4)', alpha=0.9)
        ax.fill_between(x, 0, y, alpha=0.3, color='#3498DB')
        
        # Reference line
        ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
        
        # Styling
        ax.set_title('🔭 Astronomy Foundation Environment Test', 
                     fontsize=22, fontweight='bold', pad=20)
        ax.set_xlabel('X Values', fontsize=16, fontweight='bold')
        ax.set_ylabel('Y Values', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, linewidth=1)
        ax.legend(fontsize=14, loc='upper right')
        
        # Peak annotation
        max_idx = np.argmax(y)
        ax.annotate(
            f'Peak: ({x[max_idx]:.2f}, {y[max_idx]:.3f})',
            xy=(x[max_idx], y[max_idx]),
            xytext=(40, 30), textcoords='offset points',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F39C12', 
                      alpha=0.9, edgecolor='white'),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3',
                            linewidth=2, color='#F39C12')
        )
        
        # Status text box
        status_text = '✓ All visual components working!\n🔭 Foundation Environment Ready'
        props = dict(boxstyle='round', facecolor='#2ECC71', alpha=0.9, 
                     edgecolor='white', linewidth=2)
        ax.text(0.02, 0.98, status_text, transform=ax.transAxes,
                fontsize=14, fontweight='bold', verticalalignment='top',
                bbox=props, color='white')
        
        plt.tight_layout()
        
        if show_plot:
            print(f"\n{Colors.info('📊 Displaying visual test plot...')}")
            print(f"{Colors.info('   Close the plot window to continue.')}\n")
            plt.show()
        
        plt.close(fig)
        return True
        
    except Exception as e:
        print(f"{Colors.error(f'Visual test failed: {e}')}")
        return False


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def print_section(title, icon=""):
    """Print a formatted section header."""
    full_title = f"{icon} {title}" if icon else title
    print(f"\n{Colors.header(full_title)}")
    print(Colors.header("-" * 50))


def print_results(results, show_hints=True):
    """Print test results with optional fix hints."""
    for result in results:
        print(f"  {result}")
        if show_hints and result.fix_hint and result.status in [TestResult.FAIL, TestResult.WARN]:
            print(f"    {Colors.info('→ Fix:')} {result.fix_hint}")


def run_all_tests(visual=True, verbose=True):
    """
    Run all environment tests.
    
    Parameters:
    -----------
    visual : bool
        If True, show a visual test plot at the end
    verbose : bool
        If True, show detailed output
        
    Returns:
    --------
    int : Exit code (0 for success, 1 for failure)
    """
    # Initialize results tracker
    all_results = TestResults()
    
    # Print header
    print("\n" + "=" * 60)
    print(Colors.header("🔭 ASTRONOMY FOUNDATION ENVIRONMENT TEST"))
    print("=" * 60)
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Platform: {sys.platform}")
    print("=" * 60)
    
    # =========================================================================
    # TEST 1: Core Scientific Stack
    # =========================================================================
    print_section("Core Scientific Stack", "📦")
    results = test_core_scientific_stack()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 2: Astronomy Libraries
    # =========================================================================
    print_section("Astronomy Libraries", "🌟")
    results = test_astronomy_libraries()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 3: Visualization Tools
    # =========================================================================
    print_section("Visualization Tools", "📊")
    results = test_visualization_tools()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 4: Jupyter Components
    # =========================================================================
    print_section("Jupyter Components", "📓")
    results = test_jupyter_components()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 5: Development Tools
    # =========================================================================
    print_section("Development Tools", "🔧")
    results = test_development_tools()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 6: Environment Configuration
    # =========================================================================
    print_section("Environment Configuration", "⚙️")
    results = test_environment_config()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 7: Visual Foundations Library
    # =========================================================================
    print_section("Visual Foundations Library", "🎨")
    results = test_visual_foundations()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # TEST 8: Functional Tests
    # =========================================================================
    print_section("Functional Tests", "🧪")
    
    results = test_numpy_operations()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    results = test_matplotlib_plotting()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    results = test_astropy_units()
    for r in results:
        all_results.add(r)
    print_results(results)
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 60)
    print(Colors.header("📋 TEST SUMMARY"))
    print("=" * 60)
    
    # Calculate success rate
    passed = all_results.passed
    failed = all_results.failed
    warnings = all_results.warnings
    total = all_results.total
    
    # Status line
    if failed == 0:
        status_icon = Colors.success("✓")
        status_text = Colors.success("ALL CRITICAL TESTS PASSED")
    else:
        status_icon = Colors.error("✗")
        status_text = Colors.error(f"{failed} CRITICAL TEST(S) FAILED")
    
    print(f"\n  {status_icon} {status_text}")
    print(f"\n  {Colors.success('Passed:')}  {passed}")
    print(f"  {Colors.error('Failed:')}  {failed}")
    print(f"  {Colors.warning('Warnings:')} {warnings}")
    print(f"  {Colors.info('Total:')}   {total}")
    print(f"\n  Duration: {all_results.duration:.2f} seconds")
    
    # Success rate bar
    rate = all_results.success_rate
    bar_length = 30
    filled = int(bar_length * rate / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if rate >= 80:
        bar_color = Colors.GREEN
    elif rate >= 60:
        bar_color = Colors.YELLOW
    else:
        bar_color = Colors.RED
    
    print(f"\n  Success Rate: {bar_color}{bar}{Colors.RESET} {rate:.0f}%")
    
    # =========================================================================
    # RECOMMENDATIONS
    # =========================================================================
    print("\n" + "-" * 60)
    
    if failed == 0 and warnings == 0:
        print(Colors.success("\n🎉 Excellent! Your environment is fully configured."))
        print("\n💡 Next steps:")
        print("   • Run the foundation dashboard:")
        print("     python foundation_dashboard.py")
        print("   • Start JupyterLab for interactive work:")
        print("     jupyter lab")
        print("   • Explore sample visualizations:")
        print("     python visual_foundations.py")
    elif failed == 0:
        print(Colors.success("\n✓ Core environment is ready to use."))
        print(Colors.warning(f"\n⚠️  {warnings} optional component(s) not installed."))
        print("\n   Install them for full functionality, or continue without.")
    else:
        print(Colors.error("\n⚠️  Some critical components are missing."))
        print("\n   Install missing packages with:")
        print("   pip install numpy scipy matplotlib pandas astropy plotly seaborn")
    
    print("\n" + "=" * 60)
    
    # =========================================================================
    # VISUAL TEST
    # =========================================================================
    if visual and failed == 0:
        print(Colors.info("\n🎨 Running visual test..."))
        try:
            success = run_visual_test(show_plot=True)
            if success:
                print(Colors.success("✓ Visual test completed successfully!"))
        except Exception as e:
            print(Colors.warning(f"Visual test skipped: {e}"))
    
    print(Colors.info("\n🔭 Foundation test complete!\n"))
    
    # Return exit code
    return 0 if failed == 0 else 1


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test the Astronomy Starter Kit environment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_foundation.py              # Run all tests with visual
  python test_foundation.py --no-visual  # Skip visual test
  python test_foundation.py --quiet      # Minimal output
        """
    )
    
    parser.add_argument(
        '--no-visual', '-n',
        action='store_true',
        help='Skip the visual test plot'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (only show summary)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Astronomy Foundation Test v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Run tests
    exit_code = run_all_tests(
        visual=not args.no_visual,
        verbose=not args.quiet
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
