
## README: 2D Droplet Spray Cooling Simulation

This script simulates the cooling effect of randomly falling water droplets
on a horizontal plate. It models both local cooling from droplets and
2D heat diffusion across the plate using a finite-difference method.

---------------------------------------------
Plate / Grid:
---------------------------------------------
- Plate dimensions: L_x $\times$ L_y (meters)
- Grid resolution: N_x $\times$ N_y
- Grid spacing: dx = L_x / N_x, dy = L_y / N_y
- Coordinate vectors: x_v, y_v

---------------------------------------------
Temperature Field:
---------------------------------------------
- T[i,j] stores the temperature at grid cell (i,j) in °C
- Initial temperature: T = 5°C everywhere

---------------------------------------------
Droplet Spray:
---------------------------------------------
- Number of droplets per batch: $n_{\rm drop}$
- Cooling per droplet: $\Delta T_{\rm drop}$
- Droplet positions $(x_w, y_w)$ chosen randomly on the plate
- 3×3 weighted kernel applied around each droplet:

$$
\text{weights} =
\frac{1}{16} \begin{bmatrix}
1 & 2 & 1 \\
2 & 4 & 2 \\
1 & 2 & 1
\end{bmatrix}
$$

---------------------------------------------
2D Heat Diffusion (Finite Difference Method):
---------------------------------------------
- Thermal diffusivity: $\alpha$
- Time step: $\Delta t$
- Fourier numbers:

$$
\text{Fo}_x = \frac{\alpha \Delta t}{dx^2}, \quad
\text{Fo}_y = \frac{\alpha \Delta t}{dy^2}
$$

- Explicit 2D diffusion update for interior points:

$$
T_{i,j}^{n+1} = T_{i,j}^n + \text{Fo}_x \left(T_{i+1,j}^n - 2 T_{i,j}^n + T_{i-1,j}^n\right)+ \text{Fo}_y \left(T_{i,j+1}^n - 2 T_{i,j}^n + T_{i,j-1}^n\right)
$$

- This approximates the heat equation:

$$
\frac{\partial T}{\partial t} = \alpha \left(\frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2}\right)
$$

---------------------------------------------
Simulation Loop:
---------------------------------------------
1) Spray $n_{\rm drop}$ droplets onto random positions on the plate  
2) Apply local cooling using the 3×3 kernel  
3) Apply in-plane heat diffusion using the 2D FDM  
4) Check for ice formation: if any $T_{i,j} < 0^\circ \rm C$, stop simulation  
5) Repeat until total_hits >= max_hits

---------------------------------------------
Visualization:
---------------------------------------------
- Ice mask: shows cells where $T < 0$ (blue = ice)
  
   <img width="502" height="336" alt="image" src="https://github.com/user-attachments/assets/b32c4df0-aedc-41f2-adc9-5d85f70b1682" />

- Temperature field: heatmap of plate temperature in °C

   <img width="605" height="467" alt="image" src="https://github.com/user-attachments/assets/90566789-cbf8-4f27-8d2d-24edd7721a74" />







