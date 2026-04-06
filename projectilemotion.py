import importlib
import pm_tools
importlib.reload(pm_tools)
from pm_tools import get_rounding_from_speed, no_drag, const_drag, alt_drag # Import necessary functions from pm_tools.py

import numpy as np, pandas as pd, plotly.graph_objects as go
from math import pi, radians
from IPython.display import HTML

class ProjectileMotion:
    def __init__(self, 
                time_step: float = 0.1, # in s, time step for the simulation. Smaller values will yield smoother trajectories but will take longer to compute. Default is 0.1 s.
                initial_position: list = [0,0], # in m, vector form [x,y]
                initial_speed: float = 300, # in m/s, scalar value    
                launch_angle: float = 45, # in degrees, angle of launch with respect to horizontal
                diameter: float = 0.07, # in m, diameter of the spherical projectile. Default is 0.07 m, which simulates a standard baseball.
                density: float = 7800, # in kg/m³, density of the spherical projectile. Default is 7800 kg/m³, which simulates a standard baseball.
                viscosity: float = 0.25, # in Ns²/m⁴, for medium that projectile is traversing through. Default is 0.25, which simulates air resistance.
                altitude_threshold: float = 10e3, # in m, threshold when continuous drag starts to decrease exponentially to simulate thinning atmosphere. Default is 10,000 m.
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
        self.viscosity = viscosity 
        self.drag_coefficient = 0.5 * self.viscosity * (self.diameter**2) # in kg/m
        self.altitude_threshold = altitude_threshold # in m
        
        self.time_step = time_step

        data = pd.DataFrame(self.simulate(), columns=['t', 'x', 'y', 'vx', 'vy', 'ax', 'ay']) # Run the simulation and store results in a DataFrame
        position_decimals = get_rounding_from_speed(self.initial_speed) # Determine number of decimal places
        time_decimals = int(round(-np.log10(self.time_step))) # Determine number of decimal places for time
        self.data = data.round({'t': time_decimals, # Round all columns for display/analysis
                                'x': position_decimals, 'y': position_decimals,
                                'vx': position_decimals, 'vy': position_decimals,
                                'ax': position_decimals, 'ay': position_decimals
                                })

    def simulate(self):
        if self.viscosity > 0 and self.altitude_threshold > 0: # if viscosity and altitude_threshold are greater than 0, we assume there is altitude-dependent drag.
            self.color = 'green'
            return alt_drag(
                initial_position=self.initial_position,
                initial_speed=self.initial_speed,
                launch_angle=self.launch_angle,
                gravity=self.gravity,
                time_step=self.time_step,
                mass=self.mass,
                drag_coefficient=self.drag_coefficient,
                altitude_threshold=self.altitude_threshold
            )

        elif self.viscosity > 0 and self.altitude_threshold == 0: # if viscosity is greater than 0 and altitude_threshold is 0, we assume there is constant drag.
            self.color = 'blue'
            return const_drag(
                initial_position=self.initial_position,
                initial_speed=self.initial_speed,
                launch_angle=self.launch_angle,
                gravity=self.gravity,
                time_step=self.time_step,
                mass=self.mass,
                drag_coefficient=self.drag_coefficient
            )
        
        else: # if viscosity/altitude_threshold is 0, we assume there is no drag.
            self.color = 'red'
            return no_drag(
                initial_position=self.initial_position,
                initial_speed=self.initial_speed,
                launch_angle=self.launch_angle,
                gravity=self.gravity,
                time_step=self.time_step
            )
    
    def animate(self):
        data = np.array(self.data)
        color = self.color

        # Create frames: each frame shows trajectory up to index i and current position marker
        frames = []
        for i in range(len(data)):
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
                        line=dict(color=color, width=1, dash='dash'),
                        showlegend=False,
                    ),
                    go.Scatter(
                        x=[data[i, 1]], 
                        y=[data[i, 2]], 
                        mode='markers', 
                        marker=dict(color=color, size=10),
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
                    line=dict(color=color, width=1, dash='dash'),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[data[0, 1]], 
                    y=[data[0, 2]], 
                    mode='markers', 
                    marker=dict(color=color, size=10),
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