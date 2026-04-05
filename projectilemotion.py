import importlib
import pm_tools
importlib.reload(pm_tools)
from pm_tools import get_rounding_from_speed

import numpy as np, pandas as pd, plotly.graph_objects as go
from math import pi, radians, cos, sin, exp, atan, sqrt
from IPython.display import HTML

class ProjectileMotion:
    def __init__(self, 
                time_step: float, # in s

                initial_position: list = [0,0], # in m, vector form [x,y]
                initial_speed: float = 300, # in m/s, scalar value    
                launch_angle: float = 45, # in degrees, angle of launch with respect to horizontal
                diameter: float = 0.07, # in m
                density: float = 7800, # in kg/m³
        ):  
        # Initial Conditions
        self.initial_position = initial_position
        self.initial_speed = initial_speed
        self.launch_angle = radians(launch_angle) # transform degrees to radians

        # Spherical Object properties
        self.diameter = diameter
        self.density = density
        self.volume = (4/3) * pi * (self.diameter/2)**3 
        self.mass = self.density * self.volume 

        # Constants
        self.gravity = 9.8 # in m/s²
        self.viscosity = 0.25 # in Ns²/m⁴, for medium that projectile is traversing through
        self.altitude_threshold = float(10e3) # in m
        self.drag_coefficient = 0.5 * self.viscosity * (self.diameter**2) # in kg/m
        
        # Time parameters
        self.time_step = time_step

        data = pd.DataFrame(self.simulate(), columns=['t', 'x', 'y'])
        position_decimals = get_rounding_from_speed(self.initial_speed) # Determine number of decimal places
        time_decimals = int(round(-np.log10(self.time_step))) # Determine number of decimal places for time
        self.data = data.round({'t': time_decimals, 'x': position_decimals, 'y': position_decimals}) # Round all columns for display/analysis

    def simulate(self):
        # Extract initial conditions and constants for ease of use
        x, y = self.initial_position[0], self.initial_position[1]
        vx = self.initial_speed * cos(self.launch_angle)
        vy = self.initial_speed * sin(self.launch_angle)
        g = self.gravity
        dt = self.time_step
        t = dt 
        data = [[0, x, y]]

        while y > -1:
            x += vx * dt # update horizontal position, V
            y += vy * dt + (0.5 * -g * dt**2) # update vertical position with gravity effect, VV

            data.append([t, x, y]) # store time, horizontal position, and vertical position in data list
            
            vy += dt * -g # update vertical velocity, VV
            t += dt # update time, VV



        # Last two points
        t1, x1, y1 = data[-2]
        t2, x2, y2 = data[-1]

        alpha = -y1 / (y2 - y1) # Interpolation factor

        # Interpolated impact time and position
        t_max = t1 + alpha * (t2 - t1)
        x_max = x1 + alpha * (x2 - x1)

        data[-1] = [t_max, x_max, 0] # Replace last point

        return data

    def animate(self):
        data = np.array(self.data)
        
        # Create frames: each frame shows trajectory up to index i and current position marker
        frames = []
        for i in range(1, len(data)):
            # Calculate dynamic axis ranges for this frame
            x_data = data[:i+1, 1]
            y_data = data[:i+1, 2]
            
            x_min, x_max = x_data.min(), x_data.max()
            y_min, y_max = y_data.min(), y_data.max()
            
            # Add padding (10% of range)
            x_padding = (x_max - x_min) * 0.1
            y_padding = (y_max - y_min) * 0.1
            
            frames.append(go.Frame(
                data=[
                    go.Scatter(
                        x=data[:i+1, 1], 
                        y=data[:i+1, 2], 
                        mode='lines', 
                        name='trajectory', 
                        line=dict(color='red', width=1, dash='dash'),
                        showlegend=False,
                    ),
                    go.Scatter(
                        x=[data[i, 1]], 
                        y=[data[i, 2]], 
                        mode='markers', 
                        marker=dict(color='red', size=10),
                        showlegend=False,
                        hoverinfo='skip'
                    )
                ],
                layout=go.Layout(
                    xaxis=dict(range=[x_min - x_padding, x_max + x_padding]),
                    yaxis=dict(range=[y_min - y_padding, y_max + y_padding])
                ),
                name=str(i)
            ))
        
        # Initial frame (t=0)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=data[:1, 1], 
                    y=data[:1, 2], 
                    mode='lines', 
                    name='trajectory', 
                    line=dict(color='red', width=1, dash='dash'),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[data[0, 1]], 
                    y=[data[0, 2]], 
                    mode='markers', 
                    marker=dict(color='red', size=10),
                    showlegend=False,
                    hoverinfo='skip'
                )
            ],
            frames=frames
        )
        
        # Set initial axis ranges
        initial_x_range = [data[0, 1] - 10, data[0, 1] + 10]  # data[0,1] is x
        initial_y_range = [data[0, 2] - 10, data[0, 2] + 10]  # data[0,2] is y
        
        # Add play/pause buttons and slider
        fig.update_layout(
            title='Trajectory',
            xaxis_title='Distance (m)',
            yaxis_title='Height (m)',
            xaxis=dict(range=initial_x_range),
            yaxis=dict(range=initial_y_range),
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'x': 0.1,
                'y': 1.15,
                'buttons': [
                    {
                        'label': 'Play', 
                        'method': 'animate', 
                        'args': [None, {
                            'frame': {'duration': 60, 'redraw': True}, # adjust duration for smoother animation
                            'fromcurrent': True,
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    },
                    {
                        'label': 'Pause', 
                        'method': 'animate', 
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False}, 
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ]
            }],
            sliders=[{
                'active': 0,
                'steps': [
                    {
                        'label': f"{data[i][0]:.2f}s",
                        'method': 'animate',
                        'args': [[str(i)], {
                            'frame': {'duration': 0, 'redraw': True},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                    for i in range(len(data))
                ],
                'x': 0.1,
                'len': 0.9,
                'xanchor': 'left',
                'y': 0,
                'yanchor': 'top'
            }]
        )
        
        fig.add_hline(y=0, line_dash='solid', line_color='black', opacity=0.5)
        fig.show()