# Projectile Motion Simulation
**Hyunje Kim** — Classical Mechanics

A numerical simulation of projectile motion comparing three physical models: vacuum (no drag), constant drag, and altitude-dependent drag. Built with Python in a Jupyter Notebook, with an animated matplotlib visualization.

---

## Physics

The simulation models a steel sphere launched at an initial velocity and angle, tracking its trajectory under three conditions:

| Model | Forces | Description |
|---|---|---|
| 🟢 Vacuum | $\vec{F}_g$ | Gravity only, no air resistance |
| 🔵 Constant Drag | $\vec{F}_g + \vec{F}_D$ | Drag coefficient $c = \gamma D^2$ (constant) |
| 🔴 Altitude-Dependent Drag | $\vec{F}_g + \vec{F}_D(y)$ | Drag coefficient $c(y) = \gamma D^2 e^{-y/\lambda}$ (varies with altitude) |

---

## Object & Parameters

**Steel Sphere**
- Diameter: $D = 0.07$ m
- Density: $\rho = 7800$ kg/m³
- Mass: $m = \rho V$

**Initial Conditions**
- Launch speed: $v_0 = 300$ m/s
- Launch angle: $\theta = 50°$
- Origin: $(x, y) = (0, 0)$

**Constants**
- $g = 9.8$ m/s²
- $\gamma = 0.25$ Ns²/m⁴
- $\lambda = 10000$ m (atmospheric scale height)
- $\Delta t = 0.01$ s

---

## Numerical Method

Trajectories are computed using the **Velocity Verlet algorithm**, a second-order symplectic integrator well-suited for conservative and near-conservative systems. Each time step involves:

1. Update position using current velocity and acceleration
2. Compute a temporary new acceleration (at new position, old velocity)
3. Compute a temporary new velocity
4. Compute the final new acceleration (at new position, temporary velocity)
5. Update velocity using the average of old and new accelerations
6. Reassign acceleration for the next step

---

## Output

The notebook produces an **inline HTML animation** (via `matplotlib.animation` and `IPython.display.HTML`) showing all three trajectories being drawn simultaneously, with a sphere marker tracking each projectile's current position.

---

## Requirements

```
numpy
matplotlib
IPython
```

Run in a Jupyter environment (Jupyter Notebook, JupyterLab, or VS Code with the Jupyter extension).
