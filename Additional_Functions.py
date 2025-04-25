#=============================SETUPS===========================================
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.linalg import lstsq
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
# =============================================================
def polynomial_fit(X, Y, degree):
    for i_x in range(degree+1):
        if i_x==0 :
            A = np.ones_like(X);
        else:
            A = np.column_stack((A, (X**i_x)))      
    coefficients, _, _, _ = lstsq(A, Y)
    return  coefficients

def Predict_Poly(X, coefficients, degree):
    for i_x in range(degree+1):
        if i_x==0:
            A = np.ones_like(X);
        else:
            A = np.column_stack((A, (X**i_x)))
    Y = np.dot(A, coefficients)
    return  Y

def Vec_thick(X, degree):
    for i_x in range(degree+1):
            if i_x==0 :
                A = np.ones_like(X);
            else:
                A = np.row_stack((A, (X**i_x))); 
    return  A

#==============================================================================
def is_number(input_str):
        try:
            float(input_str)
            return False
        except ValueError:
            return True
def Superposition(Data):
   
    Data_Super = np.column_stack(( np.sum(Data[:,0:6], axis=1), np.sum(Data[:,6:12], axis=1), np.sum(Data[:,12:18], axis=1)))    
    return Data_Super
def Principal_Stress(Data):
    Sigma_x = Data[:,0]; Sigma_y = Data[:,1]; Sigma_xy = Data[:,2]
    Vonmises = np.sqrt( Sigma_x**2 + Sigma_y**2 + 3*Sigma_xy**2 - Sigma_x*Sigma_y )
    Sigma_1 = 0.5*( Sigma_x + Sigma_y) + np.sqrt((0.5*(Sigma_x-Sigma_y))**2 + Sigma_xy**2 )
    Sigma_2 = 0.5*( Sigma_x + Sigma_y) - np.sqrt((0.5*(Sigma_x-Sigma_y))**2 + Sigma_xy**2 )
    Shear_max = 0.5*np.abs( Sigma_1 - Sigma_2 )
    #=====
    Vonmises_max = round(np.max(Vonmises), 2)
    Sigma_1_max = round(np.max(Sigma_1), 2)
    Sigma_2_max = round(np.max(Sigma_2), 2)
    Shear_max = round(np.max(Shear_max), 2)
    return Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max


#==============================================================================
def polynomial_surface_fit(X, Y, Z, degree_x, degree_y):
    for i_x in range(degree_x+1):
        for i_y in range(degree_y+1):            
            if i_x==0 and i_y==0:
                A = np.ones_like(X);
            else:
                A = np.column_stack((A, (X**i_x)*(Y**i_y)))      
    coefficients, _, _, _ = lstsq(A, Z)
    return  coefficients

def Surface_Predict(X, Y, coefficients,degree_x, degree_y):
    for i_x in range(degree_x+1):
        for i_y in range(degree_y+1):            
            if i_x==0 and i_y==0:
                A = np.ones_like(X);
            else:
                A = np.column_stack((A, (X**i_x)*(Y**i_y)))
    Z = np.dot(A, coefficients)
    return  Z
def scaler_thick_poisson(X_train, X_test, y_train, y_test, Scaler_Type):               
    
    if Scaler_Type == 0:                
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        y_train_scaled = y_train.copy() 
        y_test_scaled = y_test.copy()
        Scaler_xy = []
        Name_scaler = 'NoScaler'
    if Scaler_Type == 1:
        scaler_x = StandardScaler()
        X_train_scaled = scaler_x.fit_transform(X_train)
    
        data_mean_x = scaler_x.mean_
        data_std_x = np.sqrt(scaler_x.var_)
        
        X_test_scaled = (X_test-data_mean_x)/data_std_x                    
        scaler_y = StandardScaler()
        y_train_scaled = scaler_y.fit_transform(y_train)
        data_mean_y = scaler_y.mean_
        data_std_y = np.sqrt(scaler_y.var_)            
        y_test_scaled = (y_test-data_mean_y)/data_std_y
        Scaler_xy = np.array([data_mean_y[0], data_std_y[0]])
        Name_scaler = 'Std'
    elif Scaler_Type == 2:
        scaler_x = MinMaxScaler()
        X_train_scaled = scaler_x.fit_transform(X_train)
        
        data_min_x = scaler_x.data_min_
        data_max_x = scaler_x.data_max_
        
        X_test_scaled = (X_test-data_min_x)/(data_max_x-data_min_x)                    
        scaler_y = MinMaxScaler()
        y_train_scaled = scaler_y.fit_transform(y_train)
        data_min_y = scaler_y.data_min_
        data_max_y = scaler_y.data_max_
        y_test_scaled = (y_test-data_min_y)/(data_max_y-data_min_y)                    
        Scaler_xy = np.array([data_min_y[0], data_max_y[0]])
        Name_scaler = 'MinMax'# -*- coding: utf-8 -*-
    return X_train_scaled, X_test_scaled, y_train_scaled, y_test_scaled, Scaler_xy, Name_scaler
