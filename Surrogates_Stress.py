import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Additional_Functions import*
# =============
def Surrogates_Stress(TPMS,Shell_Surface, F_X, F_Y, F_Z, F_XY, F_XZ, F_YZ, Thickness_user, Poisson_user, Cell_Size):
    #================GET-INPUTS==============================
    Folder_Path_Data = 'Surrogates_Stress/' 
    Folder_Path_Coeffs = 'Surrogates_Stress/'  +  'Sur_Poly/' 
    # ========SHELL ELEMENTS=========
    # Read the CSV file into DataFrames
    df_vertices_1 = pd.read_csv(Folder_Path_Data +TPMS +'_Unit_Size_1_Nodes.csv', header=None)
    vertices_1 = df_vertices_1.values
    # ===
    vertices_2 = vertices_1*float(Cell_Size)
    # ---
    df_elements = pd.read_csv(Folder_Path_Data+TPMS +'_Unit_Size_1_Shell_Elements.csv', header=None)
    elements = (df_elements.values).astype(int)  # Adjust for zero-based indexing in Python
    # ---
    faces_2 = [[vertices_2[tri[0]], vertices_2[tri[1]], vertices_2[tri[2]], vertices_2[tri[3]]] for tri in elements]
    #-----------Train-Test-No of Thick/Poisson-----------------------
    Unit_Size = 1  # Unit cell of 1x1x1
    num_samples_train = 1000
    num_samples_test = 200 
    num_samples_pred = 30 
    degree_x = 9
    degree_y = 5  
    min_rho_list = [0.063, 0.057, 0.079]
    max_rho_list = [0.653, 0.458, 0.574]
    Area_list = [3.09, 2.35, 3.56]
    rho_thick_list = [0.324, 0.426, 0.281]
    # --------------------------------------
    # min_thick_list = np.round(np.array(min_rho_list) / np.array(Area_list), 3)
    # max_thick_list = np.round(np.array(max_rho_list) / np.array(Area_list), 3)
    min_thick_list = np.array([0.02 , 0.024, 0.022])
    max_thick_list = np.array([0.211, 0.195, 0.161])
    min_poisson = 0.2; # Minimum poisson
    max_poisson = 0.4; # Maximum poisson
    if TPMS == 'Gyroid':
        min_thick = min_thick_list[0]
        max_thick = max_thick_list[0]
        rho_thick_TPMS = rho_thick_list[0]
    elif TPMS == 'Primitive': 
        min_thick = min_thick_list[1]
        max_thick = max_thick_list[1]
        rho_thick_TPMS = rho_thick_list[1]
    elif TPMS == 'IWP':
        min_thick = min_thick_list[2]
        max_thick = max_thick_list[2]
        rho_thick_TPMS = rho_thick_list[2]
    # ================================================
    Loads = ['E11', 'E22', 'E33', 'E12', 'E13', 'E23']    
    Loads_Tittle = ['X-Normal', 'Y-Normal', 'Z-Normal', 'XY-Shear', 'XZ-Shear', 'YZ-Shear']
    # Method of surrogates models
    opti_methods = 'Sur_Poly'  # Sur_Poly; RBF
    Name_Scaler = 'MinMax';   # 0-No  1- Std; 2-MinMax
    name_model = TPMS + '_Micro'    # Model TPMS's name
    No_Thick_Pred, Traction_Pred = 10, 10
    # ===============
    Train_Test_Pred = 'Train' 
    df_X_Train = pd.read_csv( Folder_Path_Data + TPMS + '_Thick_Poisson_' +Train_Test_Pred + '_LHS_' + str(num_samples_train) + '.csv', header=None) # Import csv file        
    X_Train = df_X_Train.values
    Thick_Set_Train, Poisson_Set_Train = X_Train[:,0], X_Train[:,1]
    #=========CHECKING VALIDITY OF INPUTS=================   
    if is_number(Thickness_user) or float(Thickness_user)*float(Cell_Size) < min_thick*float(Cell_Size) or float(Thickness_user)*float(Cell_Size) > max_thick*float(Cell_Size):                
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.6, 'Invalid Thickness!!!', fontsize = 30, fontweight='bold', color = 'red',ha='center')
        ax.text(0.5, 0.5, 'Unit cell size: {}'.format(float(Cell_Size)), fontweight='bold',fontsize=30, ha='center')
        ax.text(0.5, 0.4, 'Min Thickness: {}'.format(min_thick*float(Cell_Size)), fontweight='bold',fontsize=30, ha='center')
        ax.text(0.5, 0.3, 'Max Thickness: {}'.format(max_thick*float(Cell_Size)), fontweight='bold',fontsize=30, ha='center')
        ax.axis('off')
        Density_TPMS = 0
        Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max = 0, 0, 0, 0
    elif is_number(Poisson_user) or float(Poisson_user) < min_poisson or float(Poisson_user) > max_poisson:                
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.6, "Invalid Poisson's ratio !!!", fontsize = 30, fontweight='bold', color = 'red',ha='center')
        ax.text(0.5, 0.4, "Min Poisson's ratio: {}".format(min_poisson), fontweight='bold',fontsize=30, ha='center')
        ax.text(0.5, 0.3, "Max Poisson's ratio: {}".format(max_poisson), fontweight='bold',fontsize=30, ha='center')
        ax.axis('off')
        Density_TPMS = 0
        Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max = 0, 0, 0, 0
    elif is_number(F_X) or is_number(F_Y) or is_number(F_Z) or is_number(F_XY) or is_number(F_XZ) or is_number(F_YZ):                
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.6, 'Invalid Values!!!', fontsize = 30, fontweight='bold', color = 'red',ha='center')
        ax.axis('off')
        Density_TPMS = 0
        Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max = 0, 0, 0, 0
    else:
        # ===================START PREDICTION====================
        thickness = float(Thickness_user)/float(Cell_Size) # Normalized thickness
        Density_TPMS = thickness/rho_thick_TPMS
        # ---------------    
        poisson = float(Poisson_user) # Poisson from users
        # Traction applied to unit cells
        Traction_Vec = np.array([float(F_X), float(F_Y), float(F_Z), float(F_XY), float(F_XZ), float(F_YZ)])
        #--------------------------------IMPORT-XYZ-------------------------------------           
        df_Abaqus = pd.read_pickle( Folder_Path_Data + name_model + '_' + 'E11' + '_Thick_Poisson_' +  str(Traction_Pred) + 
                                   '_Macro_Force_'  + 'Pred_LHS_'+str(num_samples_pred) + '_' + Shell_Surface + '.pkl' , compression='zip')  # Import csv file        
        data_Unit_18 = df_Abaqus.values
        #--no of elements--
        no_ele = int(data_Unit_18.shape[0]/8)      
        no_Unit_SGs = 1;     #  No of Units for surrogate models
        XYZ_Unit_SGs = data_Unit_18[:int(no_Unit_SGs*no_ele),0:3]
        # ============= START LINEAR COMBINATION AND SUPERPOSITION =============
        PRED_X  = np.zeros((8*no_ele,6)) # Initial space for sigma_x
        PRED_Y  = np.zeros((8*no_ele,6)) # Initial space for sigma_y
        PRED_XY = np.zeros((8*no_ele,6)) # Initial space for sigma_xy
        Unit_18 = np.zeros((8*no_ele,7)) # Initial space for sigma
        PRED_CASES = []
        for E_ij, Load_Case in enumerate(Loads):
            Coeffs_x  =  [] 
            Coeffs_y  =  []
            Coeffs_xy =  [] 
            Unit_18_i_case = []  
            Load_tittle  = Loads_Tittle[E_ij] # Load case E_ij
            Traction = Traction_Vec[E_ij]   # Traction in load case E_ij
            # Load coefficient of cubic splines        
            File_Name_Coeffs =  Folder_Path_Coeffs + name_model + '_' + Load_Case + '_' + opti_methods +'_' + str(degree_x) + '_' +str(degree_y) + '_' + Name_Scaler  + '_LHS_' + str(num_samples_train)+ '_'

            df_Coeffs_x_Top = pd.read_pickle( File_Name_Coeffs + 'Coeffs_11'+ '_' + 'Top' +'.pkl' , compression='zip')    # Coeffs_x                    
            df_Coeffs_y_Top = pd.read_pickle(File_Name_Coeffs + 'Coeffs_22' + '_' + 'Top'+'.pkl' , compression='zip')    # Coeffs_y                  
            df_Coeffs_xy_Top = pd.read_pickle(File_Name_Coeffs + 'Coeffs_12'+ '_' + 'Top' +'.pkl' , compression='zip')  # Coeffs_xy            
            
            df_Coeffs_x_Bottom = pd.read_pickle( File_Name_Coeffs + 'Coeffs_11'+ '_' + 'Bottom' +'.pkl' , compression='zip')    # Coeffs_x                    
            df_Coeffs_y_Bottom  = pd.read_pickle(File_Name_Coeffs + 'Coeffs_22' + '_' + 'Bottom'+'.pkl' , compression='zip')    # Coeffs_y                  
            df_Coeffs_xy_Bottom  = pd.read_pickle(File_Name_Coeffs + 'Coeffs_12'+ '_' + 'Bottom' +'.pkl' , compression='zip')  # Coeffs_xy   
            
            Coeffs_x_Top = np.array(df_Coeffs_x_Top.values, dtype = float)
            Coeffs_y_Top = np.array(df_Coeffs_y_Top.values, dtype = float)
            Coeffs_xy_Top = np.array(df_Coeffs_xy_Top.values, dtype = float)  
            
            Coeffs_x_Bottom = np.array(df_Coeffs_x_Bottom.values, dtype = float)
            Coeffs_y_Bottom = np.array(df_Coeffs_y_Bottom.values, dtype = float)
            Coeffs_xy_Bottom = np.array(df_Coeffs_xy_Bottom.values, dtype = float)  
            
            # Prediction with 01 N and new thickness + scaling methods         
            if Name_Scaler == 'MinMax':
                thickness_scale = (thickness - min_thick )/(max_thick - min_thick)
                poisson_scale = (poisson -  min_poisson )/(max_poisson -min_poisson)
                
                Vec_thick_poisson = Surface_Vec(thickness_scale, poisson_scale, degree_x, degree_y) 
                # ==============TOP=======================
                prediction_x_Top  = np.dot(Coeffs_x_Top[:,2:], Vec_thick_poisson)*(Coeffs_x_Top[:,1]-Coeffs_x_Top[:,0]).reshape(-1,1) +  Coeffs_x_Top[:,0].reshape(-1,1)
                prediction_y_Top  = np.dot(Coeffs_y_Top[:,2:], Vec_thick_poisson)*(Coeffs_y_Top[:,1]-Coeffs_y_Top[:,0]).reshape(-1,1)   +  Coeffs_y_Top[:,0].reshape(-1,1)
                prediction_xy_Top = np.dot(Coeffs_xy_Top[:,2:], Vec_thick_poisson)*(Coeffs_xy_Top[:,1]-Coeffs_xy_Top[:,0]).reshape(-1,1) +  Coeffs_xy_Top[:,0].reshape(-1,1) 
                # ===============BOTTOM==================
                prediction_x_Bottom  = np.dot(Coeffs_x_Bottom[:,2:], Vec_thick_poisson)*(Coeffs_x_Bottom[:,1]-Coeffs_x_Bottom[:,0]).reshape(-1,1) +  Coeffs_x_Bottom[:,0].reshape(-1,1)
                prediction_y_Bottom  = np.dot(Coeffs_y_Bottom[:,2:], Vec_thick_poisson)*(Coeffs_y_Bottom[:,1]-Coeffs_y_Bottom[:,0]).reshape(-1,1)   +  Coeffs_y_Bottom[:,0].reshape(-1,1)
                prediction_xy_Bottom = np.dot(Coeffs_xy_Bottom[:,2:], Vec_thick_poisson)*(Coeffs_xy_Bottom[:,1]-Coeffs_xy_Bottom[:,0]).reshape(-1,1) +  Coeffs_xy_Bottom[:,0].reshape(-1,1) 
                
            #==========LINEAR COMBINATION========================       
            prediction_x_Top  = prediction_x_Top*Traction; 
            prediction_y_Top  = prediction_y_Top*Traction;  
            prediction_xy_Top = prediction_xy_Top*Traction; 
            # ==============================
            prediction_x_Bottom  = prediction_x_Bottom*Traction; 
            prediction_y_Bottom  = prediction_y_Bottom*Traction;  
            prediction_xy_Bottom = prediction_xy_Bottom*Traction; 
            # ==============================================
            Unit_SGs_Top = np.hstack((XYZ_Unit_SGs, prediction_x_Top, prediction_y_Top, prediction_xy_Top))  
            #============================================
            Unit_SGs_Bottom = np.hstack((XYZ_Unit_SGs, prediction_x_Bottom, prediction_y_Bottom, prediction_xy_Bottom))  
            #===
            if Shell_Surface == 'Top':
                Unit_1_Pred_Case = Unit_SGs_Top
                Unit_1_Pred_Case_Opposite = Unit_SGs_Bottom
            if Shell_Surface == 'Bottom':
                Unit_1_Pred_Case = Unit_SGs_Bottom
                Unit_1_Pred_Case_Opposite = Unit_SGs_Top   
            # Going into data for all Units: 1 - 8
            Unit_1 = np.zeros((no_ele,6))
            Unit_2 = np.zeros((no_ele,6))
            Unit_3 = np.zeros((no_ele,6))
            Unit_4 = np.zeros((no_ele,6))
            Unit_5 = np.zeros((no_ele,6))
            Unit_6 = np.zeros((no_ele,6))
            Unit_7 = np.zeros((no_ele,6))
            Unit_8 = np.zeros((no_ele,6))
            # Going into symmetry for each stress components
            for S_ij in range(3):
                index_Sij = [0,1,2,3 + S_ij]
                
                Unit_1_Pred =  Unit_1_Pred_Case[:, index_Sij]
                Unit_1_Pred_Opposite =  Unit_1_Pred_Case_Opposite[:, index_Sij]
                Unit_1_7_Trans, Unit_2_7_Trans, Unit_3_7_Trans, Unit_4_7_Trans, Unit_5_7_Trans, Unit_6_7_Trans, Unit_7_7_Trans, Unit_8_7_Trans = TPMS_Stress_Trans(Unit_Size, TPMS, Unit_1_Pred, Unit_1_Pred_Opposite,E_ij, S_ij)
                
                Unit_1[:, index_Sij]= Unit_1_7_Trans
                Unit_2[:, index_Sij]= Unit_2_7_Trans
                Unit_3[:, index_Sij]= Unit_3_7_Trans
                Unit_4[:, index_Sij]= Unit_4_7_Trans
                Unit_5[:, index_Sij]= Unit_5_7_Trans
                Unit_6[:, index_Sij]= Unit_6_7_Trans
                Unit_7[:, index_Sij]= Unit_7_7_Trans
                Unit_8[:, index_Sij]= Unit_8_7_Trans
            # Merger stress components together    
            Unit_18_i_case = np.vstack((Unit_1, Unit_2, Unit_3, Unit_4, Unit_5, Unit_6, Unit_7, Unit_8))            
            PRED_X[:,E_ij] = Unit_18_i_case[:, 3]
            PRED_Y[:,E_ij] = Unit_18_i_case[:, 4]
            PRED_XY[:,E_ij] = Unit_18_i_case[:,5]
        # =========End of all loading cases=================
        XYZ_CASES  = Unit_18_i_case[:,0:3]
        PRED_CASES = np.hstack((PRED_X, PRED_Y, PRED_XY))
        PRED_CASES = np.vstack((PRED_CASES))
        # SUPERPOSITION OF ALL 06 LOADING CASES
        Pred_Super = Superposition(PRED_CASES) # 
        # ----Maximum Vonmise and Shear stress
        Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max = Principal_Stress(Pred_Super)
        # STORE ALL DATA TO PLOT + SCALING OF UNIT CELLS
        Unit_18[:,0:6] = np.hstack((XYZ_CASES*float(Cell_Size), Pred_Super))         
        Unit_18[:,6] = np.sqrt(Pred_Super[:,0]**2 + Pred_Super[:,1]**2 + 3*Pred_Super[:,2]**2 - Pred_Super[:,0]*Pred_Super[:,1])
        #=============MAIN OF PLOT====================
        cmap = 'jet'
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1, projection='3d')
        # title_name =r'$\sigma_1$'
        # Data = Unit_18[:,[0,1,2,3]]        
        # ax1 = Plot_Stress_Abaqus(ax1, title_name, cmap, Data)
        title_name_1 =r'$\sigma_{11}$'
        cbar_name_1 = ' '
        colors_1 = Unit_18[:,3]  # Ensure this matches the number of elements
        norm_1 = plt.Normalize(vmin=colors_1.min(), vmax=colors_1.max())
        mapped_colors_1 = plt.cm.jet(norm_1(colors_1))  # Use the 'jet' colormap
        
        ax1 = Plot_Shell_Elements(ax1, title_name_1, cbar_name_1, norm_1, mapped_colors_1, vertices_2, faces_2)
        #---------------------------------------------
        ax2 = fig.add_subplot(2, 2, 2, projection='3d')
        # title_name =r'$\sigma_2$'
        # Data = Unit_18[:,[0,1,2,4]]
        # ax1 = Plot_Stress_Abaqus(ax1, title_name, cmap, Data)
        title_name_2 =r'$\sigma_{22}$'
        cbar_name_2 = ' '
        colors_2 = Unit_18[:,4]  # Ensure this matches the number of elements            
        norm_2 = plt.Normalize(vmin=colors_2.min(), vmax=colors_2.max())
        mapped_colors_2 = plt.cm.jet(norm_2(colors_2))  # Use the 'jet' colormap
        
        ax2 = Plot_Shell_Elements(ax2, title_name_2, cbar_name_2,norm_2, mapped_colors_2,vertices_2, faces_2) 
        #---------------------------------------------
        ax3 = fig.add_subplot(2, 2, 3, projection='3d')
        # title_name =r'$\sigma_{12}$'
        # Data = Unit_18[:,[0,1,2,5]]
        # ax1 = Plot_Stress_Abaqus(ax1, title_name, cmap, Data)
        title_name_3 =r'$\sigma_{12}$'
        cbar_name_3 = ' '
        colors_3 = Unit_18[:,5]  # Ensure this matches the number of elements
        norm_3 = plt.Normalize(vmin=colors_3.min(), vmax=colors_3.max())
        mapped_colors_3 = plt.cm.jet(norm_3(colors_3))  # Use the 'jet' colormap
        
        ax3 = Plot_Shell_Elements(ax3, title_name_3, cbar_name_3,norm_3, mapped_colors_3,vertices_2, faces_2)
        #---------------------------------------------        
        ax4 = fig.add_subplot(2, 2, 4, projection='3d')        
        # title_name =r'$\sigma_{vm}$'
        # Data = Unit_18[:,[0,1,2,6]]
        # ax1 = Plot_Stress_Abaqus(ax1, title_name, cmap, Data)
        
        title_name_4 = r'$\sigma_{vm}$'
        cbar_name_4 = ' '
        colors_4 = Unit_18[:,6]  # Ensure this matches the number of elements
        norm_4 = plt.Normalize(vmin=colors_4.min(), vmax=colors_4.max())
        mapped_colors_4 = plt.cm.jet(norm_4(colors_4))  # Use the 'jet' colormap
        
        ax4 = Plot_Shell_Elements(ax4, title_name_4, cbar_name_4,norm_4, mapped_colors_4,vertices_2, faces_2)


    return fig, Density_TPMS, Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max