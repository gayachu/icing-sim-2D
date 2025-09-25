import numpy as np
import matplotlib.pyplot as plt

# ───── Plate / grid parameters ──────────────────────────────
Lx, Ly = 1.0, 0.5       # plate dimensions in meters
Nx, Ny = 200, 100       # grid resolution in X and Y
dx, dy = Lx/Nx, Ly/Ny
xv = np.linspace(0, Lx, Nx)
yv = np.linspace(0, Ly, Ny)

# initial temperature field (°C)
T = np.ones((Nx,Ny)) * 5.0

# simple 3×3 kernel (sum to 1)
weights = np.array([[1, 2, 1],
                    [2, 4, 2],
                    [1, 2, 1]], float)
weights /= weights.sum()

# ───── Diffusion parameters ─────────────────────────────────
alpha     = 1e-4       # thermal diffusivity
dt_heat   = 1e-3
Fo_x      = alpha*dt_heat/dx**2
Fo_y      = alpha*dt_heat/dy**2
n_diffuse = 1         # diffusion sub-steps per batch

# ───── Droplet‐spray parameters ─────────────────────────────
n_drop   = 100000
dT_drop  = 0.1       # °C cooled per drop 
rng      = np.random.default_rng(0)

total_hits = 0
max_hits   = 1000000

# ───── Main loop: spray, cool, diffuse ──────────────────────
while total_hits < max_hits:
    # 1) Spray all drops at once onto random (x,y) on plate
    xw = rng.random(n_drop) * Lx
    yw = rng.random(n_drop) * Ly

    # 2) For each drop, map to plate grid and apply cooling
    for i in range(n_drop):
        ix = int(np.floor(xw[i]/Lx * Nx))
        iy = int(np.floor(yw[i]/Ly * Ny))
        ix = np.clip(ix, 0, Nx-1)
        iy = np.clip(iy, 0, Ny-1)

        # apply 3×3 cooling stencil around (ix,iy)
        for dx_off in (-1,0,1):
            for dy_off in (-1,0,1):
                jx = ix + dx_off
                jy = iy + dy_off
                if 0 <= jx < Nx and 0 <= jy < Ny:
                    T[jx,jy] -= dT_drop * weights[dx_off+1, dy_off+1]

        total_hits += 1
        if total_hits >= max_hits:
            break

    # 3) In‐plane diffusion every batch
    for _ in range(n_diffuse):
        Tn = T.copy()
        Tn[1:-1,1:-1] = (
            T[1:-1,1:-1]
          + Fo_x*(T[2:,1:-1]   - 2*T[1:-1,1:-1] + T[:-2,1:-1])
          + Fo_y*(T[1:-1,2:]   - 2*T[1:-1,1:-1] + T[1:-1,:-2])
        )
        T = Tn

    # 4) Stop if any cell drops below zero
    if (T < 0).any():
        print(f"Ice formed after {total_hits} drops!")
        break

# ───── Plotting ──────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4))

# Ice mask
im1 = ax1.imshow((T.T<0), origin='lower',
                 extent=[0,Lx,0,Ly], cmap='Blues')
ax1.set_title("Ice mask (blue=ice)")
ax1.set_xlabel("x (m)")
ax1.set_ylabel("y (m)")

# Temperature field
im2 = ax2.imshow(T.T, origin='lower',
                 extent=[0,Lx,0,Ly], cmap='coolwarm')
ax2.set_title("Temperature (°C)")
ax2.set_xlabel("x (m)"); ax2.set_ylabel("y (m)")
fig.colorbar(im2, ax=ax2, label="T (°C)")

plt.tight_layout()
plt.show()