#=============================SETUPS===========================================
def Surface_Vec(X, Y, degree_x, degree_y):
    for i_x in range(degree_x+1):
        for i_y in range(degree_y+1):            
            if i_x==0 and i_y==0:
                A = np.ones_like(X);
            else:
                A = np.row_stack((A, (X**i_x)*(Y**i_y))); 
    return  A
#=============================SETUPS===========================================

#===============
def cmap_plot(Data):
    cmap = 'jet'            
    min_cm, max_cm = np.min(Data), np.max(Data)
    norm = Normalize(vmin = min_cm, vmax = max_cm)           
    sm = ScalarMappable(norm=norm, cmap=cmap);   
    sm.set_array(np.linspace(-1, 1, 256))
    sm.set_clim(min_cm, max_cm)
    sm.autoscale_None() 
    return cmap, norm, sm

#=========Stress transformation===============================
def TPMS_Stress_Trans(Unit_Size, TPMS_Type, Unit_1, Unit_1_G, E_ij, S_ij):
    # GEOMETRY TRANSFORMATION FROM UNIT 1

    if TPMS_Type == 'Primitive' or TPMS_Type == 'IWP' or TPMS_Type == 'Neovius':
        p1 = Unit_1.copy()        
        p2 = Unit_1.copy();  
        p7 = Unit_1.copy();
        p8 = Unit_1.copy();
        
        p3 = Unit_1.copy();  
        p4 = Unit_1.copy();  
        p5 = Unit_1.copy();  
        p6 = Unit_1.copy();  
        # ---------------------------------------------------
        p2[:,0]= -p2[:,0]
        # ---------------------------------------------------
        p3[:,0]= -p3[:,0];
        p3[:,1]= -p3[:,1];
        # # -------------------------------------------------
        p4[:,1]= -p4[:,1];
        # ---------------------------------------------
        p5[:,2]= -p1[:,2] ;
        # ---------------------------------------------
        p6[:,0]= -p6[:,0] ;
        p6[:,2]= -p6[:,2] ;
        # ---------------------------------------------
        p7[:,0]= -p7[:,0] ;
        p7[:,1]= -p7[:,1] ;
        p7[:,2]= -p7[:,2] ;
        # ---------------------------------------------
        p8[:,1]= -p8[:,1] ;
        p8[:,2]= -p8[:,2] ;
        # ===========================================
        if E_ij <3 and  S_ij ==2 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = p3[:,3];
            
            p4[:,3] = -p4[:,3];
            p5[:,3] = -p5[:,3];
            
            p6[:,3] = p6[:,3];
            p7[:,3] = -p7[:,3];
            p8[:,3] = p8[:,3];

        # -------XY SHEAR-----------------------
        if E_ij == 3 and  S_ij < 2 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = p3[:,3];                
            p4[:,3] = -p4[:,3];
            
            p5[:,3] = p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = -p8[:,3];
        if E_ij == 3 and  S_ij == 2 :     
            p2[:,3] = p2[:,3];
            p3[:,3] = p3[:,3];                
            p4[:,3] = p4[:,3];
            
            p5[:,3] = -p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = -p7[:,3];
            p8[:,3] = -p8[:,3];

        # -------XZ SHEAR-----------------------
        if E_ij == 4 and  S_ij < 2 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = p4[:,3];
            
            p5[:,3] = -p5[:,3];                
            p6[:,3] = p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = -p8[:,3];
        if E_ij == 4 and  S_ij == 2 :     
            p2[:,3] = p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = -p4[:,3];
            
            p5[:,3] = p5[:,3];                
            p6[:,3] = p6[:,3];
            p7[:,3] = -p7[:,3];
            p8[:,3] = -p8[:,3];

        # -------YZ SHEAR-----------------------
        if E_ij == 5 and  S_ij < 2 :     
            p2[:,3] = p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = -p4[:,3];
            
            p5[:,3] = -p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = p8[:,3];
        if E_ij == 5 and  S_ij == 2 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = p4[:,3];
            
            p5[:,3] = p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = -p7[:,3];
            p8[:,3] = p8[:,3];        
    elif TPMS_Type == 'Gyroid':
        p1 = Unit_1.copy()     
        p3 = Unit_1.copy();   
        p5 = Unit_1.copy();  
        p7 = Unit_1.copy();
        # ==
        p2 = Unit_1_G.copy();   
        p4 = Unit_1_G.copy();
        p6 = Unit_1_G.copy();
        p8 = Unit_1_G.copy();
        # =====================
        a = Unit_Size*0.5;  
        
        p2[:, 0] = (-1)*p1[:, 0] - a
        p2[:, 1] = p1[:, 1] + a
        
        p3[:, 0] = (-1)*p1[:, 0] 
        p3[:, 1] = (-1)*p1[:, 1] - a
        
        p4[:, 0] = p1[:, 0] + a
        p4[:, 1] = (-1)*p1[:, 1] 
        

        p5[:, 0] = (-1)*p1[:, 0] - a
        p5[:, 1] = (-1)*p1[:, 1] 
        p5[:, 2] = p1[:, 2] - a
        
        p6[:, 0] = p1[:, 0]
        p6[:, 1] = (-1)*p1[:, 1] - a
        p6[:, 2] = p1[:, 2] - a
        
        p7[:, 0] = p1[:, 0] + a
        p7[:, 1] = p1[:, 1] + a
        p7[:, 2] = p1[:, 2] - a
        
        p8[:, 0] = (-1)*p1[:, 0] 
        p8[:, 1] = p1[:, 1]
        p8[:, 2] = p1[:, 2] - a  
        # ===
        # -------XY SHEAR-----------------------
        if E_ij == 3 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = p3[:,3];                
            p4[:,3] = -p4[:,3];
            
            p5[:,3] = p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = -p8[:,3];

        # -------XZ SHEAR-----------------------
        if E_ij == 4 :     
            p2[:,3] = -p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = p4[:,3];
            
            p5[:,3] = -p5[:,3];                
            p6[:,3] = p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = -p8[:,3];


        # -------YZ SHEAR-----------------------
        if E_ij == 5 :     
            p2[:,3] = p2[:,3];
            p3[:,3] = -p3[:,3];                
            p4[:,3] = -p4[:,3];
            
            p5[:,3] = -p5[:,3];                
            p6[:,3] = -p6[:,3];
            p7[:,3] = p7[:,3];
            p8[:,3] = p8[:,3];

    # ===================================================================
    return p1, p2, p3, p4, p5, p6, p7, p8

