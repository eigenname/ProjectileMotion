from math import cos, sin, atan2, sqrt, exp, floor, log10

def get_rounding_from_speed(value): # Determine the number of decimal places based on initial speed arg
    if value == 0:
        return 0
    return max(0, -floor(log10(abs(value))))

def no_drag(initial_position, initial_speed, launch_angle, gravity, time_step):
    # Create a simple projectile motion simulation without drag
    x, y = initial_position
    vx = initial_speed * cos(launch_angle)
    vy = initial_speed * sin(launch_angle)
    g = gravity
    dt = time_step
    t = 0
    data = [[t, x, y, vx, vy, 0, -g]] # initial state includes acceleration for consistency with other simulations

    while y >= 0:
        x += vx * dt # Update horizontal position based on current velocity & time step
        y += vy * dt - (0.5 * g * dt**2) # Update vertical position based on current velocity, gravity, and time step
        vy -= g * dt # Update vertical velocity based on gravity and time step
        t += dt 
        data.append([t, x, y, vx, vy, 0, -g]) # Append current state to data list, including acceleration for consistency with other simulations

    # extract last two points for interpolation
    t1, x1, y1 = data[-2][:3] # Unpack only the first 3 elements (t, x, y) from the second to last point
    t2, x2, y2 = data[-1][:3]

    alpha = -y1 / (y2 - y1) # Interpolation factor

    # Interpolated impact time and position
    t_max = t1 + alpha * (t2 - t1)
    x_max = x1 + alpha * (x2 - x1)

    data[-1] = [t_max, x_max, 0, 0, 0, 0, 0] # Replace last point with interpolated impact point

    return data

def const_drag(initial_position, initial_speed, launch_angle, gravity, time_step, 
               mass, drag_coefficient):
    # Now drag is a constant force opposite to the direction of motion, with magnitude proportional to speed
    x, y = initial_position
    vx = initial_speed * cos(launch_angle)
    vy = initial_speed * sin(launch_angle)
    m = mass
    g = gravity
    ax = -drag_coefficient * initial_speed * vx/m # Drag acceleration in x direction
    ay = -g -(drag_coefficient * initial_speed * vy/m) # Total acceleration in y direction includes gravity and drag
    dt = time_step
    t = 0
    data = [[t, x, y, vx, vy, ax, ay]]

    while y >= 0:
        x += vx * dt + (0.5 * ax * dt**2) # Update horizontal position based on current velocity, acceleration, and time step
        y += vy * dt + (0.5 * ay * dt**2) # Update vertical position based on current velocity, acceleration, and time step

        angle = atan2(vy, vx) # update angular component for position & velocity
        v = sqrt(vx**2 + vy**2) # update speed for drag calculation
        temp_ax = -drag_coefficient * v**2 * cos(angle)/m # Update drag acceleration based on current speed and angle
        temp_ay = -g -(drag_coefficient * v**2 * sin(angle)/m) # Update total acceleration in y direction

        temp_vx  = vx + ((0.5*dt)*(temp_ax + ax)) # Update velocity based on new acceleration
        temp_vy = vy + ((0.5*dt)*(temp_ay + ay)) # Update velocity based on new acceleration
        temp_v = sqrt(temp_vx**2 + temp_vy**2) # Update speed for next iteration's drag calculation

        new_ax = -drag_coefficient * temp_v * temp_vx/m # Update drag acceleration based on new speed and angle

        new_ay = -g -(drag_coefficient * temp_v * temp_vy/m) # Update total acceleration in y direction
        vx += ((0.5*dt)*(new_ax + ax)) # Update velocity based on new acceleration
        vy += ((0.5*dt)*(new_ay + ay)) # Update velocity based on new acceleration
        
        ax, ay = new_ax, new_ay # Update acceleration for next iteration

        t += dt
        data.append([t, x, y, vx, vy, ax, ay])

    # extract last two points for interpolation
    t1, x1, y1 = data[-2][:3] # Unpack only the first 3 elements (t, x, y) from the second to last point
    t2, x2, y2 = data[-1][:3]

    alpha = -y1 / (y2 - y1) # Interpolation factor

    # Interpolated impact time and position
    t_max = t1 + alpha * (t2 - t1)
    x_max = x1 + alpha * (x2 - x1)

    data[-1] = [t_max, x_max, 0, 0, 0, 0, 0] # Replace last point with interpolated impact point

    return data

def alt_drag(initial_position, initial_speed, launch_angle, gravity, time_step,
             mass, drag_coefficient, altitude_threshold):
    # Now drag decreases exponentially with altitude above a certain threshold to simulate thinning atmosphere.
    x, y = initial_position
    vx = initial_speed * cos(launch_angle)
    vy = initial_speed * sin(launch_angle)
    m = mass
    g = gravity
    ax = -drag_coefficient * initial_speed * vx/m # Drag acceleration in x direction
    ay = -g -(drag_coefficient * initial_speed * vy/m) # Total acceleration in y direction includes gravity and drag
    λ = altitude_threshold
    drag = drag_coefficient * exp(-y/λ) # continuous drag function that decreases with altitude
    dt = time_step
    t = 0
    data = [[t, x, y, vx, vy, ax, ay]]

    while y >= 0:
        x += vx * dt + (0.5 * ax * dt**2) # Update horizontal position based on current velocity, acceleration, and time step
        y += vy * dt + (0.5 * ay * dt**2) # Update vertical position based on current velocity, acceleration, and time step
        drag = drag_coefficient * exp(-y/λ) # update drag based on new altitude/y-value each iteration

        angle = atan2(vy, vx) # update angular component for position & velocity
        v = sqrt(vx**2 + vy**2) # update speed for drag calculation
        temp_ax = -drag * v**2 * cos(angle)/m # Update drag acceleration based on current speed and angle
        temp_ay = -g -(drag * v**2 * sin(angle)/m) # Update total acceleration in y direction

        temp_vx  = vx + ((0.5*dt)*(temp_ax + ax)) # Update velocity based on new acceleration
        temp_vy = vy + ((0.5*dt)*(temp_ay + ay)) # Update velocity based on new acceleration
        temp_v = sqrt(temp_vx**2 + temp_vy**2) # Update speed for next iteration's drag calculation

        new_ax = -drag * temp_v * temp_vx/m # Update drag acceleration based on new speed and angle

        new_ay = -g -(drag * temp_v * temp_vy/m) # Update total acceleration in y direction
        vx += ((0.5*dt)*(new_ax + ax)) # Update velocity based on new acceleration
        vy += ((0.5*dt)*(new_ay + ay)) # Update velocity based on new acceleration
        
        ax, ay = new_ax, new_ay # Update acceleration for next iteration

        t += dt
        data.append([t, x, y, vx, vy, ax, ay])

    # extract last two points for interpolation
    t1, x1, y1 = data[-2][:3] # Unpack only the first 3 elements (t, x, y) from the second to last point
    t2, x2, y2 = data[-1][:3]

    alpha = -y1 / (y2 - y1) # Interpolation factor

    # Interpolated impact time and position
    t_max = t1 + alpha * (t2 - t1)
    x_max = x1 + alpha * (x2 - x1)

    data[-1] = [t_max, x_max, 0, 0, 0, 0, 0] # Replace last point with interpolated impact point

    return data

