#!/usr/bin/env python3
"""
Visual Foundations for Astronomy
================================
A library of accessible visualization tools for learning astronomy with Python.

This module provides visual learning tools optimized for:
- Large, readable text (16-20pt fonts)
- High-contrast dark themes
- Color-blind friendly palettes
- Interactive hover tooltips
- Clear labels and annotations

Part of the Astronomy Starter Kit
https://github.com/RedChaosWolf92/astronomy-starter-kit

Author: Greg (RedChaosWolf92)
License: MIT
"""

import numpy as np
import warnings

# =============================================================================
# VISUAL PREFERENCES SETUP
# =============================================================================
# These settings are applied when the module is imported to ensure
# all plots have good visual accessibility by default.

try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    
    # Dark background for better contrast (easier on eyes, better for presentations)
    plt.style.use('dark_background')
    
    # Large figure size for visibility
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # Large fonts for accessibility
    plt.rcParams['font.size'] = 16
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 14
    
    # Better line widths
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['axes.linewidth'] = 1.5
    
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    warnings.warn("matplotlib not available. Static plots disabled.")

try:
    import seaborn as sns
    # Colorful, distinct colors that work well for color-blind users
    sns.set_palette("husl")
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    warnings.warn("seaborn not available. Some styling features disabled.")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    warnings.warn("plotly not available. Interactive plots disabled.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


# =============================================================================
# COLOR-BLIND FRIENDLY PALETTES
# =============================================================================

# Primary accessible color scheme
# These colors are distinguishable for most forms of color blindness
ACCESSIBLE_COLORS = {
    'primary': '#3498DB',      # Blue - main data
    'secondary': '#E74C3C',    # Red - secondary data/highlights
    'success': '#2ECC71',      # Green - positive indicators
    'warning': '#F39C12',      # Orange - warnings/attention
    'info': '#9B59B6',         # Purple - information
    'light': '#ECF0F1',        # Light gray - backgrounds/grids
    'dark': '#34495E',         # Dark gray - text/borders
    'cyan': '#1ABC9C',         # Teal/cyan - alternative
}

# Wong color palette - optimized for color-blind accessibility
# Reference: Wong, B. (2011). Nature Methods 8, 441
WONG_PALETTE = [
    '#000000',  # Black
    '#E69F00',  # Orange
    '#56B4E9',  # Sky blue
    '#009E73',  # Bluish green
    '#F0E442',  # Yellow
    '#0072B2',  # Blue
    '#D55E00',  # Vermillion
    '#CC79A7',  # Reddish purple
]


# =============================================================================
# VISUAL FOUNDATIONS CLASS
# =============================================================================

class VisualFoundations:
    """
    Foundation class for accessible visual astronomy development.
    
    This class provides methods for creating clear, accessible visualizations
    optimized for visual learners and users who benefit from high-contrast,
    large-text displays.
    
    Features:
    ---------
    - Accessible color schemes (color-blind friendly)
    - Large fonts (16-20pt) for readability
    - Dark themes for better contrast
    - Interactive hover tooltips
    - Multiple plot types (line, scatter, bar)
    - Comparison layouts for multiple datasets
    
    Example:
    --------
    >>> from visual_foundations import VisualFoundations
    >>> vf = VisualFoundations()
    >>> x, y, title = vf.create_sample_data('spectrum')
    >>> fig = vf.interactive_plot(x, y, title)
    >>> fig.show()
    """
    
    def __init__(self, color_scheme='accessible'):
        """
        Initialize VisualFoundations with an accessible color scheme.
        
        Parameters:
        -----------
        color_scheme : str
            Color scheme to use: 'accessible' (default) or 'wong'
        """
        if color_scheme == 'wong':
            self.colors = {
                'primary': WONG_PALETTE[5],    # Blue
                'secondary': WONG_PALETTE[6],  # Vermillion
                'success': WONG_PALETTE[3],    # Bluish green
                'warning': WONG_PALETTE[1],    # Orange
                'info': WONG_PALETTE[7],       # Reddish purple
                'light': '#ECF0F1',
                'dark': '#34495E',
                'cyan': WONG_PALETTE[2],       # Sky blue
            }
            self.palette = WONG_PALETTE
        else:
            self.colors = ACCESSIBLE_COLORS.copy()
            self.palette = list(ACCESSIBLE_COLORS.values())
        
        # Background colors for dark theme
        self.bg_colors = {
            'figure': '#34495E',
            'axes': '#2C3E50',
            'grid': '#4A6278',
        }
    
    # =========================================================================
    # SAMPLE DATA GENERATION
    # =========================================================================
    
    def create_sample_data(self, data_type='sine', n_points=100, noise_level=0.1):
        """
        Generate sample astronomical data for testing and learning.
        
        This method creates realistic-looking sample data that mimics
        common astronomical measurements, useful for learning visualization
        techniques without needing real data.
        
        Parameters:
        -----------
        data_type : str
            Type of data to generate:
            - 'sine': Simple sine wave (periodic signals)
            - 'exponential': Exponential decay (radioactive decay, cooling)
            - 'spectrum': Astronomical spectrum with absorption lines
            - 'lightcurve': Stellar brightness variations over time
            - 'random' or 'linear': Linear trend with noise
            
        n_points : int
            Number of data points to generate (default: 100)
            
        noise_level : float
            Amount of random noise to add (default: 0.1)
            
        Returns:
        --------
        x : numpy.ndarray
            X-axis values (typically time or wavelength)
        y : numpy.ndarray
            Y-axis values (the measured quantity)
        title : str
            Descriptive title for the data type
            
        Example:
        --------
        >>> vf = VisualFoundations()
        >>> x, y, title = vf.create_sample_data('spectrum', n_points=200)
        >>> print(f"Generated {len(x)} points of {title}")
        Generated 200 points of Sample Astronomical Spectrum
        """
        x = np.linspace(0, 10, n_points)
        
        if data_type == 'sine':
            # Simple periodic signal - common in variable stars, pulsars
            y = np.sin(x) + noise_level * np.random.random(n_points)
            title = "Sample Sine Wave Data"
            
        elif data_type == 'exponential':
            # Exponential decay - radioactive decay, cooling curves
            y = np.exp(-x / 3) + noise_level * 0.5 * np.random.random(n_points)
            title = "Sample Exponential Decay"
            
        elif data_type == 'spectrum':
            # Simulated astronomical spectrum with absorption lines
            # Base continuum with slight slope and noise
            y = 1 + 0.1 * np.sin(5 * x) + noise_level * 0.5 * np.random.random(n_points)
            
            # Add Gaussian absorption features (like spectral lines)
            absorption_centers = [2.5, 5.0, 7.5]
            absorption_depths = [0.25, 0.15, 0.20]
            absorption_widths = [0.1, 0.15, 0.12]
            
            for center, depth, width in zip(absorption_centers, 
                                            absorption_depths, 
                                            absorption_widths):
                y -= depth * np.exp(-(x - center)**2 / width)
            
            title = "Sample Astronomical Spectrum"
            
        elif data_type == 'lightcurve':
            # Stellar brightness variations over time
            # Combines: slow trend + periodic variation + noise
            trend = -0.01 * x  # Slight dimming trend
            periodic = 0.05 * np.sin(2 * np.pi * x / 2.5)  # Periodic variation
            noise = noise_level * 0.2 * np.random.random(n_points)
            y = 1 + trend + periodic + noise
            title = "Sample Light Curve"
            
        elif data_type == 'transit':
            # Exoplanet transit light curve
            y = np.ones(n_points)
            # Add transit dip
            transit_center = 5.0
            transit_duration = 1.5
            transit_depth = 0.02
            in_transit = np.abs(x - transit_center) < transit_duration / 2
            y[in_transit] -= transit_depth
            # Add ingress/egress
            ingress = (x > transit_center - transit_duration/2 - 0.2) & \
                      (x < transit_center - transit_duration/2 + 0.2)
            egress = (x > transit_center + transit_duration/2 - 0.2) & \
                     (x < transit_center + transit_duration/2 + 0.2)
            y[ingress] -= transit_depth * 0.5
            y[egress] -= transit_depth * 0.5
            # Add noise
            y += noise_level * 0.1 * np.random.random(n_points)
            title = "Sample Exoplanet Transit"
            
        elif data_type == 'blackbody':
            # Blackbody radiation curve (simplified)
            # x represents wavelength in arbitrary units
            T = 5778  # Solar temperature
            # Planck-like function (simplified)
            y = (x ** -5) / (np.exp(1.0 / (x + 0.1)) - 1)
            y = y / np.max(y)  # Normalize
            y += noise_level * 0.05 * np.random.random(n_points)
            title = "Sample Blackbody Spectrum"
            
        else:  # 'random' or 'linear'
            # Simple linear trend with scatter
            y = 0.5 * x + noise_level * np.random.random(n_points)
            title = "Sample Linear Data"
            
        return x, y, title
    
    # =========================================================================
    # STATIC MATPLOTLIB PLOTS
    # =========================================================================
    
    def foundation_plot(self, x, y, title="Data Visualization",
                        xlabel="X Values", ylabel="Y Values",
                        style='line', color=None, annotate_peaks=False,
                        save_path=None, show=True):
        """
        Create accessible matplotlib plots with good visual defaults.
        
        This method creates static plots with large fonts, high contrast,
        and clear labeling for maximum readability.
        
        Parameters:
        -----------
        x, y : array-like
            Data to plot
            
        title : str
            Plot title (displayed in large, bold text)
            
        xlabel, ylabel : str
            Axis labels (displayed in bold text)
            
        style : str
            Plot style: 'line', 'scatter', or 'bar'
            
        color : str, optional
            Color for the plot. Uses primary color if None.
            
        annotate_peaks : bool
            If True, annotate local maxima with labels.
            Requires scipy for peak detection.
            
        save_path : str, optional
            If provided, save the figure to this path.
            
        show : bool
            If True (default), display the plot.
            
        Returns:
        --------
        fig : matplotlib.figure.Figure
            The figure object
        ax : matplotlib.axes.Axes
            The axes object
            
        Example:
        --------
        >>> vf = VisualFoundations()
        >>> x, y, title = vf.create_sample_data('spectrum')
        >>> fig, ax = vf.foundation_plot(x, y, title,
        ...                              xlabel="Wavelength (μm)",
        ...                              ylabel="Relative Flux")
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("matplotlib is required for static plots. "
                            "Install with: pip install matplotlib")
        
        if color is None:
            color = self.colors['primary']
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Create plot based on style
        if style == 'line':
            ax.plot(x, y, color=color, linewidth=3, marker='o',
                    markersize=6, markerfacecolor='white',
                    markeredgecolor=color, markeredgewidth=2,
                    label='Data')
        elif style == 'scatter':
            ax.scatter(x, y, color=color, alpha=0.8, s=120,
                       edgecolors='white', linewidth=1.5,
                       label='Data')
        elif style == 'bar':
            ax.bar(x, y, color=color, alpha=0.8,
                   edgecolor='white', linewidth=1.5,
                   label='Data')
        else:
            raise ValueError(f"Unknown style: {style}. Use 'line', 'scatter', or 'bar'")
        
        # Enhanced styling for accessibility
        ax.set_title(title, fontsize=22, fontweight='bold', pad=25)
        ax.set_xlabel(xlabel, fontsize=18, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=18, fontweight='bold')
        ax.grid(True, alpha=0.4, linewidth=1.5, color=self.bg_colors['grid'])
        
        # Dark background for better contrast
        ax.set_facecolor(self.bg_colors['axes'])
        fig.patch.set_facecolor(self.bg_colors['figure'])
        
        # Annotate peaks if requested
        if annotate_peaks:
            self._annotate_peaks(ax, x, y)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches='tight',
                        facecolor=fig.get_facecolor(), edgecolor='none')
            print(f"✓ Figure saved to: {save_path}")
        
        # Show if requested
        if show:
            plt.show()
        
        return fig, ax
    
    def _annotate_peaks(self, ax, x, y, min_height_percentile=75):
        """
        Annotate local maxima on a plot.
        
        Parameters:
        -----------
        ax : matplotlib.axes.Axes
            The axes to annotate
        x, y : array-like
            The data
        min_height_percentile : float
            Only annotate peaks above this percentile
        """
        try:
            from scipy.signal import find_peaks
            
            min_height = np.percentile(y, min_height_percentile)
            peaks, properties = find_peaks(y, height=min_height)
            
            for peak in peaks[:5]:  # Limit to 5 peaks
                ax.annotate(
                    f'Peak: {y[peak]:.2f}',
                    (x[peak], y[peak]),
                    xytext=(0, 25),
                    textcoords='offset points',
                    ha='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5',
                              facecolor='#F39C12', alpha=0.9,
                              edgecolor='white', linewidth=2),
                    arrowprops=dict(arrowstyle='->',
                                    connectionstyle='arc3,rad=0',
                                    color='white', linewidth=2)
                )
        except ImportError:
            warnings.warn("scipy is required for peak annotation. "
                         "Install with: pip install scipy")
    
    # =========================================================================
    # INTERACTIVE PLOTLY PLOTS
    # =========================================================================
    
    def interactive_plot(self, x, y, title="Interactive Data",
                         xlabel="X Values", ylabel="Y Values",
                         color=None, save_html=None, show=True):
        """
        Create interactive plotly visualization with hover tooltips.
        
        Interactive plots allow you to:
        - Hover over points to see exact values
        - Zoom and pan to explore data
        - Save as PNG directly from the plot
        
        Parameters:
        -----------
        x, y : array-like
            Data to plot
            
        title : str
            Plot title
            
        xlabel, ylabel : str
            Axis labels
            
        color : str, optional
            Line/marker color. Uses primary color if None.
            
        save_html : str, optional
            If provided, save the interactive plot as HTML file.
            
        show : bool
            If True (default), display the plot.
            
        Returns:
        --------
        fig : plotly.graph_objects.Figure
            The interactive figure object
            
        Example:
        --------
        >>> vf = VisualFoundations()
        >>> x, y, title = vf.create_sample_data('lightcurve')
        >>> fig = vf.interactive_plot(x, y, title,
        ...                           xlabel="Time (days)",
        ...                           ylabel="Relative Brightness")
        >>> fig.show()
        """
        if not PLOTLY_AVAILABLE:
            raise ImportError("plotly is required for interactive plots. "
                            "Install with: pip install plotly")
        
        if color is None:
            color = self.colors['primary']
        
        fig = go.Figure()
        
        # Add main trace with hover information
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines+markers',
            name='Data',
            hovertemplate=(
                '<b>X:</b> %{x:.4f}<br>'
                '<b>Y:</b> %{y:.4f}<br>'
                '<extra></extra>'
            ),
            line=dict(width=3, color=color),
            marker=dict(
                size=8,
                color='white',
                line=dict(width=2, color=color)
            )
        ))
        
        # Update layout for accessibility
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                font=dict(size=24),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title=dict(text=xlabel, font=dict(size=18)),
            yaxis_title=dict(text=ylabel, font=dict(size=18)),
            hovermode='closest',
            template='plotly_dark',
            height=600,
            font=dict(size=16),
            # Add good margins for readability
            margin=dict(l=80, r=40, t=80, b=60),
            # Legend styling
            legend=dict(
                font=dict(size=14),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='white',
                borderwidth=1
            )
        )
        
        # Make axis labels bold
        fig.update_xaxes(
            title_font=dict(size=18),
            tickfont=dict(size=14),
            gridcolor='rgba(255,255,255,0.2)',
            gridwidth=1
        )
        fig.update_yaxes(
            title_font=dict(size=18),
            tickfont=dict(size=14),
            gridcolor='rgba(255,255,255,0.2)',
            gridwidth=1
        )
        
        # Save if path provided
        if save_html:
            fig.write_html(save_html)
            print(f"✓ Interactive plot saved to: {save_html}")
        
        # Show if requested
        if show:
            fig.show()
        
        return fig
    
    # =========================================================================
    # COMPARISON PLOTS
    # =========================================================================
    
    def comparison_plot(self, datasets, labels, title="Data Comparison",
                        save_html=None, show=True):
        """
        Compare multiple datasets visually in a 2x2 subplot grid.
        
        Useful for comparing different data types, observations,
        or analysis results side by side.
        
        Parameters:
        -----------
        datasets : list of tuples
            Each tuple contains (x, y) data arrays.
            Maximum of 4 datasets will be displayed.
            
        labels : list of str
            Label for each dataset (used as subplot titles)
            
        title : str
            Overall plot title
            
        save_html : str, optional
            If provided, save as interactive HTML file.
            
        show : bool
            If True (default), display the plot.
            
        Returns:
        --------
        fig : plotly.graph_objects.Figure
            The interactive comparison figure
            
        Example:
        --------
        >>> vf = VisualFoundations()
        >>> data = vf.learning_dashboard_data()
        >>> datasets = [data['sine_wave'], data['spectrum']]
        >>> labels = ['Sine Wave', 'Spectrum']
        >>> fig = vf.comparison_plot(datasets, labels, "Data Comparison")
        """
        if not PLOTLY_AVAILABLE:
            raise ImportError("plotly is required for comparison plots. "
                            "Install with: pip install plotly")
        
        n_datasets = min(len(datasets), 4)  # Maximum 4 subplots
        
        # Create 2x2 subplot grid
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f"<b>{label}</b>" for label in labels[:n_datasets]],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Colors for each subplot
        subplot_colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['success'],
            self.colors['warning']
        ]
        
        # Subplot positions
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        # Add each dataset
        for i, (dataset, label) in enumerate(zip(datasets[:n_datasets],
                                                  labels[:n_datasets])):
            x, y = dataset
            row, col = positions[i]
            
            fig.add_trace(
                go.Scatter(
                    x=x, y=y,
                    mode='lines+markers',
                    name=label,
                    line=dict(color=subplot_colors[i], width=2),
                    marker=dict(size=5),
                    hovertemplate='X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Update layout
        fig.update_layout(
            title_text=f"<b>{title}</b>",
            title_font_size=24,
            title_x=0.5,
            template='plotly_dark',
            height=700,
            showlegend=True,
            font=dict(size=14),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.15,
                xanchor='center',
                x=0.5,
                font=dict(size=12)
            )
        )
        
        # Update all axes
        fig.update_xaxes(
            gridcolor='rgba(255,255,255,0.2)',
            tickfont=dict(size=12)
        )
        fig.update_yaxes(
            gridcolor='rgba(255,255,255,0.2)',
            tickfont=dict(size=12)
        )
        
        # Save if path provided
        if save_html:
            fig.write_html(save_html)
            print(f"✓ Comparison plot saved to: {save_html}")
        
        # Show if requested
        if show:
            fig.show()
        
        return fig
    
    # =========================================================================
    # LEARNING DASHBOARD DATA
    # =========================================================================
    
    def learning_dashboard_data(self, n_points=75):
        """
        Generate a collection of sample datasets for interactive learning.
        
        Returns a dictionary of pre-generated datasets that can be used
        for learning visualization techniques, testing plots, or
        demonstrating different data patterns.
        
        Parameters:
        -----------
        n_points : int
            Number of points per dataset (default: 75)
            
        Returns:
        --------
        dict : Dictionary containing sample datasets with keys:
            - 'sine_wave': Periodic oscillation data
            - 'exponential': Decay curve data
            - 'spectrum': Absorption spectrum data
            - 'lightcurve': Brightness variation data
            - 'transit': Exoplanet transit data
            - 'blackbody': Thermal emission data
            
            Each value is a tuple of (x_array, y_array)
            
        Example:
        --------
        >>> vf = VisualFoundations()
        >>> data = vf.learning_dashboard_data()
        >>> x, y = data['spectrum']
        >>> print(f"Spectrum data: {len(x)} points")
        """
        datasets = {}
        
        data_types = ['sine', 'exponential', 'spectrum', 
                      'lightcurve', 'transit', 'blackbody']
        
        for dtype in data_types:
            x, y, _ = self.create_sample_data(dtype, n_points)
            # Convert data_type name to friendly key
            key = dtype if dtype != 'sine' else 'sine_wave'
            datasets[key] = (x, y)
        
        return datasets
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def get_color(self, name):
        """
        Get a color from the accessible color scheme.
        
        Parameters:
        -----------
        name : str
            Color name: 'primary', 'secondary', 'success', 
            'warning', 'info', 'light', 'dark', 'cyan'
            
        Returns:
        --------
        str : Hex color code
        """
        return self.colors.get(name, self.colors['primary'])
    
    def list_colors(self):
        """
        Display all available colors in the scheme.
        
        Returns:
        --------
        dict : Dictionary of color names and hex codes
        """
        print("Available Colors:")
        print("-" * 30)
        for name, hex_code in self.colors.items():
            print(f"  {name:12} : {hex_code}")
        return self.colors.copy()
    
    def list_data_types(self):
        """
        Display all available sample data types.
        
        Returns:
        --------
        list : List of data type names
        """
        types = ['sine', 'exponential', 'spectrum', 'lightcurve', 
                 'transit', 'blackbody', 'linear']
        print("Available Data Types:")
        print("-" * 50)
        descriptions = {
            'sine': 'Periodic oscillation (variable stars, pulsars)',
            'exponential': 'Exponential decay (cooling, radioactive)',
            'spectrum': 'Absorption spectrum with spectral lines',
            'lightcurve': 'Stellar brightness over time',
            'transit': 'Exoplanet transit light curve',
            'blackbody': 'Thermal emission curve',
            'linear': 'Linear trend with noise'
        }
        for dtype in types:
            print(f"  {dtype:12} : {descriptions[dtype]}")
        return types


# =============================================================================
# TEST FUNCTION
# =============================================================================

def test_visual_foundations():
    """
    Test the Visual Foundations setup and demonstrate all features.
    
    This function runs a series of tests to verify that all visualization
    capabilities are working correctly. It's useful for:
    - Verifying your installation is complete
    - Seeing examples of all plot types
    - Testing after updates or changes
    
    Run from command line:
        python visual_foundations.py
    
    Or import and call:
        from visual_foundations import test_visual_foundations
        test_visual_foundations()
    """
    import os
    
    print("\n" + "=" * 70)
    print("🎨 VISUAL FOUNDATIONS TEST SUITE")
    print("=" * 70)
    print("\nTesting visual capabilities for astronomy learning...")
    print("Target: Large fonts, high contrast, accessible colors\n")
    
    # Create instance
    vf = VisualFoundations()
    
    # Results tracking
    passed = 0
    failed = 0
    
    # -------------------------------------------------------------------------
    # Test 1: Sample data generation
    # -------------------------------------------------------------------------
    print("[1/5] Testing sample data generation...")
    try:
        data_types = ['sine', 'exponential', 'spectrum', 'lightcurve', 
                      'transit', 'blackbody']
        for dtype in data_types:
            x, y, title = vf.create_sample_data(dtype, 50)
            assert len(x) == 50, f"Expected 50 points, got {len(x)}"
            assert len(y) == 50, f"Expected 50 points, got {len(y)}"
            print(f"    ✓ Generated {dtype}: {len(x)} points")
        print("  ✓ Sample data generation: PASSED")
        passed += 1
    except Exception as e:
        print(f"  ✗ Sample data generation: FAILED - {e}")
        failed += 1
    
    # -------------------------------------------------------------------------
    # Test 2: Static matplotlib plotting
    # -------------------------------------------------------------------------
    print("\n[2/5] Testing static matplotlib plots...")
    if MATPLOTLIB_AVAILABLE:
        try:
            x, y, title = vf.create_sample_data('spectrum', 100)
            fig, ax = vf.foundation_plot(
                x, y, title,
                xlabel="Wavelength (μm)",
                ylabel="Relative Intensity",
                style='line',
                show=False  # Don't display during test
            )
            # Test saving
            test_path = '/tmp/test_visual_foundations_static.png'
            fig.savefig(test_path, dpi=100)
            assert os.path.exists(test_path), "File not saved"
            plt.close(fig)
            print(f"    ✓ Static plot created and saved")
            print("  ✓ Static matplotlib plotting: PASSED")
            passed += 1
        except Exception as e:
            print(f"  ✗ Static matplotlib plotting: FAILED - {e}")
            failed += 1
    else:
        print("  ⊘ Static matplotlib plotting: SKIPPED (matplotlib not installed)")
    
    # -------------------------------------------------------------------------
    # Test 3: Interactive plotly plotting
    # -------------------------------------------------------------------------
    print("\n[3/5] Testing interactive plotly plots...")
    if PLOTLY_AVAILABLE:
        try:
            x, y, title = vf.create_sample_data('lightcurve', 75)
            fig = vf.interactive_plot(
                x, y, "Interactive Light Curve",
                xlabel="Time (days)",
                ylabel="Brightness",
                show=False  # Don't display during test
            )
            # Test saving
            test_path = '/tmp/test_visual_foundations_interactive.html'
            fig.write_html(test_path)
            assert os.path.exists(test_path), "File not saved"
            print(f"    ✓ Interactive plot created and saved as HTML")
            print("  ✓ Interactive plotly plotting: PASSED")
            passed += 1
        except Exception as e:
            print(f"  ✗ Interactive plotly plotting: FAILED - {e}")
            failed += 1
    else:
        print("  ⊘ Interactive plotly plotting: SKIPPED (plotly not installed)")
    
    # -------------------------------------------------------------------------
    # Test 4: Comparison plots
    # -------------------------------------------------------------------------
    print("\n[4/5] Testing comparison plots...")
    if PLOTLY_AVAILABLE:
        try:
            data_dict = vf.learning_dashboard_data(n_points=50)
            datasets = [
                data_dict['sine_wave'],
                data_dict['exponential'],
                data_dict['spectrum'],
                data_dict['lightcurve']
            ]
            labels = ['Sine Wave', 'Exponential Decay', 'Spectrum', 'Light Curve']
            
            fig = vf.comparison_plot(
                datasets, labels,
                "Foundation Data Types Comparison",
                show=False
            )
            # Test saving
            test_path = '/tmp/test_visual_foundations_comparison.html'
            fig.write_html(test_path)
            assert os.path.exists(test_path), "File not saved"
            print(f"    ✓ Comparison plot created with 4 subplots")
            print("  ✓ Comparison plotting: PASSED")
            passed += 1
        except Exception as e:
            print(f"  ✗ Comparison plotting: FAILED - {e}")
            failed += 1
    else:
        print("  ⊘ Comparison plotting: SKIPPED (plotly not installed)")
    
    # -------------------------------------------------------------------------
    # Test 5: Color scheme and utilities
    # -------------------------------------------------------------------------
    print("\n[5/5] Testing color schemes and utilities...")
    try:
        # Test color retrieval
        primary = vf.get_color('primary')
        assert primary.startswith('#'), "Color should be hex code"
        
        # Test Wong palette
        vf_wong = VisualFoundations(color_scheme='wong')
        assert len(vf_wong.palette) == 8, "Wong palette should have 8 colors"
        
        # Test learning dashboard data
        data = vf.learning_dashboard_data()
        assert 'sine_wave' in data, "Missing sine_wave data"
        assert 'spectrum' in data, "Missing spectrum data"
        
        print(f"    ✓ Color scheme: {len(vf.colors)} accessible colors")
        print(f"    ✓ Wong palette: {len(vf_wong.palette)} color-blind safe colors")
        print(f"    ✓ Dashboard data: {len(data)} dataset types")
        print("  ✓ Color schemes and utilities: PASSED")
        passed += 1
    except Exception as e:
        print(f"  ✗ Color schemes and utilities: FAILED - {e}")
        failed += 1
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("🎨 VISUAL FOUNDATIONS TEST COMPLETE")
    print("=" * 70)
    
    total = passed + failed
    print(f"\n  Results: {passed}/{total} tests passed")
    
    if failed == 0:
        print("\n✅ All tests passed! Visual Foundations is ready to use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check error messages above.")
    
    print("\n" + "-" * 70)
    print("VISUAL ACCESSIBILITY FEATURES:")
    print("-" * 70)
    print("  • Large, readable fonts (16-20pt)")
    print("  • High-contrast dark theme")
    print("  • Interactive hover tooltips")
    print("  • Color-blind friendly palettes")
    print("  • Multiple plot styles (line, scatter, bar)")
    print("  • Comparison layouts for multiple datasets")
    
    print("\n" + "-" * 70)
    print("QUICK START USAGE:")
    print("-" * 70)
    print("""
  from visual_foundations import VisualFoundations
  
  vf = VisualFoundations()
  
  # Generate sample data
  x, y, title = vf.create_sample_data('spectrum')
  
  # Create static plot
  fig, ax = vf.foundation_plot(x, y, title)
  
  # Create interactive plot
  fig = vf.interactive_plot(x, y, title)
  fig.show()
  
  # Compare multiple datasets
  data = vf.learning_dashboard_data()
  datasets = [data['sine_wave'], data['spectrum']]
  labels = ['Sine Wave', 'Spectrum']
  vf.comparison_plot(datasets, labels)
""")
    
    print("🎯 Visual Foundations test complete!\n")
    
    return passed, failed


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    test_visual_foundations()