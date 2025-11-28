#!/usr/bin/env python3
"""
Foundation Dashboard for Astronomy Learning
============================================
An interactive web dashboard for visual astronomy learning and data exploration.

This dashboard provides:
- Real-time data visualization with adjustable parameters
- Multiple astronomical data types to explore
- Statistical analysis with explanations
- Educational descriptions for learning

Part of the Astronomy Starter Kit
https://github.com/RedChaosWolf92/astronomy-starter-kit

Author: Greg (RedChaosWolf92)
License: MIT

Usage:
------
    python foundation_dashboard.py
    
Then open your browser to: http://localhost:8050

Dependencies:
-------------
    pip install dash plotly numpy pandas
"""

import numpy as np
import warnings

# Check for required dependencies
try:
    import dash
    from dash import dcc, html, Input, Output
    import plotly.graph_objects as go
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False
    warnings.warn("dash not available. Install with: pip install dash")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Try to import VisualFoundations for consistent styling
try:
    from visual_foundations import VisualFoundations, ACCESSIBLE_COLORS
    VF_AVAILABLE = True
except ImportError:
    VF_AVAILABLE = False
    # Define fallback colors if visual_foundations not available
    ACCESSIBLE_COLORS = {
        'primary': '#3498DB',
        'secondary': '#E74C3C',
        'success': '#2ECC71',
        'warning': '#F39C12',
        'info': '#9B59B6',
        'light': '#ECF0F1',
        'dark': '#34495E',
        'cyan': '#1ABC9C',
    }


# =============================================================================
# DASHBOARD STYLING
# =============================================================================

# Dark theme colors for accessibility
DASHBOARD_STYLES = {
    'background': '#1a1a2e',
    'card_bg': '#16213e',
    'accent': '#0f3460',
    'text': '#FFFFFF',
    'text_muted': '#B0B0B0',
    'border': '#3498DB',
}

# Common style dictionaries
HEADER_STYLE = {
    'textAlign': 'center',
    'color': DASHBOARD_STYLES['text'],
    'marginBottom': '10px',
    'fontSize': '36px',
    'fontWeight': 'bold',
    'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
}

SUBHEADER_STYLE = {
    'textAlign': 'center',
    'color': DASHBOARD_STYLES['text_muted'],
    'marginBottom': '30px',
    'fontSize': '18px',
}

LABEL_STYLE = {
    'color': DASHBOARD_STYLES['text'],
    'fontSize': '18px',
    'fontWeight': 'bold',
    'marginBottom': '10px',
    'display': 'block',
}

CARD_STYLE = {
    'backgroundColor': DASHBOARD_STYLES['card_bg'],
    'padding': '20px',
    'borderRadius': '12px',
    'border': f"2px solid {DASHBOARD_STYLES['accent']}",
    'marginBottom': '20px',
}

INFO_PANEL_STYLE = {
    'backgroundColor': 'rgba(52, 152, 219, 0.15)',
    'padding': '25px',
    'borderRadius': '12px',
    'border': f"2px solid {ACCESSIBLE_COLORS['primary']}",
    'marginTop': '20px',
}


# =============================================================================
# DATA TYPE DESCRIPTIONS (Educational Content)
# =============================================================================

