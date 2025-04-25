import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('Agg')
from Surrogates_Stress import*
from Surrogates_Homogenization import*
# =========================
def Frame_Tab_1(Plot_frame):
    try:
        TPMS_1 = str(TPMS_var_1.get())
        Shell_Surface_1 =  str(Surface_var_1.get())
        Cell_Size =  Cell_Size_Entry_1_var.get()
        F_X = Traction_X_Entry_1_var.get()
        F_Y = Traction_Y_Entry_1_var.get()
        F_Z = Traction_Z_Entry_1_var.get()
        
        F_XY = Traction_XY_Entry_1_var.get()
        F_XZ = Traction_XZ_Entry_1_var.get()
        F_YZ = Traction_YZ_Entry_1_var.get()


        Thickness_1 = Thickness_Entry_1_var.get()
        Poisson_1 =  Poisson_Entry_1_var.get()
        
        fig, Density_TPMS, Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max = Surrogates_Stress(TPMS_1, Shell_Surface_1, F_X, F_Y, F_Z, F_XY, F_XZ, F_YZ, Thickness_1, Poisson_1,Cell_Size)

        canvas = FigureCanvasTkAgg(fig, master = Plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan= 11, padx=10, pady=10, sticky='nsew')
        
        # Display relative density
        index_row = 0
        rho_label = tk.Label(Plot_frame, text="Relative density:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        rho_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
        rho_value = tk.Label(Plot_frame, text= str(np.round(Density_TPMS,3))  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        rho_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
        # Display Max_VonMises 
        index_row = index_row + 1
        vonmises_label = tk.Label(Plot_frame, text="Maximum von Mises stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        vonmises_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
        vonmises_value = tk.Label(Plot_frame, text= str(Vonmises_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        vonmises_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
        # Display Max_Sigma_1 
        index_row = index_row + 1
        Sigma_1_label = tk.Label(Plot_frame, text="Maximum major stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        Sigma_1_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
        Sigma_1_value = tk.Label(Plot_frame, text= str(Sigma_1_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        Sigma_1_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
         # Display Max_Sigma_2 
        index_row = index_row + 1
        Sigma_2_label = tk.Label(Plot_frame, text="Maximum minor stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        Sigma_2_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
        Sigma_2_value = tk.Label(Plot_frame, text= str(Sigma_2_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        Sigma_2_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
        # Display Max_Shear
        index_row = index_row + 1
        shear_label = tk.Label(Plot_frame, text="Maximum shear stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nw')
        shear_value = tk.Label(Plot_frame, text= str(Shear_max) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nw')        
        
    except ValueError:
        print("Invalid inputs. Please enter valid inputs.")
# =========================
def Frame_Tab_2(Plot_frame):
    try:
        TPMS_2 = str(TPMS_var_2.get())

        Density_2 = Density_Entry_2_var.get()
        Poisson_2 =  Poisson_Entry_2_var.get()
        Young_2 =  Young_Entry_2_var.get()
        fig, Young, Poisson ,Shear = Surrogates_Homogenization(TPMS_2, Density_2, Poisson_2,Young_2)

        canvas = FigureCanvasTkAgg(fig, master = Plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan= 11, padx=10, pady=10, sticky='nsew')
                
        # # Display Traction
        # Display Thickness
        index_row = 0
        Elastic_label = tk.Label(Plot_frame, text='Effective elastic parameters', font = ('Helvetica', 12,'bold'), bg='#fff', fg='blue')
        Elastic_label.grid(row=index_row, column=3, columnspan=2,padx=4, pady=10, sticky='sw')
        # Display Young modulus
        index_row = index_row + 1
        Young_label = tk.Label(Plot_frame, text="Young's modulus:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        Young_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
        Young_value = tk.Label(Plot_frame, text= str(Young) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        Young_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')       
        # Display Shear modulus
        index_row = index_row + 1
        Shear_label = tk.Label(Plot_frame, text="Shear's modulus:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        Shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
        Shear_value = tk.Label(Plot_frame, text= str(Shear) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
        Shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')  
        # Display Poisson's ratio  
        index_row = index_row + 1
        Poisson_label = tk.Label(Plot_frame, text="Poisson's ratio:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
        Poisson_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
        Poisson_value = tk.Label(Plot_frame, text= str(Poisson), font = ('Helvetica', font_size, 'bold'), bg='#fff')
        Poisson_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')     
        
    except ValueError:
        print("Invalid inputs. Please enter valid inputs.")

#------------------------------------------------------------------------------
root = tk.Tk()
root.title("TPMS_UConn_Project")
root.geometry("1366x768")
#------------------------------------------------------------------------------
# Create a tabbed layout
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=1)
#------------------------------------------------------------------------------
# Create tabs

tab1 = ttk.Frame(notebook)

notebook.add(tab1, text='Stress')
font_size = 10

#================== Widgets for Tab 2 ==================================
index_row = 0
TPMS_label_1 = tk.Label(tab1, text='TPMS: ', font = ('Helvetica', font_size, 'bold'))
TPMS_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
options = ['Gyroid', 'Primitive', 'IWP']
TPMS_var_1 = tk.StringVar(tab1)
TPMS_var_1.set('Gyroid')
TPMS_option = tk.OptionMenu(tab1, TPMS_var_1, *options)
TPMS_option.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Surface_label_1 = tk.Label(tab1, text='Faces: ', font = ('Helvetica', font_size, 'bold'))
Surface_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
options = ['Top', 'Bottom']
Surface_var_1 = tk.StringVar(tab1)
Surface_var_1.set('Top')
Surface_option = tk.OptionMenu(tab1, Surface_var_1, *options)
Surface_option.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
# ------------------------------------------------------------------------------
index_row = index_row + 1
Cell_Size_label_1 = tk.Label(tab1, text="Unit cell size (side length): ", font = ('Helvetica', font_size, 'bold'))
Cell_Size_label_1.grid(row= index_row, column=0, padx=10, pady=10, sticky="sw")
Cell_Size_Entry_1_var = tk.StringVar(tab1)
Cell_Size_Entry_1_var.set('1')  # Default value for A1
Cell_Size_Entry_1 = tk.Entry(tab1, textvariable = Cell_Size_Entry_1_var)
Cell_Size_Entry_1.grid(row= index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Traction_X_label_1 = tk.Label(tab1, text="Traction X: ", font = ('Helvetica', font_size, 'bold'))
Traction_X_label_1.grid(row= index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_X_Entry_1_var = tk.StringVar(tab1)
Traction_X_Entry_1_var.set(str(10))  # Default value for A1
Traction_X_Entry_1 = tk.Entry(tab1, textvariable = Traction_X_Entry_1_var)
Traction_X_Entry_1.grid(row= index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
index_row = index_row + 1
Traction_Y_label_1 = tk.Label(tab1, text="Traction Y: ", font = ('Helvetica', font_size, 'bold'))
Traction_Y_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_Y_Entry_1_var = tk.StringVar(tab1)
Traction_Y_Entry_1_var.set(str(10))  # Default value for A1
Traction_Y_Entry_1 = tk.Entry(tab1, textvariable = Traction_Y_Entry_1_var)
Traction_Y_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Traction_Z_label_1 = tk.Label(tab1, text="Traction Z: ", font = ('Helvetica', font_size, 'bold'))
Traction_Z_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_Z_Entry_1_var = tk.StringVar(tab1)
Traction_Z_Entry_1_var.set(str(10))  # Default value for A1
Traction_Z_Entry_1 = tk.Entry(tab1, textvariable = Traction_Z_Entry_1_var)
Traction_Z_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Traction_XY_label_1 = tk.Label(tab1, text="Traction XY: ", font = ('Helvetica', font_size, 'bold'))
Traction_XY_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_XY_Entry_1_var = tk.StringVar(tab1)
Traction_XY_Entry_1_var.set(str(10))  # Default value for A1
Traction_XY_Entry_1 = tk.Entry(tab1, textvariable = Traction_XY_Entry_1_var)
Traction_XY_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Traction_XZ_label_1 = tk.Label(tab1, text="Traction XZ: ", font = ('Helvetica', font_size, 'bold'))
Traction_XZ_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_XZ_Entry_1_var = tk.StringVar(tab1)
Traction_XZ_Entry_1_var.set(str(10))  # Default value for A1
Traction_XZ_Entry_1 = tk.Entry(tab1, textvariable = Traction_XZ_Entry_1_var)
Traction_XZ_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Traction_YZ_label_1 = tk.Label(tab1, text="Traction YZ: ", font = ('Helvetica', font_size, 'bold'))
Traction_YZ_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Traction_YZ_Entry_1_var = tk.StringVar(tab1)
Traction_YZ_Entry_1_var.set(str(10))  # Default value for A1
Traction_YZ_Entry_1 = tk.Entry(tab1, textvariable = Traction_YZ_Entry_1_var)
Traction_YZ_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Thickness_label_1 = tk.Label(tab1, text="Thickness: ", font = ('Helvetica', font_size, 'bold'))
Thickness_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Thickness_Entry_1_var = tk.StringVar(tab1)
Thickness_Entry_1_var.set('0.1')  # Default value for A1
Thickness_Entry_1 = tk.Entry(tab1, textvariable = Thickness_Entry_1_var)
Thickness_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")

#--------------------------------------------------------------------------
index_row = index_row + 1
Young_label_1 = tk.Label(tab1, text="Young's modulus: ", font = ('Helvetica', font_size, 'bold'))
Young_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Young_Entry_1_var = tk.StringVar(tab1)
Young_Entry_1_var.set('119000')  # Default value for A1
Young_Entry_1 = tk.Entry(tab1, textvariable = Young_Entry_1_var)
Young_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
index_row = index_row + 1
Poisson_label_1 = tk.Label(tab1, text="Poisson's ratio: ", font = ('Helvetica', font_size, 'bold'))
Poisson_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Poisson_Entry_1_var = tk.StringVar(tab1)
Poisson_Entry_1_var.set('0.3')  # Default value for A1
Poisson_Entry_1 = tk.Entry(tab1, textvariable = Poisson_Entry_1_var)
Poisson_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
Frame_Tab_1(tab1)
#------------------------------------------------------------------------------
update_button_tab1 = tk.Button(tab1, text = 'Update and Plot', command = lambda: Frame_Tab_1(tab1), font = ('Helvetica', font_size + 2, 'bold'), bg='#fff', fg='red')
update_button_tab1.grid(row = 0, column = 0, columnspan=2, padx = 20, pady = 10)
#------------------------------------------------------------------------------
# Make the plot_frame adjust its size when the root is resized
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(2, weight=1)
#------------------------------------------------------------------------------
# Create tabs
# ===============================================================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Effective elastic properties')
font_size = 10
#================== Widgets for Tab 2 ==================================
index_row = 0
TPMS_label_2 = tk.Label(tab2, text='TPMS: ', font = ('Helvetica', font_size, 'bold'))
TPMS_label_2.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
options = ['Gyroid', 'Primitive', 'IWP']
TPMS_var_2 = tk.StringVar(tab2)
TPMS_var_2.set('Gyroid')
TPMS_option = tk.OptionMenu(tab2, TPMS_var_2, *options)
TPMS_option.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#------------------------------------------------------------------------------
index_row = index_row + 1
Density_label_2 = tk.Label(tab2, text="Density: ", font = ('Helvetica', font_size, 'bold'))
Density_label_2.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Density_Entry_2_var = tk.StringVar(tab2)
Density_Entry_2_var.set('0.1')  # Default value for A1
Density_Entry_2 = tk.Entry(tab2, textvariable = Density_Entry_2_var)
Density_Entry_2.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
index_row = index_row + 1
Young_label_2 = tk.Label(tab2, text="Young's modulus: ", font = ('Helvetica', font_size, 'bold'))
Young_label_2.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Young_Entry_2_var = tk.StringVar(tab2)
Young_Entry_2_var.set('119000')  # Default value for A1
Young_Entry_2 = tk.Entry(tab2, textvariable = Young_Entry_2_var)
Young_Entry_2.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
index_row = index_row + 1
Poisson_label_2 = tk.Label(tab2, text="Poisson's ratio: ", font = ('Helvetica', font_size, 'bold'))
Poisson_label_2.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Poisson_Entry_2_var = tk.StringVar(tab2)
Poisson_Entry_2_var.set('0.3')  # Default value for A1
Poisson_Entry_2 = tk.Entry(tab2, textvariable = Poisson_Entry_2_var)
Poisson_Entry_2.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
#--------------------------------------------------------------------------
Frame_Tab_2(tab2)
#------------------------------------------------------------------------------
update_button_tab2 = tk.Button(tab2, text = 'Update', command = lambda: Frame_Tab_2(tab2), font = ('Helvetica', font_size + 2, 'bold'), bg='#fff', fg='red')
update_button_tab2.grid(row = 0, column = 0, columnspan=2, padx = 20, pady = 10)
#------------------------------------------------------------------------------
# Make the plot_frame adjust its size when the root is resized
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(2, weight=1)
#------------------------------------------------------------------------------

#--------------------------------------------------
root.mainloop()



