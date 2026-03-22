# Projectile Motion Simulation — Animated Visualization

A projectile motion simulator built in Python, developed as a class project for Classical Mechanics. Simulates a steel sphere launched at a fixed angle and speed, comparing three physical models under the Velocity Verlet integration scheme. The project examines how atmospheric drag — both constant and altitude-dependent — deviates from the idealized vacuum trajectory.

---

## Models

Three levels of physical complexity are compared throughout:

**Vacuum** — gravity only, no air resistance. The idealized baseline. Produces the longest range and highest peak, following the standard parabolic trajectory.

**Constant Drag** — drag force $\vec{F}_D = c \cdot v^2$ with fixed drag coefficient $c = \gamma D^2$, independent of altitude. Models air resistance as uniform throughout the flight. Shorter range and lower peak than vacuum.

**Altitude-Dependent Drag** — drag coefficient varies with altitude as $c(y) = \gamma D^2 e^{-y/\lambda}$, where $\lambda$ is the atmospheric scale height. Air thins with altitude, so drag is weaker at the peak and stronger near the ground. Trajectory falls between vacuum and constant drag at altitude, converging toward constant drag near landing.

---

## Stage 1 — Trajectory Simulation

### Object & Initial Conditions
Simulates a steel sphere with the following parameters:

- Diameter: $D = 0.07$ m
- Density: $\rho = 7800$ kg/m³
- Launch speed: $v_0 = 300$ m/s
- Launch angle: $\theta = 50°$
- Origin: $(x, y) = (0, 0)$

### Numerical Method
Trajectories are computed using the **Velocity Verlet algorithm**, a second-order symplectic integrator well-suited for systems with velocity-dependent forces. Each time step proceeds as:

1. Update position using current velocity and acceleration
2. Compute temporary new acceleration (new position, old velocity)
3. Compute temporary new velocity
4. Compute final new acceleration (new position, temporary velocity)
5. Update velocity using the average of old and new accelerations
6. Reassign acceleration for the next step

Time step $\Delta t = 0.01$ s, simulation runs until $y < 0$ or $t = 35$ s.

---

## Stage 2 — Animation

### Animated Output
The notebook produces an **inline HTML animation** via `matplotlib.animation` and `IPython.display.HTML`, showing all three trajectories drawn simultaneously in real time. A sphere marker tracks each projectile's current position frame by frame.

| Color | Model |
|---|---|
| 🟢 Green | Vacuum — $\vec{F}_g$ only |
| 🔵 Blue | Constant drag — $\vec{F}_g + \vec{F}_D$ |
| 🔴 Red | Altitude-dependent drag — $\vec{F}_g + \vec{F}_D(y)$ |

---

## Relationship to Other Versions

This is the **animated visualization** of the original static matplotlib plots produced for the Classical Mechanics course project. The physics and numerical method are unchanged from the original; the animation layer was added independently afterward.

| Version | Description |
|---|---|
| **Original (course)** | Static matplotlib plots of all three trajectories |
| **This version** | Animated, frame-by-frame trajectory rendering with sphere markers |

---

## Dependencies

```
numpy
matplotlib
IPython
```

---

## Notes

- The altitude-dependent drag model uses an exponential atmospheric density profile $e^{-y/\lambda}$, where $\lambda = 10000$ m serves as the scale height.
- The angular components of velocity are updated each step via $\theta = \arctan(y/x)$ to correctly decompose the drag force into $x$ and $y$ components.
- The vacuum trajectory sets the axis bounds for the animation — all three models are plotted within the vacuum range and peak height.
