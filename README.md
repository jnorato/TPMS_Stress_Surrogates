1. To use graphical user interface (GUI): Run "Main_GUI_TPMS.py". The users need to install "tkinter" before using
2. For stress's prediction, call "Surrogates_Stress.py"
```
  import matplotlib
  import matplotlib.pyplot as plt
  from Surrogates_Stress import*
  TPMS, Shell_Surface = 'Gyroid', 'Bottom'
  F_X, F_Y, F_Z, F_XY, F_XZ, F_YZ = 10,10,10,10,10,10
  Thick_rho_label, Thick_rho, Poisson_user, Cell_Size = 'Thickness', 0.1, 0.3, 1
  fig, Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max, Density_TPMS, min_thick_rho, max_thick_rho = Surrogates_Stress(TPMS,Shell_Surface, F_X, F_Y, F_Z, F_XY, F_XZ, F_YZ, Thick_rho_label, Thick_rho, Poisson_user, Cell_Size)
  fig
      
  ```
4. For Elasticity tensor's prediction, call "Surrogates_Homogenization.py"
  ```
  import matplotlib
  import matplotlib.pyplot as plt
  from Surrogates_Homogenization import*
  TPMS = 'Gyroid'
  Density_user, Poisson_user, Young_user = 0.1, 0.3, 1119e3
  fig, Young, Poisson, Shear = Surrogates_Homogenization(TPMS, Density_user, Poisson_user, Young_user)
  fig
  ```
