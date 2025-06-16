import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Additional_Functions import*
# ===================================
def Surrogates_Homogenization(TPMS, Density_user, Poisson_user, Young_user):
    #================GET-INPUTS==============================
    Folder_Path_Coeffs = 'Surrogates_Homogenization/'
        # ================================
    max_density = 1; # Maximum Density
    min_density_list = [0.063, 0.057, 0.0256];   # Minimum Density for Gyroid, Primitive, IWP
    min_poisson = 0.2; # Minimum poisson
    max_poisson = 0.4; # Maximum poisson  
    # ========
    Young_user =  float(Young_user)
    G =Young_user/(2*(1+min_poisson))
    degree_x = 3;
    degree_y= 1;
    # ===================================
    if TPMS == 'Gyroid': 
        i_TPMS = 0
        min_density = min_density_list[0]
    elif TPMS == 'Primitive': 
        i_TPMS = 1
        min_density = min_density_list[1]
    elif TPMS == 'IWP':
        i_TPMS = 2
        min_density = min_density_list[2]

    #=========CHECKING VALIDITY OF INPUTS=================   
    if is_number(Density_user) or float(Density_user) < min_density or float(Density_user) > max_density:                
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.6, 'Invalid Density!!!', fontsize = 30, fontweight='bold', color = 'red',ha='center')
        ax.text(0.5, 0.4, 'Min Density: {}'.format(min_density), fontweight='bold',fontsize=30, ha='center')
        ax.text(0.5, 0.3, 'Max Density: {}'.format(max_density), fontweight='bold',fontsize=30, ha='center')
        ax.axis('off')
        E_Homo_i, nu_Homo_i ,G_Homo_i = 0, 0, 0
    elif is_number(Poisson_user) or float(Poisson_user) < min_poisson or float(Poisson_user) > max_poisson:                
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.6, "Invalid Poisson's ratio !!!", fontsize = 30, fontweight='bold', color = 'red',ha='center')
        ax.text(0.5, 0.4, "Min Poisson's ratio: {}".format(min_poisson), fontweight='bold',fontsize=30, ha='center')
        ax.text(0.5, 0.3, "Max Poisson's ratio: {}".format(max_poisson), fontweight='bold',fontsize=30, ha='center')
        ax.axis('off')
        E_Homo_i, nu_Homo_i ,G_Homo_i = 0, 0, 0
    else:
        # ===================START PREDICTION====================
        Density = float(Density_user) # Density from users
        poisson = float(Poisson_user) # Poisson from users
        # Traction applied to unit cells
        # =======================================
        df_Coeffs = np.genfromtxt( Folder_Path_Coeffs+ 'TPMS_Surrogates_Homogenization_Coeffs.csv', delimiter=',') 
        Coeffs = df_Coeffs[:,:]    
        Coeffs = df_Coeffs[i_TPMS*3:i_TPMS*3+3,:]
        Coeffs_E = Coeffs[0,:].T
        Coeffs_nu = Coeffs[1,:].T
        Coeffs_G = Coeffs[2,:].T 
        for i_x in range(degree_x+1):
            for i_y in range(degree_y+1):            
                if i_x==0 and i_y==0:
                    Pred_Vec = np.ones_like(Density);
                else:
                    Pred_Vec = np.column_stack((Pred_Vec, (Density**i_x)*(poisson**i_y))) 
        #======TITTLE==== 
        # Interpolation law
        E_Homo_i = Young_user*np.dot(Pred_Vec,Coeffs_E)
        nu_Homo_i = np.dot(Pred_Vec,Coeffs_nu)
        G_Homo_i = G*np.dot(Pred_Vec,Coeffs_G)
        E_Homo_i, nu_Homo_i ,G_Homo_i = E_Homo_i[0],nu_Homo_i[0],G_Homo_i[0]
        # --------------------------
        C11 = E_Homo_i*(1-nu_Homo_i)/(1-nu_Homo_i-2*nu_Homo_i**2)
        C12 = E_Homo_i*nu_Homo_i/(1-nu_Homo_i-2*nu_Homo_i**2)
        C44 = G_Homo_i
        # ==================================================
        Elasticity_Tensor = np.array([[C11, C12, C12, 0, 0, 0], 
                                        [C12, C11, C12, 0, 0, 0], 
                                        [C12, C12, C11, 0, 0, 0], 
                                        [0, 0, 0, C44, 0, 0], 
                                        [0, 0, 0, 0, C44, 0], 
                                        [0, 0, 0, 0, 0, C44]])
        # ========================================
        
        # Plot the elasticity tensor
        fig, ax = plt.subplots()
        cax = ax.matshow(Elasticity_Tensor, cmap="coolwarm")

        # Add values to each cell
        for (i, j), val in np.ndenumerate(Elasticity_Tensor):
            ax.text(j, i, f"{val:.3f}", ha='center', va='center',  fontsize=14)
        # Customize the plot
        ax.set_xticks(range(6))
        ax.set_yticks(range(6))
        # Set tick labels as numbers 1 to 6
        ax.set_xticklabels([str(i) for i in range(1, 7)], fontsize=14)
        ax.set_yticklabels([str(i) for i in range(1, 7)], fontsize=14)
        plt.title("Elasticity Tensor",  fontsize=16)
        # =====end==========

    return fig, np.round(E_Homo_i,3), np.round(nu_Homo_i,3),np.round(G_Homo_i,3), Elasticity_Tensor