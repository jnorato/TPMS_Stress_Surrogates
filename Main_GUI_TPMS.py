import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('Agg')
from Surrogates_Stress import*
from Surrogates_Homogenization import*
import pandas as pd
from tkinter import filedialog, messagebox
import os
# ======Read inputs==========
def read_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")],
                                          title="Open input parameters CSV")
    if not filepath:
        return  # user canceled

    try:
        df = pd.read_csv(filepath, index_col=0)
        data = df["Value"].to_dict()

        # Set GUI values
        TPMS_var_1.set(data.get("TPMS", ""))
        Surface_var_1.set(data.get("Shell_Surface", ""))

        Traction_X_Entry_1_var.set(data.get("F_X", 0))
        Traction_Y_Entry_1_var.set(data.get("F_Y", 0))
        Traction_Z_Entry_1_var.set(data.get("F_Z", 0))
        Traction_XY_Entry_1_var.set(data.get("F_XY", 0))
        Traction_XZ_Entry_1_var.set(data.get("F_XZ", 0))
        Traction_YZ_Entry_1_var.set(data.get("F_YZ", 0))

        Thick_rho_label_1_var.set(data.get("Thick_rho_label", ""))
        Thick_rho_Entry_1_var.set(data.get("Thick_rho", 0.0))

        Poisson_Entry_1_var.set(data.get("Poisson_user", 0.3))
        Young_Entry_1_var.set(data.get("Young_user", 119000))
        Cell_Size_Entry_1_var.set(data.get("Cell_Size", 1))

        messagebox.showinfo("Loaded", f"Inputs loaded from:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
# =====Save inputs=================
def save_input_file():
    # Collect current values from Tkinter variables
    data = {
        "TPMS": TPMS_var_1.get(),
        "Shell_Surface": Surface_var_1.get(),
        "F_X": Traction_X_Entry_1_var.get(),
        "F_Y": Traction_Y_Entry_1_var.get(),
        "F_Z": Traction_Z_Entry_1_var.get(),
        "F_XY": Traction_XY_Entry_1_var.get(),
        "F_XZ": Traction_XZ_Entry_1_var.get(),
        "F_YZ": Traction_YZ_Entry_1_var.get(),
        "Thick_rho_label": Thick_rho_label_1_var.get(),
        "Thick_rho": Thick_rho_Entry_1_var.get(),
        "Poisson_user": Poisson_Entry_1_var.get(),
        "Young_user": Young_Entry_1_var.get(),
        "Cell_Size": Cell_Size_Entry_1_var.get()
    }

    # Ask user to choose save location
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")],
                                            title="Save input parameters to CSV")
    if not filepath:
        return  # User cancelled

    try:
        # Convert to DataFrame and save
        df = pd.DataFrame(list(data.items()), columns=["Parameter", "Value"])
        df.to_csv(filepath, index=False)
        messagebox.showinfo("Success", f"Inputs saved to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")
# ======Save stress==================
def save_stress_to_csv(TPMS, Shell_Surface, Unit_18):
    try:
        # Save the result to CSV
        header = ['x', 'y', 'z', 'sigma_11', 'sigma_22', 'sigma_12', 'vonMises']
        df = pd.DataFrame(Unit_18, columns=header)
        # Ask user where to save
        default_name = f"{TPMS}_Stress_On_{Shell_Surface}_Face.csv"
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile=default_name,
                                                filetypes=[("CSV files", "*.csv")])
        # Create Output folder if it doesn't exist
        output_folder = "Output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not filepath:
            return  # user cancelled

        df.to_csv(filepath, index=False)
        messagebox.showinfo("Saved", f"Stress data saved to:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save stress data:\n{e}")