#=========PLOTTING FROM STRESS ======================

def Plot_Shell_Elements(ax, title_name, cbar_name,norm, mapped_colors,vertices,faces):   
    
    # Create a Poly3DCollection
    poly3d = Poly3DCollection(faces, facecolors=mapped_colors, edgecolors='k', linewidths=0.0, alpha=1)
    
    # Add the collection to the plot
    ax.add_collection3d(poly3d)

    # Set the limits of the plot based on the vertices
    ax.set_xlim([vertices[:, 0].min(), vertices[:, 0].max()])
    ax.set_ylim([vertices[:, 1].min(), vertices[:, 1].max()])
    ax.set_zlim([vertices[:, 2].min(), vertices[:, 2].max()])
   
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='jet'), ax=ax)

    cbar.formatter.set_powerlimits((0, 0))
    cbar.formatter.set_useMathText(True)
    cbar.ax.set_title(cbar_name) # Set title for the colorbar
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # set axis labels and title
    ax.set_xlabel(r'$x$', fontsize = 14)
    ax.set_ylabel(r'$y$', fontsize = 14)
    ax.set_zlabel(r'$z$', fontsize = 14)
    ax.set_title(title_name, fontsize = 16, fontweight='bold')
    ax.zaxis.labelpad = 0
    ax.view_init(elev= 30, azim= 45)
    ax.set_box_aspect((1, 1, 1))
    # Set the x and y tick locators and formatters
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.zaxis.set_major_locator(MultipleLocator(0.5))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.1f'))      
        
    return ax