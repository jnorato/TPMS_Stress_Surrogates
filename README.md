# Surrogate Models of Stress for Triply Periodic Minimal Surface Lattices

**Authors:**  
Sy Nguyen-Van, Guha Manogharan, Lan-Hsuan Huang, Julián A. Norato

## Citation
Sy Nguyen-Van, Guha Manogharan, Lan-Hsuan Huang, Julián A. Norato,  
**Surrogate models of stress for triply periodic minimal surface lattices**,  
*Computer Methods in Applied Mechanics and Engineering*,  
Volume 444, 2025, 118119, ISSN 0045-7825.  
[https://doi.org/10.1016/j.cma.2025.118119](https://doi.org/10.1016/j.cma.2025.118119)  
[ScienceDirect Article](https://www.sciencedirect.com/science/article/pii/S0045782525003913)

## Keywords
TPMS lattices · Surrogate models · Multi-scale analysis

---

## Instructions

### 1. Graphical User Interface (GUI)
To launch the GUI, run:

```bash
python Main_GUI_TPMS.py
```

> **Note**: Ensure `tkinter` is installed on your system before running the GUI.

---

### 2. Predicting Stress Using Surrogate Models

Use `Surrogates_Stress.py` to predict stress values.

```python
import matplotlib
import matplotlib.pyplot as plt
from Surrogates_Stress import *

TPMS, Shell_Surface = 'Gyroid', 'Bottom'
F_X, F_Y, F_Z = 10, 10, 10
F_XY, F_XZ, F_YZ = 10, 10, 10
Thick_rho_label, Thick_rho = 'Thickness', 0.1
Poisson_user, Cell_Size = 0.3, 1

fig, Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max, Density_TPMS, min_thick_rho, max_thick_rho, Unit_18 = Surrogates_Stress(
    TPMS, Shell_Surface, F_X, F_Y, F_Z, F_XY, F_XZ, F_YZ, 
    Thick_rho_label, Thick_rho, Poisson_user, Cell_Size
)
fig
```

---

### 3. Predicting Elasticity Tensor Using Surrogate Models

Use `Surrogates_Homogenization.py` to predict the elasticity tensor.

```python
import matplotlib
import matplotlib.pyplot as plt
from Surrogates_Homogenization import *

TPMS = 'Gyroid'
Density_user, Poisson_user, Young_user = 0.1, 0.3, 1119e3

fig, Young, Poisson, Shear, Elasticity_Tensor = Surrogates_Homogenization(
    TPMS, Density_user, Poisson_user, Young_user
)
fig
```