DATA_TYPE_INFO = {
    'sine': {
        'icon': '📈',
        'title': 'Sine Wave',
        'description': (
            'A periodic oscillating function fundamental to physics and astronomy. '
            'Sine waves appear in light waves, sound waves, and the motion of '
            'orbiting objects. Variable stars often show sinusoidal brightness changes.'
        ),
        'astronomy_context': (
            'Pulsating variable stars like Cepheids show periodic brightness '
            'variations that can be modeled with sine functions. These are used '
            'as "standard candles" to measure cosmic distances.'
        ),
        'xlabel': 'Phase / Time',
        'ylabel': 'Amplitude',
    },
    'exponential': {
        'icon': '📉',
        'title': 'Exponential Decay',
        'description': (
            'A function that decreases rapidly at first, then more slowly over time. '
            'This pattern appears in radioactive decay, thermal cooling, and the '
            'fading of transient astronomical events.'
        ),
        'astronomy_context': (
            'Supernova light curves often show exponential decay as radioactive '
            'elements (like Nickel-56) power the fading glow. The decay rate '
            'helps astronomers understand the explosion physics.'
        ),
        'xlabel': 'Time',
        'ylabel': 'Intensity',
    },
    'spectrum': {
        'icon': '🌟',
        'title': 'Astronomical Spectrum',
        'description': (
            'A representation of light intensity across different wavelengths. '
            'The dips (absorption lines) reveal which chemical elements are '
            'present in a star or planet atmosphere.'
        ),
        'astronomy_context': (
            'Spectroscopy is how we determine stellar composition, temperature, '
            'and motion. The absorption features in this simulation are similar '
            'to hydrogen or metal lines in real stellar spectra.'
        ),
        'xlabel': 'Wavelength (arbitrary units)',
        'ylabel': 'Relative Flux',
    },
    'lightcurve': {
        'icon': '💫',
        'title': 'Stellar Light Curve',
        'description': (
            'A plot of brightness over time, showing how a star\'s light output '
            'changes. Combines long-term trends with periodic variations, '
            'similar to real stellar observations.'
        ),
        'astronomy_context': (
            'Light curves are essential for detecting exoplanet transits (when '
            'a planet crosses in front of its star) and studying variable stars. '
            'The periodic dips can reveal orbital periods and planet sizes.'
        ),
        'xlabel': 'Time (days)',
        'ylabel': 'Relative Brightness',
    },
    'transit': {
        'icon': '🪐',
        'title': 'Exoplanet Transit',
        'description': (
            'The characteristic dip in starlight when a planet passes in front '
            'of its host star. The depth and duration of the transit reveal '
            'the planet\'s size and orbital properties.'
        ),
        'astronomy_context': (
            'NASA\'s Kepler and TESS missions have discovered thousands of '
            'exoplanets using this transit method. The transit depth is '
            'proportional to (planet radius / star radius)².'
        ),
        'xlabel': 'Time (hours)',
        'ylabel': 'Relative Flux',
    },
    'random': {
        'icon': '📊',
        'title': 'Random Walk',
        'description': (
            'A mathematical process where each step is random. Useful for '
            'understanding noise in data and testing analysis algorithms. '
            'The cumulative sum of random values creates wandering patterns.'
        ),
        'astronomy_context': (
            'Random noise is present in all astronomical observations due to '
            'photon counting statistics, atmospheric effects, and detector '
            'limitations. Understanding noise helps separate real signals.'
        ),
        'xlabel': 'Step Number',
        'ylabel': 'Cumulative Value',
    },
}

# Statistics explanations for educational purposes
STATS_EXPLANATIONS = {
    'mean': (
        'The average value of all data points. In astronomy, this represents '
        'the typical brightness or flux level.'
    ),
    'std': (
        'Standard deviation measures spread from the mean. Higher values '
        'indicate more variability in the data.'
    ),
    'min': (
        'The minimum value in the dataset. For light curves, this might '
        'represent the faintest measurement.'
    ),
    'max': (
        'The maximum value in the dataset. For spectra, this could be '
        'the peak continuum level.'
    ),
    'range': (
        'The difference between maximum and minimum. A larger range '
        'indicates greater variation in the data.'
    ),
}


# =============================================================================
# FOUNDATION DASHBOARD CLASS
# =============================================================================

