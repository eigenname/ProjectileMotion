import numpy as np
from math import cos, sin

def get_rounding_from_speed(value): # Determine the number of decimal places based on initial speed arg
    if value == 0:
        return 0
    return max(0, -np.floor(np.log10(abs(value))))

def no_drag(initial_position, initial_speed, launch_angle, gravity, time_step):
    # Create a simple projectile motion simulation without drag
    x, y = initial_position
    vx = initial_speed * cos(launch_angle)
    vy = initial_speed * sin(launch_angle)
    g = gravity
    dt = time_step
    t = 0
    data = [[t, x, y]]

    while y >= 0:
        x += vx * dt
        y += vy * dt - (0.5 * g * dt**2)
        vy -= g * dt
        t += dt
        data.append([t, x, y])

    # extract last two points for interpolation
    t1, x1, y1 = data[-2]
    t2, x2, y2 = data[-1]

    alpha = -y1 / (y2 - y1) # Interpolation factor

    # Interpolated impact time and position
    t_max = t1 + alpha * (t2 - t1)
    x_max = x1 + alpha * (x2 - x1)

    data[-1] = [t_max, x_max, 0] # Replace last point with interpolated impact point

    return data