# ========Save homogenization=================
def save_homogenization_to_csv(TPMS, Elasticity_Tensor):
    try:
        # Save the result to CSV
        # Create DataFrame and export        
        df = pd.DataFrame(Elasticity_Tensor)       
        # Ask user where to save
        default_name = f"{TPMS}_Elasticity_Tensor.csv"
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile=default_name,
                                                filetypes=[("CSV files", "*.csv")])
        # Create Output folder if it doesn't exist
        output_folder = "Output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not filepath:
            return  # user cancelled

        df.to_csv(filepath, index=False, header=False)
        messagebox.showinfo("Saved", f"Elasticity Tensor saved to:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Elasticity Tensor data:\n{e}")

# ===Plot and update=============
def Plot_GUI(Plot_frame_1,Plot_frame_2, frame_left, frame_right, frame_left_2, frame_right_2, frame_thick_rho, row_range):
    # Update and plot the stress
    read_input_button = tk.Button(frame_left, text="Load inputs", font=('Helvetica', font_size_1, 'bold'),
                              command=read_input_file, bg='#fff', fg='black')
    read_input_button.grid(row=1, column=0, padx=2, pady=10, sticky='sw')
    # # ==================================================
    save_input_button = tk.Button(frame_left, text="Save inputs", font=('Helvetica', font_size_1, 'bold'),
                              command=save_input_file, bg='#fff', fg='black')
    save_input_button.grid(row=1, column=1, padx=2, pady=10, sticky='sw')
    # ====

    # ===================================================
    TPMS_1 = str(TPMS_var_1.get()) # TPMS types
    Shell_Surface_1 =  str(Surface_var_1.get()) # Faces
    
    cell_size_str = Cell_Size_Entry_1_var.get().strip()
    if cell_size_str == "":
        raise ValueError("Unit cell size cannot be empty. Please enter a value.")
    Cell_Size = float(cell_size_str)
    # ====================================
    F_X = Traction_X_Entry_1_var.get() # Traction: X
    F_Y = Traction_Y_Entry_1_var.get() # Traction: Y
    F_Z = Traction_Z_Entry_1_var.get() # Traction: Z
    
    F_XY = Traction_XY_Entry_1_var.get()  # Traction: XY
    F_XZ = Traction_XZ_Entry_1_var.get()  # Traction: XZ
    F_YZ = Traction_YZ_Entry_1_var.get()  # Traction: YZ

    Thick_rho_label = str(Thick_rho_label_1_var.get()) # Label: Thickness or density
    Thick_rho_1 = Thick_rho_Entry_1_var.get() # Thickness or density
    Poisson_1 =  Poisson_Entry_1_var.get() # Poisson's ratio
    Young_1 =  Young_Entry_1_var.get() # Young's modulus
    
    
    
    # Surrogates of stress
    fig, Vonmises_max, Sigma_1_max, Sigma_2_max, Shear_max ,Density_TPMS, min_thick_rho, max_thick_rho, Unit_18 = Surrogates_Stress(TPMS_1, Shell_Surface_1, F_X, F_Y, F_Z, F_XY, F_XZ,
                                                                                             F_YZ, Thick_rho_label, Thick_rho_1, Poisson_1,Cell_Size)
    # ====Save stress
    # # Add button to exit
    save_output_button = tk.Button(frame_right, text="Save stress", font=('Helvetica', font_size_1, 'bold'),
                              command=lambda: save_stress_to_csv(TPMS_1, Shell_Surface_1, Unit_18), bg='#fff', fg='black')
    save_output_button.grid(row=1, column=3, padx=5, pady=10, sticky='sw')
    
    exit_button = tk.Button(frame_right, text="Exit", font=('Helvetica', font_size_1, 'bold'), command=root.destroy)
    exit_button.grid(row=1, column=4, padx=5, pady=10, sticky='sw')
    
    # Graphical user interfaces
    canvas = FigureCanvasTkAgg(fig, master = Plot_frame_1)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan= 10, padx=10, pady=10, sticky='nsew')

    # Display relative density
    index_row = 3
    rho_label = tk.Label(frame_right, text="Relative density:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    rho_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    rho_value = tk.Label(frame_right, text= str(Density_TPMS)  , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    rho_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_VonMises 
    index_row = index_row + 1
    vonmises_label = tk.Label(frame_right, text="Maximum von Mises stress:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    vonmises_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    vonmises_value = tk.Label(frame_right, text= str(Vonmises_max)  , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    vonmises_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_Sigma_1 
    index_row = index_row + 1
    Sigma_1_label = tk.Label(frame_right, text="Major principal stress:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    Sigma_1_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    Sigma_1_value = tk.Label(frame_right, text= str(Sigma_1_max)  , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    Sigma_1_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
     # Display Max_Sigma_2 
    index_row = index_row + 1
    Sigma_2_label = tk.Label(frame_right, text="Minor principal stress:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    Sigma_2_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    Sigma_2_value = tk.Label(frame_right, text= str(Sigma_2_max)  , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    Sigma_2_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_Shear
    index_row = index_row + 1
    shear_label = tk.Label(frame_right , text="Maximum shear stress:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nw')
    shear_value = tk.Label(frame_right, text= str(Shear_max) , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nw')      
    # ====================================================================
    Range_label = tk.Label(frame_left,  text=" Range: [" + str(min_thick_rho)+ ", "+str(max_thick_rho) + "]",
                           font=('Helvetica', font_size_1 - 2, 'bold'))
    Range_label.grid(row=row_range, column=1, padx=4, pady=10, sticky='nw') 
    #================== Homogenization ==================================
    fig, Young_Homo, Poisson_Homo, Shear_Homo, Elasticity_Tensor = Surrogates_Homogenization(TPMS_1, Density_TPMS, Poisson_1,Young_1)
    
    # ====Save Homogenization========
    save_stress_button = tk.Button(frame_right_2, text="Save Homogenization", font=('Helvetica', font_size_1, 'bold'),
                                   command=lambda: save_homogenization_to_csv(TPMS_1, Elasticity_Tensor), bg='#fff', fg='black')
    save_stress_button.grid(row=1, column=3, padx=5, pady=10, sticky="sw")
    
    exit_button = tk.Button(frame_right_2, text="Exit", font=('Helvetica', font_size_1, 'bold'), command=root.destroy)
    exit_button.grid(row=1, column=4, padx=5, pady=10, sticky='sw')

    
    # Graphical user interface
    canvas = FigureCanvasTkAgg(fig, master = Plot_frame_2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan= 10, padx=10, pady=10, sticky='nsew')                
    # TPMS
    # Update and plot the stress
    read_input_button = tk.Button(frame_left_2, text="Load inputs", font=('Helvetica', font_size_1, 'bold'),
                              command=read_input_file, bg='#fff', fg='black')
    read_input_button.grid(row=1, column=0, padx=2, pady=10, sticky='sw')
    # # ==================================================
    save_input_button = tk.Button(frame_left_2, text="Save inputs", font=('Helvetica', font_size_1, 'bold'),
                              command=save_input_file, bg='#fff', fg='black')
    save_input_button.grid(row=1, column=1, padx=2, pady=10, sticky='sw')
    # ====
    # ================================================
    # TPMS selector
    inner_row = 2

    
    TPMS_label_2 = tk.Label(frame_left_2, text='TPMS: ', font = ('Helvetica', font_size_1, 'bold'))
    TPMS_label_2.grid(row = inner_row, column=0, padx=10, pady=10, sticky="sw")
    TPMS_label_2_1 = tk.Label(frame_left_2, text=TPMS_1, font = ('Helvetica', font_size_1))
    TPMS_label_2_1.grid(row = inner_row, column=1, padx=10, pady=10, sticky="sw")

    
    # Face selector
    inner_row += 1
    Surface_label_2 = tk.Label(frame_left_2, text='' , font=('Helvetica', font_size_1))
    Surface_label_2.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")
    
    
    # # Unit cell size entry
    inner_row += 1
    Cell_Size_label_1 = tk.Label(frame_left_2, text="Unit cell size (side length):", font=('Helvetica', font_size_1, 'bold'))
    Cell_Size_label_1.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")
    
    Cell_Size_Entry_1 =tk.Label(frame_left_2, text=str(Cell_Size), font = ('Helvetica', font_size_1))
    Cell_Size_Entry_1.grid(row=inner_row, column=1, padx=10, pady=5, sticky="nw")

    # # Unit cell size entry
    inner_row += 1
    X_load = tk.Label(frame_left_2, text=" ", font=('Helvetica', font_size_1, 'bold'))
    X_load.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")
    # # Unit cell size entry
    inner_row += 1
    Y_load = tk.Label(frame_left_2, text=" ", font=('Helvetica', font_size_1, 'bold'))
    Y_load.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")
    
    # =====
    inner_row += 1
    Thick_rho_label_2 = tk.Label(frame_left_2, text='Density: ', font = ('Helvetica', font_size_1, 'bold'))
    Thick_rho_label_2.grid(row = inner_row, column=0, padx=10, pady=10, sticky="w")
    Thick_rho_label_2_1 = tk.Label(frame_left_2, text=str(Density_TPMS), font = ('Helvetica', font_size_1))
    Thick_rho_label_2_1.grid(row = inner_row, column=1, padx=10, pady=10, sticky="w")
    # =====
    inner_row += 1
    Young_label_2 = tk.Label(frame_left_2, text="Young's modulus: ", font = ('Helvetica', font_size_1, 'bold'))
    Young_label_2.grid(row = inner_row, column=0, padx=10, pady=10, sticky="w")
    Young_label_2_1 = tk.Label(frame_left_2, text=str(Young_1), font = ('Helvetica', font_size_1))
    Young_label_2_1.grid(row = inner_row, column=1, padx=10, pady=10, sticky="w")
    # =====
    inner_row += 1
    Poisson_label_2 = tk.Label(frame_left_2, text="Poisson's ratio: ", font = ('Helvetica', font_size_1, 'bold'))
    Poisson_label_2.grid(row = inner_row, column=0, padx=10, pady=10, sticky="w")
    Poisson_label_2_1 = tk.Label(frame_left_2, text=str(Poisson_1), font = ('Helvetica', font_size_1))
    Poisson_label_2_1.grid(row = inner_row, column=1, padx=10, pady=10, sticky="w")
    

    
    # Display Effective elastic parameters
    index_row = 3
    Elastic_label = tk.Label(frame_right_2, text='Effective elastic parameters', font = ('Helvetica', 12,'bold'), bg='#fff', fg='black')
    Elastic_label.grid(row=index_row, column=3, columnspan=2,padx=4, pady=10, sticky='sw')
    # Display Young modulus
    index_row = index_row + 1
    Young_label = tk.Label(frame_right_2, text="Young's modulus:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    Young_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='sw')
    Young_value = tk.Label(frame_right_2, text= str(Young_Homo) , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    Young_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='sw')       
    
    # Display Shear modulus
    index_row = index_row + 1
    Shear_label = tk.Label(frame_right_2, text="Shear's modulus:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    Shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='sw')
    Shear_value = tk.Label(frame_right_2, text= str(Shear_Homo) , font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    Shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='sw')  
    # Display Poisson's ratio  
    index_row = index_row + 1
    Poisson_label = tk.Label(frame_right_2, text="Poisson's ratio:", font = ('Helvetica', font_size_1, 'bold'), bg='#fff', fg='black')
    Poisson_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nw')
    Poisson_value = tk.Label(frame_right_2, text= str(Poisson_Homo), font = ('Helvetica', font_size_1, 'bold'), bg='#fff')
    Poisson_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nw')
    #------------------------------------------------------------------------------ 

    
    return TPMS_1, Density_TPMS, Young_1, Poisson_1
# =========================
def on_tpms_change(*args):
    Plot_GUI(tab1, tab2,  frame_left, frame_right, frame_left_2, frame_right_2, frame_thick_rho, row_range)
#------------------------------------------------------------------------------
root = tk.Tk()
root.state('zoomed')  # For Windows: maximizes the window
root.title("TPMS_Stress_Surrogates")
root.geometry("1366x768")
#------------------------------------------------------------------------------
# Create a tabbed layout
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=1)
# -----------------------------
font_size_1 = 10
font_size_2 = 15
# -----------------------------
# ========= Tab 1 for surrogates of stress =========
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Stress')
# Outer frame to contain everything in one grid cell
index_row = 0
# Create the outer frame to contain all components
frame_left = tk.Frame(tab1)
frame_left.grid(row=index_row, column=0, columnspan=2, padx=5, pady=5, sticky="nw")
# Inner row counter for frame_left
inner_row = 0
# Add input
Input_label_1 = tk.Label(frame_left, text='Inputs', font=('Helvetica', font_size_2, 'bold')) 
Input_label_1.grid(row=inner_row, column=0, columnspan=2, padx=10, pady=5, sticky="n")
# =================================================================
# Create the outer frame to contain all components
frame_right = tk.Frame(tab1)
frame_right.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky="nw")
# Add ouput
Output_label_1 = tk.Label(frame_right, text='Outputs', font=('Helvetica', font_size_2, 'bold')) 
Output_label_1.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky="n")

# ================================================
# TPMS selector
inner_row += 2
TPMS_label_1 = tk.Label(frame_left, text='TPMS: ', font=('Helvetica', font_size_1, 'bold')) 
TPMS_label_1.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")

options = ['Gyroid', 'Primitive', 'IWP']
TPMS_var_1 = tk.StringVar(tab1)
TPMS_var_1.set('Gyroid')
TPMS_option = tk.OptionMenu(frame_left, TPMS_var_1, *options)
TPMS_option.grid(row=inner_row, column=1, padx=10, pady=5, sticky="nw")

# Face selector
inner_row += 1
Surface_label_1 = tk.Label(frame_left, text='Face: ', font=('Helvetica', font_size_1, 'bold'))
Surface_label_1.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")

options = ['Top', 'Bottom']
Surface_var_1 = tk.StringVar(tab1)
Surface_var_1.set('Top')
Surface_option = tk.OptionMenu(frame_left, Surface_var_1, *options)
Surface_option.grid(row=inner_row, column=1, padx=10, pady=5, sticky="nw")

# Unit cell size entry
inner_row += 1
Cell_Size_label_1 = tk.Label(frame_left, text="Unit cell size (side length):", font=('Helvetica', font_size_1, 'bold'))
Cell_Size_label_1.grid(row=inner_row, column=0, padx=10, pady=5, sticky="nw")

Cell_Size_Entry_1_var = tk.StringVar(tab1, value="1")
Cell_Size_Entry_1 = tk.Entry(frame_left, textvariable=Cell_Size_Entry_1_var, width=10)
Cell_Size_Entry_1.grid(row=inner_row, column=1, padx=10, pady=5, sticky="nw")

# Frame for X, Y, Z entries (packed horizontally)
inner_row += 1
frame_xyz = tk.Frame(frame_left)
frame_xyz.grid(row=inner_row, column=0, columnspan=2, sticky="w", padx=10, pady=5)

Traction_X_label_1 = tk.Label(frame_xyz, text="X:", font=('Helvetica', font_size_1, 'bold'))
Traction_X_label_1.pack(side="left")
Traction_X_Entry_1_var = tk.StringVar(tab1, value="10")
Traction_X_Entry_1 = tk.Entry(frame_xyz, textvariable=Traction_X_Entry_1_var, width=10)
Traction_X_Entry_1.pack(side="left")

Traction_Y_label_1 = tk.Label(frame_xyz, text=" Y:", font=('Helvetica', font_size_1, 'bold'))
Traction_Y_label_1.pack(side="left")
Traction_Y_Entry_1_var = tk.StringVar(tab1, value="20")
Traction_Y_Entry_1 = tk.Entry(frame_xyz, textvariable=Traction_Y_Entry_1_var, width=10)
Traction_Y_Entry_1.pack(side="left")

Traction_Z_label_1 = tk.Label(frame_xyz, text=" Z:", font=('Helvetica', font_size_1, 'bold'))
Traction_Z_label_1.pack(side="left")
Traction_Z_Entry_1_var = tk.StringVar(tab1, value="30")
Traction_Z_Entry_1 = tk.Entry(frame_xyz, textvariable=Traction_Z_Entry_1_var, width=10)
Traction_Z_Entry_1.pack(side="left")

# Frame for XY, XZ, YZ entries (packed horizontally)
inner_row += 1
frame_shear = tk.Frame(frame_left)
frame_shear.grid(row=inner_row, column=0, columnspan=2, sticky="w", padx=10, pady=5)

Traction_XY_label_1 = tk.Label(frame_shear, text="XY:", font=('Helvetica', font_size_1, 'bold'))
Traction_XY_label_1.pack(side="left")
Traction_XY_Entry_1_var = tk.StringVar(tab1, value="10")
Traction_XY_Entry_1 = tk.Entry(frame_shear, textvariable=Traction_XY_Entry_1_var, width=9)
Traction_XY_Entry_1.pack(side="left")

Traction_XZ_label_1 = tk.Label(frame_shear, text=" XZ:", font=('Helvetica', font_size_1, 'bold'))
Traction_XZ_label_1.pack(side="left")
Traction_XZ_Entry_1_var = tk.StringVar(tab1, value="20")
Traction_XZ_Entry_1 = tk.Entry(frame_shear, textvariable=Traction_XZ_Entry_1_var, width=8)
Traction_XZ_Entry_1.pack(side="left")

Traction_YZ_label_1 = tk.Label(frame_shear, text=" YZ:", font=('Helvetica', font_size_1, 'bold'))
Traction_YZ_label_1.pack(side="left")
Traction_YZ_Entry_1_var = tk.StringVar(tab1, value="30")
Traction_YZ_Entry_1 = tk.Entry(frame_shear, textvariable=Traction_YZ_Entry_1_var, width=9)
Traction_YZ_Entry_1.pack(side="left")

# Frame for 'Thickness/Density', Young's modulus, and Poisson's ratio (inside frame_left)
# Make sure `inner_row` is defined and incremented properly
# --- Thickness/Density selector and entry ---
inner_row += 1
frame_thick_rho = tk.Frame(frame_left)
frame_thick_rho.grid(row=inner_row, column=0, columnspan=1, sticky="w", padx=10, pady=5)
row_range = inner_row

Thick_rho_label_1_var = tk.StringVar(tab1)
Thick_rho_label_1_var.set('Density')
Thick_rho_label_1 = tk.OptionMenu(frame_thick_rho, Thick_rho_label_1_var, 'Thickness', 'Density')
Thick_rho_label_1.pack(side="left")

Thick_rho_Entry_1_var = tk.StringVar(tab1)
Thick_rho_Entry_1_var.set('0.1')
Thick_rho_Entry_1 = tk.Entry(frame_thick_rho, textvariable=Thick_rho_Entry_1_var, width=10)
Thick_rho_Entry_1.pack(side="left")
row_range = inner_row
# --- Young's modulus ---
inner_row += 1
frame_young = tk.Frame(frame_left)
frame_young.grid(row=inner_row, column=0, columnspan=2, sticky="w", padx=10, pady=5)

Young_label_1 = tk.Label(frame_young, text="Young's modulus: ", font=('Helvetica', font_size_1, 'bold'))
Young_label_1.pack(side="left")

Young_Entry_1_var = tk.StringVar(tab1)
Young_Entry_1_var.set('119000')
Young_Entry_1 = tk.Entry(frame_young, textvariable=Young_Entry_1_var, width=10)
Young_Entry_1.pack(side="left")

# --- Poisson's ratio ---
inner_row += 1
frame_poisson = tk.Frame(frame_left)
frame_poisson.grid(row=inner_row, column=0, columnspan=2, sticky="w", padx=10, pady=5)

Poisson_label_1 = tk.Label(frame_poisson, text="Poisson's ratio: ", font=('Helvetica', font_size_1, 'bold'))
Poisson_label_1.pack(side="left")

Poisson_Entry_1_var = tk.StringVar(tab1)
Poisson_Entry_1_var.set('0.3')
Poisson_Entry_1 = tk.Entry(frame_poisson, textvariable=Poisson_Entry_1_var, width=10)
Poisson_Entry_1.pack(side="left")

# Add button to update
inner_row += 2
frame_update = tk.Frame(frame_left)
frame_update.grid(row=inner_row, column=0, columnspan=2, padx=10, pady=5)
update_button_tab1 = tk.Button(frame_update, text = 'Update and Plot', command = lambda: Plot_GUI(tab1,tab2, frame_left, frame_right,frame_left_2, frame_right_2, frame_thick_rho, row_range), font = ('Helvetica', font_size_1 + 2, 'bold'), bg='#fff', fg='black')
update_button_tab1.pack(side="left")
# Add a separator line spanning columns (adjust row and columns as needed)

# =======Create tab 2 for homogenization==================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Effective elastic properties')

# Outer frame to contain everything in one grid cell
index_row = 0
# Create the outer frame to contain all components
frame_left_2 = tk.Frame(tab2)
frame_left_2.grid(row=index_row, column=0, columnspan=2, padx=5, pady=5, sticky="nw")
# Inner row counter for frame_left
inner_row = 0
# Add input
Input_label_2 = tk.Label(frame_left_2, text='Inputs', font=('Helvetica', font_size_2, 'bold')) 
Input_label_2.grid(row=inner_row, column=0, columnspan=2, padx=10, pady=5, sticky="n")
# =================================================================
# Create the outer frame to contain all components
frame_right_2 = tk.Frame(tab2)
frame_right_2.grid(row=0, column=3, columnspan=2, padx=5, pady=5, sticky="nw")
# Add ouput
Output_label_2 = tk.Label(frame_right_2, text='Outputs', font=('Helvetica', font_size_2, 'bold')) 
Output_label_2.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky="n")

# Add button to update
# inner_row += 2
frame_update_2 = tk.Frame(frame_left_2)
frame_update_2.grid(row=12, column=0, columnspan=2, padx=10, pady=5)
update_button_tab1 = tk.Button(frame_update_2, text = 'Update and Plot', command = lambda: Plot_GUI(tab1,tab2, frame_left, frame_right,frame_left_2, frame_right_2, frame_thick_rho, row_range), font = ('Helvetica', font_size_1 + 2, 'bold'), bg='#fff', fg='black')
update_button_tab1.pack(side="left")
# Add a separator line spanning columns (adjust row and columns as needed)

# ===========Main Run=========================
TPMS_1, Density_TPMS, Young_1, Poisson_1 = Plot_GUI(tab1,tab2, frame_left, frame_right, frame_left_2, frame_right_2, frame_thick_rho, row_range)

separator = ttk.Separator(frame_left, orient='horizontal')
separator.grid(row=10, column=0, columnspan=5, sticky="ew", pady=5)

separator = ttk.Separator(frame_right, orient='horizontal')
separator.grid(row=2, column=3, columnspan=5, sticky="ew", pady=5)


separator = ttk.Separator(frame_left_2, orient='horizontal')
separator.grid(row=10, column=0, columnspan=5, sticky="ew", pady=5)

separator = ttk.Separator(frame_right_2, orient='horizontal')
separator.grid(row=2, column=3, columnspan=5, sticky="ew", pady=5)




# =========================================
# Attach callback to the StringVar (fires when value changes)
TPMS_var_1.trace_add('write', on_tpms_change)
Thick_rho_label_1_var.trace_add('write', on_tpms_change)
Cell_Size_Entry_1_var.trace_add('write', on_tpms_change)
# ----------------------------

# Make the plot_frame adjust its size when the root is resized
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(2, weight=1)
# Add button to update

# Make the plot_frame adjust its size when the root is resized
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(2, weight=1)
#------------------------------------------------------------------------------
root.mainloop()
# End