class FoundationDashboard:
    """
    Interactive web dashboard for visual astronomy learning.
    
    This dashboard provides real-time visualization of different astronomical
    data types with adjustable parameters and educational explanations.
    
    Features:
    ---------
    - Multiple astronomical data types (sine, spectrum, lightcurve, etc.)
    - Adjustable number of points and noise level
    - Real-time plot updates
    - Statistical analysis with explanations
    - Data distribution histogram
    - Dark theme for accessibility
    - Large fonts for readability
    
    Example:
    --------
    >>> dashboard = FoundationDashboard()
    >>> dashboard.run()
    # Opens at http://localhost:8050
    """
    
    def __init__(self):
        """Initialize the dashboard application."""
        if not DASH_AVAILABLE:
            raise ImportError(
                "Dash is required for the dashboard. "
                "Install with: pip install dash plotly"
            )
        
        # Create Dash app with custom styling
        self.app = dash.Dash(
            __name__,
            title="Astronomy Foundation Dashboard",
            update_title="Updating...",
            suppress_callback_exceptions=True,
        )
        
        # Store color scheme
        self.colors = ACCESSIBLE_COLORS
        
        # Setup the dashboard
        self._setup_layout()
        self._setup_callbacks()
    
    def _setup_layout(self):
        """Create the dashboard layout with all components."""
        
        self.app.layout = html.Div([
            # ================================================================
            # HEADER SECTION
            # ================================================================
            html.Div([
                html.H1(
                    "🔭 Astronomy Foundation Dashboard",
                    style=HEADER_STYLE
                ),
                html.P(
                    "Interactive visual learning for astronomical data analysis",
                    style=SUBHEADER_STYLE
                ),
            ], style={'marginBottom': '20px'}),
            
            # ================================================================
            # CONTROLS SECTION
            # ================================================================
            html.Div([
                html.H3(
                    "⚙️ Data Controls",
                    style={
                        'color': DASHBOARD_STYLES['text'],
                        'marginBottom': '20px',
                        'fontSize': '22px',
                    }
                ),
                
                # Control panels in a row
                html.Div([
                    # Data Type Selector
                    html.Div([
                        html.Label("Select Data Type:", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id='data-type',
                            options=[
                                {'label': f"{DATA_TYPE_INFO['sine']['icon']} Sine Wave", 
                                 'value': 'sine'},
                                {'label': f"{DATA_TYPE_INFO['exponential']['icon']} Exponential Decay", 
                                 'value': 'exponential'},
                                {'label': f"{DATA_TYPE_INFO['spectrum']['icon']} Astronomical Spectrum", 
                                 'value': 'spectrum'},
                                {'label': f"{DATA_TYPE_INFO['lightcurve']['icon']} Stellar Light Curve", 
                                 'value': 'lightcurve'},
                                {'label': f"{DATA_TYPE_INFO['transit']['icon']} Exoplanet Transit", 
                                 'value': 'transit'},
                                {'label': f"{DATA_TYPE_INFO['random']['icon']} Random Walk", 
                                 'value': 'random'},
                            ],
                            value='sine',
                            style={
                                'backgroundColor': '#FFFFFF',
                                'color': '#000000',
                                'fontSize': '16px',
                            },
                            clearable=False,
                        ),
                        html.P(
                            "Choose different astronomical data patterns to explore",
                            style={
                                'color': DASHBOARD_STYLES['text_muted'],
                                'fontSize': '14px',
                                'marginTop': '8px',
                            }
                        ),
                    ], style={
                        'width': '32%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '10px',
                    }),
                    
                    # Number of Points Slider
                    html.Div([
                        html.Label("Number of Points:", style=LABEL_STYLE),
                        dcc.Slider(
                            id='n-points',
                            min=20,
                            max=300,
                            step=10,
                            value=100,
                            marks={
                                20: {'label': '20', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                100: {'label': '100', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                200: {'label': '200', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                300: {'label': '300', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                            },
                            tooltip={'placement': 'bottom', 'always_visible': True},
                        ),
                        html.P(
                            "More points = smoother curves, but slower updates",
                            style={
                                'color': DASHBOARD_STYLES['text_muted'],
                                'fontSize': '14px',
                                'marginTop': '8px',
                            }
                        ),
                    ], style={
                        'width': '32%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '10px',
                    }),
                    
                    # Noise Level Slider
                    html.Div([
                        html.Label("Noise Level:", style=LABEL_STYLE),
                        dcc.Slider(
                            id='noise-level',
                            min=0,
                            max=0.5,
                            step=0.05,
                            value=0.1,
                            marks={
                                0: {'label': '0', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                0.1: {'label': '0.1', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                0.25: {'label': '0.25', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                                0.5: {'label': '0.5', 'style': {'color': '#FFFFFF', 'fontSize': '14px'}},
                            },
                            tooltip={'placement': 'bottom', 'always_visible': True},
                        ),
                        html.P(
                            "Simulates measurement uncertainty in real observations",
                            style={
                                'color': DASHBOARD_STYLES['text_muted'],
                                'fontSize': '14px',
                                'marginTop': '8px',
                            }
                        ),
                    ], style={
                        'width': '32%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '10px',
                    }),
                ]),
            ], style=CARD_STYLE),
            
            # ================================================================
            # MAIN VISUALIZATION
            # ================================================================
            html.Div([
                html.H3(
                    "📊 Main Visualization",
                    style={
                        'color': DASHBOARD_STYLES['text'],
                        'marginBottom': '15px',
                        'fontSize': '22px',
                    }
                ),
                dcc.Graph(
                    id='main-plot',
                    style={'height': '500px'},
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'astronomy_plot',
                            'height': 600,
                            'width': 1000,
                            'scale': 2,
                        },
                    },
                ),
            ], style=CARD_STYLE),
            
            # ================================================================
            # STATISTICS AND HISTOGRAM ROW
            # ================================================================
            html.Div([
                # Histogram
                html.Div([
                    html.H3(
                        "📈 Data Distribution",
                        style={
                            'color': DASHBOARD_STYLES['text'],
                            'marginBottom': '15px',
                            'fontSize': '20px',
                        }
                    ),
                    dcc.Graph(
                        id='histogram-plot',
                        style={'height': '350px'},
                        config={'displayModeBar': False},
                    ),
                ], style={
                    **CARD_STYLE,
                    'width': '48%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                }),
                
                # Statistics Display
                html.Div([
                    html.H3(
                        "🔢 Statistics Summary",
                        style={
                            'color': DASHBOARD_STYLES['text'],
                            'marginBottom': '15px',
                            'fontSize': '20px',
                        }
                    ),
                    html.Div(id='statistics-panel'),
                ], style={
                    **CARD_STYLE,
                    'width': '48%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'marginLeft': '2%',
                }),
            ]),
            
            # ================================================================
            # EDUCATIONAL INFORMATION PANEL
            # ================================================================
            html.Div([
                html.H3(
                    "📚 Learn About This Data Type",
                    style={
                        'color': ACCESSIBLE_COLORS['primary'],
                        'marginBottom': '15px',
                        'fontSize': '22px',
                    }
                ),
                html.Div(id='education-panel'),
            ], style=INFO_PANEL_STYLE),
            
            # ================================================================
            # TIPS SECTION
            # ================================================================
            html.Div([
                html.H4(
                    "💡 Data Exploration Tips",
                    style={
                        'color': ACCESSIBLE_COLORS['success'],
                        'marginBottom': '15px',
                        'fontSize': '18px',
                    }
                ),
                html.Ul([
                    html.Li(
                        "Hover over data points to see exact values",
                        style={'marginBottom': '8px'}
                    ),
                    html.Li(
                        "Use the zoom and pan tools to explore details",
                        style={'marginBottom': '8px'}
                    ),
                    html.Li(
                        "Increase noise to see how it affects statistics",
                        style={'marginBottom': '8px'}
                    ),
                    html.Li(
                        "Compare the histogram shape for different data types",
                        style={'marginBottom': '8px'}
                    ),
                    html.Li(
                        "Click the camera icon to save plots as images",
                        style={'marginBottom': '8px'}
                    ),
                ], style={
                    'color': DASHBOARD_STYLES['text'],
                    'fontSize': '16px',
                    'lineHeight': '1.8',
                }),
            ], style={
                **CARD_STYLE,
                'marginTop': '20px',
            }),
            
            # ================================================================
            # FOOTER
            # ================================================================
            html.Div([
                html.Hr(style={'borderColor': DASHBOARD_STYLES['accent']}),
                html.P([
                    "🔭 Astronomy Starter Kit | ",
                    html.A(
                        "GitHub Repository",
                        href="https://github.com/RedChaosWolf92/astronomy-starter-kit",
                        target="_blank",
                        style={'color': ACCESSIBLE_COLORS['primary']},
                    ),
                    " | Built with Dash & Plotly",
                ], style={
                    'textAlign': 'center',
                    'color': DASHBOARD_STYLES['text_muted'],
                    'fontSize': '14px',
                    'marginTop': '20px',
                }),
            ]),
            
        ], style={
            'backgroundColor': DASHBOARD_STYLES['background'],
            'color': DASHBOARD_STYLES['text'],
            'padding': '30px',
            'minHeight': '100vh',
            'fontFamily': 'system-ui, -apple-system, sans-serif',
        })
    
    def _generate_data(self, data_type, n_points, noise_level):
        """
        Generate sample astronomical data based on user parameters.
        
        Parameters:
        -----------
        data_type : str
            Type of data to generate
        n_points : int
            Number of data points
        noise_level : float
            Amount of random noise to add
            
        Returns:
        --------
        x, y : numpy arrays
            The generated data
        """
        x = np.linspace(0, 10, n_points)
        
        if data_type == 'sine':
            y = np.sin(x) + noise_level * np.random.random(n_points)
            
        elif data_type == 'exponential':
            y = np.exp(-x / 3) + noise_level * 0.5 * np.random.random(n_points)
            
        elif data_type == 'spectrum':
            # Continuum with noise
            y = 1 + 0.1 * np.sin(5 * x) + noise_level * 0.5 * np.random.random(n_points)
            # Add absorption features
            absorption_centers = [2.5, 5.0, 7.5]
            absorption_depths = [0.25, 0.15, 0.20]
            for center, depth in zip(absorption_centers, absorption_depths):
                y -= depth * np.exp(-(x - center)**2 / 0.15)
                
        elif data_type == 'lightcurve':
            trend = -0.01 * x  # Slow dimming
            periodic = 0.08 * np.sin(2 * np.pi * x / 2.5)  # Periodic variation
            y = 1 + trend + periodic + noise_level * 0.2 * np.random.random(n_points)
            
        elif data_type == 'transit':
            y = np.ones(n_points)
            transit_center = 5.0
            transit_duration = 1.5
            transit_depth = 0.015
            # Flat bottom transit
            in_transit = np.abs(x - transit_center) < transit_duration / 2
            y[in_transit] -= transit_depth
            # Smooth ingress/egress
            ingress = (x > transit_center - transit_duration/2 - 0.3) & \
                      (x < transit_center - transit_duration/2 + 0.1)
            egress = (x > transit_center + transit_duration/2 - 0.1) & \
                     (x < transit_center + transit_duration/2 + 0.3)
            y[ingress] -= transit_depth * 0.5
            y[egress] -= transit_depth * 0.5
            y += noise_level * 0.1 * np.random.random(n_points)
            
        else:  # random walk
            y = np.cumsum(np.random.randn(n_points) * 0.3)
            y += noise_level * np.random.random(n_points)
        
        return x, y
    
    def _setup_callbacks(self):
        """Setup interactive callbacks for real-time updates."""
        
        @self.app.callback(
            [
                Output('main-plot', 'figure'),
                Output('histogram-plot', 'figure'),
                Output('statistics-panel', 'children'),
                Output('education-panel', 'children'),
            ],
            [
                Input('data-type', 'value'),
                Input('n-points', 'value'),
                Input('noise-level', 'value'),
            ]
        )
        def update_dashboard(data_type, n_points, noise_level):
            """Update all dashboard components when parameters change."""
            
            # Generate data
            x, y = self._generate_data(data_type, n_points, noise_level)
            
            # Get data type info
            info = DATA_TYPE_INFO.get(data_type, DATA_TYPE_INFO['sine'])
            
            # ============================================================
            # CREATE MAIN PLOT
            # ============================================================
            main_fig = go.Figure()
            
            main_fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines+markers',
                name='Data',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(
                    size=7,
                    color='white',
                    line=dict(width=2, color=self.colors['primary'])
                ),
                hovertemplate=(
                    f"<b>{info['xlabel']}:</b> %{{x:.4f}}<br>"
                    f"<b>{info['ylabel']}:</b> %{{y:.4f}}<br>"
                    "<extra></extra>"
                ),
            ))
            
            main_fig.update_layout(
                title=dict(
                    text=f"<b>{info['icon']} {info['title']}</b>",
                    font=dict(size=24, color='white'),
                    x=0.5,
                ),
                xaxis_title=dict(text=info['xlabel'], font=dict(size=18)),
                yaxis_title=dict(text=info['ylabel'], font=dict(size=18)),
                template='plotly_dark',
                height=500,
                font=dict(size=16, color='white'),
                plot_bgcolor='rgba(22, 33, 62, 0.8)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                hovermode='closest',
                margin=dict(l=60, r=40, t=60, b=50),
            )
            
            main_fig.update_xaxes(
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=14),
            )
            main_fig.update_yaxes(
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=14),
            )
            
            # ============================================================
            # CREATE HISTOGRAM
            # ============================================================
            hist_fig = go.Figure()
            
            hist_fig.add_trace(go.Histogram(
                x=y,
                nbinsx=25,
                name='Distribution',
                marker_color=self.colors['secondary'],
                opacity=0.8,
                hovertemplate=(
                    "<b>Value:</b> %{x:.3f}<br>"
                    "<b>Count:</b> %{y}<br>"
                    "<extra></extra>"
                ),
            ))
            
            hist_fig.update_layout(
                title=dict(
                    text="<b>Y-Value Distribution</b>",
                    font=dict(size=18, color='white'),
                    x=0.5,
                ),
                xaxis_title=dict(text=info['ylabel'], font=dict(size=14)),
                yaxis_title=dict(text="Frequency", font=dict(size=14)),
                template='plotly_dark',
                height=350,
                font=dict(size=14, color='white'),
                plot_bgcolor='rgba(22, 33, 62, 0.8)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=50, r=30, t=50, b=40),
                bargap=0.1,
            )
            
            hist_fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
            hist_fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
            
            # ============================================================
            # CALCULATE STATISTICS
            # ============================================================
            mean_val = np.mean(y)
            std_val = np.std(y)
            min_val = np.min(y)
            max_val = np.max(y)
            range_val = max_val - min_val
            median_val = np.median(y)
            
            # Create statistics panel with explanations
            stats_panel = html.Div([
                # Statistics values
                html.Div([
                    self._create_stat_row("Mean", mean_val, self.colors['primary']),
                    self._create_stat_row("Std Dev", std_val, self.colors['warning']),
                    self._create_stat_row("Median", median_val, self.colors['info']),
                    self._create_stat_row("Min", min_val, self.colors['cyan']),
                    self._create_stat_row("Max", max_val, self.colors['success']),
                    self._create_stat_row("Range", range_val, self.colors['secondary']),
                ], style={'marginBottom': '15px'}),
                
                # Data info
                html.Hr(style={'borderColor': 'rgba(255,255,255,0.2)'}),
                html.Div([
                    html.P([
                        html.Strong("Points: ", style={'color': self.colors['light']}),
                        f"{n_points}",
                    ], style={'marginBottom': '5px'}),
                    html.P([
                        html.Strong("Noise Level: ", style={'color': self.colors['light']}),
                        f"{noise_level:.2f}",
                    ], style={'marginBottom': '5px'}),
                ], style={'fontSize': '15px', 'color': DASHBOARD_STYLES['text_muted']}),
            ])
            
            # ============================================================
            # CREATE EDUCATION PANEL
            # ============================================================
            education_panel = html.Div([
                html.H4(
                    f"{info['icon']} {info['title']}",
                    style={
                        'color': self.colors['primary'],
                        'marginBottom': '15px',
                        'fontSize': '20px',
                    }
                ),
                html.P(
                    info['description'],
                    style={
                        'fontSize': '16px',
                        'lineHeight': '1.7',
                        'marginBottom': '15px',
                        'color': DASHBOARD_STYLES['text'],
                    }
                ),
                html.Div([
                    html.H5(
                        "🔭 Astronomy Context:",
                        style={
                            'color': self.colors['success'],
                            'marginBottom': '10px',
                            'fontSize': '17px',
                        }
                    ),
                    html.P(
                        info['astronomy_context'],
                        style={
                            'fontSize': '15px',
                            'lineHeight': '1.7',
                            'color': DASHBOARD_STYLES['text_muted'],
                            'paddingLeft': '15px',
                            'borderLeft': f"3px solid {self.colors['success']}",
                        }
                    ),
                ]),
            ])
            
            return main_fig, hist_fig, stats_panel, education_panel
    
    def _create_stat_row(self, label, value, color):
        """Create a formatted statistics row."""
        return html.Div([
            html.Span(
                f"{label}: ",
                style={
                    'fontWeight': 'bold',
                    'color': color,
                    'fontSize': '16px',
                    'display': 'inline-block',
                    'width': '100px',
                }
            ),
            html.Span(
                f"{value:.4f}",
                style={
                    'fontSize': '16px',
                    'fontFamily': 'monospace',
                    'color': DASHBOARD_STYLES['text'],
                }
            ),
        ], style={'marginBottom': '10px', 'lineHeight': '1.8'})
    
    def run(self, debug=False, port=8050, host='127.0.0.1'):
        """
        Launch the dashboard server.
        
        Parameters:
        -----------
        debug : bool
            If True, enable hot-reloading and debug messages.
            Set to False for cleaner output.
        port : int
            Port number to run the server on (default: 8050)
        host : str
            Host address (default: 127.0.0.1 for localhost only)
            Use '0.0.0.0' to allow external connections
        """
        print("\n" + "=" * 60)
        print("🔭 ASTRONOMY FOUNDATION DASHBOARD")
        print("=" * 60)
        print(f"\n🚀 Starting dashboard server...")
        print(f"📊 Open your browser to: http://localhost:{port}")
        print(f"\n💡 Features:")
        print(f"   • Select different astronomical data types")
        print(f"   • Adjust number of points and noise level")
        print(f"   • View real-time statistics and distributions")
        print(f"   • Learn about each data type's astronomy context")
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 60 + "\n")
        
        self.app.run_server(debug=debug, port=port, host=host)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for running the dashboard."""
    try:
        dashboard = FoundationDashboard()
        dashboard.run()
    except ImportError as e:
        print("\n❌ Missing required packages!")
        print(f"   Error: {e}")
        print("\n📦 Install dependencies with:")
        print("   pip install dash plotly numpy pandas")
        print("\n")
        return 1
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())