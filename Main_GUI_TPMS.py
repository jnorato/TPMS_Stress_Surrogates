import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('Agg')
from Surrogates_Stress import*
from Surrogates_Homogenization import*
# ======Plot and update===================
import pandas as pd
from tkinter import filedialog, messagebox
import os
import pandas as pd
from tkinter import filedialog, messagebox

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

# =========================================
import pandas as pd
from tkinter import filedialog, messagebox

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
# ======
def save_stress_to_csv(TPMS, Shell_Surface, Unit_18):
    try:
        # Save the result to CSV
        header = ['x', 'y', 'z', 'sigma_11', 'sigma_22', 'sigma_12', 'vonMises']
        df = pd.DataFrame(Unit_18, columns=header)
        # Create Output folder if it doesn't exist
        
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

# =========================================
def save_homogenization_to_csv(TPMS, Elasticity_Tensor):
    try:
        # Save the result to CSV
        # Create DataFrame and export
        
        df = pd.DataFrame(Elasticity_Tensor)
        # Create Output folder if it doesn't exist
        
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

# =========================================
def Frame_Tab_1(Plot_frame_1,Plot_frame_2, row_range):
    # Update and plot the stress
    read_input_button = tk.Button(Plot_frame_1, text="Load inputs", font=('Helvetica', font_size, 'bold'),
                              command=read_input_file, bg='#eef', fg='black')
    read_input_button.grid(row=0, column=0, padx=5, pady=10, sticky="n")
    # =======
    save_input_button = tk.Button(tab1, text="Save inputs", font=('Helvetica', font_size, 'bold'),
                              command=save_input_file, bg='#efe', fg='black')
    save_input_button.grid(row=0, column=1, padx=5, pady=10, sticky="n")
    
    # ===================================================
    TPMS_1 = str(TPMS_var_1.get()) # TPMS types
    Shell_Surface_1 =  str(Surface_var_1.get()) # Faces
    Cell_Size =  Cell_Size_Entry_1_var.get() # Cell size
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
    # Define your header

    save_stress_button = tk.Button(tab1, text="Save Stress", font=('Helvetica', font_size, 'bold'),
                                   command=lambda: save_stress_to_csv(TPMS_1, Shell_Surface_1, Unit_18), bg='#fcc', fg='black')
    save_stress_button.grid(row=0, column=3, padx=5, pady=10, sticky="n")

    # Graphical user interfaces
    canvas = FigureCanvasTkAgg(fig, master = Plot_frame_1)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan= 11, padx=10, pady=10, sticky='nsew')
    
    # Display relative density
    index_row = 0
    rho_label = tk.Label(Plot_frame_1, text="Relative density:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    rho_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    rho_value = tk.Label(Plot_frame_1, text= str(Density_TPMS)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    rho_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_VonMises 
    index_row = index_row + 1
    vonmises_label = tk.Label(Plot_frame_1, text="Maximum von Mises stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    vonmises_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    vonmises_value = tk.Label(Plot_frame_1, text= str(Vonmises_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    vonmises_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_Sigma_1 
    index_row = index_row + 1
    Sigma_1_label = tk.Label(Plot_frame_1, text="Major principal stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    Sigma_1_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    Sigma_1_value = tk.Label(Plot_frame_1, text= str(Sigma_1_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    Sigma_1_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
     # Display Max_Sigma_2 
    index_row = index_row + 1
    Sigma_2_label = tk.Label(Plot_frame_1, text="Minor principal stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    Sigma_2_label.grid(row=index_row, column=3, padx=2, pady=10, sticky='sw')
    Sigma_2_value = tk.Label(Plot_frame_1, text= str(Sigma_2_max)  , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    Sigma_2_value.grid(row=index_row, column=4, padx=2, pady=10, sticky='sw')
    # Display Max_Shear
    index_row = index_row + 1
    shear_label = tk.Label(Plot_frame_1, text="Maximum shear stress:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nw')
    shear_value = tk.Label(Plot_frame_1, text= str(Shear_max) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nw')      
    # ====================================================================
    Range_label = tk.Label(Plot_frame_1, text=" (range: [" + str(min_thick_rho)+ ", "+str(max_thick_rho) + "]): ", font=('Helvetica', font_size, 'bold'))
    Range_label.grid(row=row_range+1, column=0, padx=10, pady=10, sticky="sw")    
    #================== Homogenization ==================================
    fig, Young_Homo, Poisson_Homo, Shear_Homo, Elasticity_Tensor = Surrogates_Homogenization(TPMS_1, Density_TPMS, Poisson_1,Young_1)
    
    # ====Save Homogenization
    save_stress_button = tk.Button(tab2, text="Save Homogenization", font=('Helvetica', font_size, 'bold'),
                                   command=lambda: save_homogenization_to_csv(TPMS_1, Elasticity_Tensor), bg='#fcc', fg='black')
    save_stress_button.grid(row=0, column=3, padx=5, pady=10, sticky="n")
    # Graphical user interface
    canvas = FigureCanvasTkAgg(fig, master = Plot_frame_2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, rowspan= 11, padx=10, pady=10, sticky='nsew')                
    # TPMS
    index_row = 0
    TPMS_label_2 = tk.Label(Plot_frame_2, text='TPMS: ', font = ('Helvetica', font_size, 'bold'))
    TPMS_label_2.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
    TPMS_label_2_1 = tk.Label(tab2, text=TPMS_1, font = ('Helvetica', font_size, 'bold'))
    TPMS_label_2_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
    # Display Effective elastic parameters
    index_row = 0
    Elastic_label = tk.Label(Plot_frame_2, text='Effective elastic parameters', font = ('Helvetica', 12,'bold'), bg='#fff', fg='blue')
    Elastic_label.grid(row=index_row, column=3, columnspan=2,padx=4, pady=10, sticky='sw')
    # Display Young modulus
    index_row = index_row + 1
    Young_label = tk.Label(Plot_frame_2, text="Young's modulus:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    Young_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
    Young_value = tk.Label(Plot_frame_2, text= str(Young_Homo) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    Young_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')       
    # Display Shear modulus
    index_row = index_row + 1
    Shear_label = tk.Label(Plot_frame_2, text="Shear's modulus:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    Shear_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
    Shear_value = tk.Label(Plot_frame_2, text= str(Shear_Homo) , font = ('Helvetica', font_size, 'bold'), bg='#fff')
    Shear_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')  
    # Display Poisson's ratio  
    index_row = index_row + 1
    Poisson_label = tk.Label(Plot_frame_2, text="Poisson's ratio:", font = ('Helvetica', font_size, 'bold'), bg='#fff', fg='red')
    Poisson_label.grid(row=index_row, column=3, padx=4, pady=10, sticky='nsew')
    Poisson_value = tk.Label(Plot_frame_2, text= str(Poisson_Homo), font = ('Helvetica', font_size, 'bold'), bg='#fff')
    Poisson_value.grid(row=index_row, column=4, padx=4, pady=10, sticky='nsew')
    #------------------------------------------------------------------------------ 

    
    return TPMS_1, Density_TPMS, Young_1, Poisson_1
# =========================
#------------------------------------------------------------------------------
root = tk.Tk()
root.state('zoomed')  # For Windows: maximizes the window
root.title("TPMS_UConn_Project")
root.geometry("1366x768")
#------------------------------------------------------------------------------
# Create a tabbed layout
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=1)
# -----------------------------
font_size = 10
font_size_2 = 8
# -----------------------------
# ========= Tab 1 for surrogates of stress =========
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Stress')
# Label for TPMS
index_row = 0
TPMS_label_1 = tk.Label(tab1, text='TPMS: ', font = ('Helvetica', font_size, 'bold'))
TPMS_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
options = ['Gyroid', 'Primitive', 'IWP']
TPMS_var_1 = tk.StringVar(tab1)
TPMS_var_1.set('Gyroid')
TPMS_option = tk.OptionMenu(tab1, TPMS_var_1, *options)
TPMS_option.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
# Label for BOTTOM and TOP faces
index_row = index_row + 1
Surface_label_1 = tk.Label(tab1, text='Face: ', font = ('Helvetica', font_size, 'bold'))
Surface_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
options = ['Top', 'Bottom']
Surface_var_1 = tk.StringVar(tab1)
Surface_var_1.set('Top')
Surface_option = tk.OptionMenu(tab1, Surface_var_1, *options)
Surface_option.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
# Label for cell size
index_row = index_row + 1
Cell_Size_label_1 = tk.Label(tab1, text="Unit cell size (side length): ", font = ('Helvetica', font_size, 'bold'))
Cell_Size_label_1.grid(row= index_row, column=0, padx=10, pady=10, sticky="sw")
Cell_Size_Entry_1_var = tk.StringVar(tab1)
Cell_Size_Entry_1_var.set('1')  # Default value for A1
Cell_Size_Entry_1 = tk.Entry(tab1, textvariable = Cell_Size_Entry_1_var, width=10)
Cell_Size_Entry_1.grid(row= index_row, column=1, padx=10, pady=10, sticky="sw")
# Label for traction: X, Y, Z, XY, YZ, XZ 
index_row = index_row + 1
Tractions_label_1 = tk.Label(tab1, text="Tractions:", font = ('Helvetica', font_size, 'bold'))
Tractions_label_1.grid(row= index_row, column=0, padx=10, pady=10, sticky="sw")

# Merger X Y Z
index_row = index_row + 1
frame_x = tk.Frame(tab1)
frame_x.grid(row=index_row, column=0, columnspan=2, padx=5, pady=5, sticky="w")
# X
Traction_X_label_1 = tk.Label(frame_x, text="X: ", font=('Helvetica', font_size, 'bold'))
Traction_X_label_1.pack(side="left")
Traction_X_Entry_1_var = tk.StringVar(tab1)
Traction_X_Entry_1_var.set(str(10))
Traction_X_Entry_1 = tk.Entry(frame_x, textvariable=Traction_X_Entry_1_var, width=10)
Traction_X_Entry_1.pack(side="left")
# Y
Traction_Y_label_1 = tk.Label(frame_x, text=" Y: ", font=('Helvetica', font_size, 'bold'))
Traction_Y_label_1.pack(side="left")
Traction_Y_Entry_1_var = tk.StringVar(tab1)
Traction_Y_Entry_1_var.set(str(20))
Traction_Y_Entry_1 = tk.Entry(frame_x, textvariable=Traction_Y_Entry_1_var, width=10)
Traction_Y_Entry_1.pack(side="left")
# Z
Traction_Z_label_1 = tk.Label(frame_x, text=" Z: ", font=('Helvetica', font_size, 'bold'))
Traction_Z_label_1.pack(side="left")
Traction_Z_Entry_1_var = tk.StringVar(tab1)
Traction_Z_Entry_1_var.set(str(30))
Traction_Z_Entry_1 = tk.Entry(frame_x, textvariable=Traction_Z_Entry_1_var, width=10)
Traction_Z_Entry_1.pack(side="left")

# Merger XY YZ XZ
index_row = index_row +1
frame_xy = tk.Frame(tab1)
# XY
frame_xy.grid(row=index_row, column=0, columnspan=2, padx=5, pady=5, sticky="w")
Traction_XY_label_1 = tk.Label(frame_xy, text="XY: ", font=('Helvetica', font_size, 'bold'))
Traction_XY_label_1.pack(side="left")
Traction_XY_Entry_1_var = tk.StringVar(tab1)
Traction_XY_Entry_1_var.set(str(10))
Traction_XY_Entry_1 = tk.Entry(frame_xy, textvariable=Traction_XY_Entry_1_var, width=9)
Traction_XY_Entry_1.pack(side="left")
# XZ
Traction_XZ_label_1 = tk.Label(frame_xy, text=" XZ: ", font=('Helvetica', font_size, 'bold'))
Traction_XZ_label_1.pack(side="left")
Traction_XZ_Entry_1_var = tk.StringVar(tab1)
Traction_XZ_Entry_1_var.set(str(20))
Traction_XZ_Entry_1 = tk.Entry(frame_xy, textvariable=Traction_XZ_Entry_1_var, width=8)
Traction_XZ_Entry_1.pack(side="left")
# YZ
Traction_YZ_label_1 = tk.Label(frame_xy, text=" YZ: ", font=('Helvetica', font_size, 'bold'))
Traction_YZ_label_1.pack(side="left")
Traction_YZ_Entry_1_var = tk.StringVar(tab1)
Traction_YZ_Entry_1_var.set(str(30))
Traction_YZ_Entry_1 = tk.Entry(frame_xy, textvariable=Traction_YZ_Entry_1_var, width=9)
Traction_YZ_Entry_1.pack(side="left")

# Label for Thickness or Density
index_row = index_row + 1
row_range=index_row
options = ['Thickness', 'Density']
Thick_rho_label_1_var = tk.StringVar(tab1)
Thick_rho_label_1_var.set('Density')
Thick_rho_label_1 = tk.OptionMenu(tab1, Thick_rho_label_1_var, *options)
Thick_rho_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")

# Entry to enter thickness or density
index_row = index_row + 1
Thick_rho_Entry_1_var = tk.StringVar(tab1)
Thick_rho_Entry_1_var.set('0.1')  # Default value for A1
Thick_rho_Entry_1 = tk.Entry(tab1, textvariable = Thick_rho_Entry_1_var, width=10)
Thick_rho_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
# Entry to enter Young's modulus
index_row = index_row + 1
Young_label_1 = tk.Label(tab1, text="Young's modulus: ", font = ('Helvetica', font_size, 'bold'))
Young_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Young_Entry_1_var = tk.StringVar(tab1)
Young_Entry_1_var.set('119000')  # Default value for A1
Young_Entry_1 = tk.Entry(tab1, textvariable = Young_Entry_1_var, width=10)
Young_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")
# Entry to enter Poisson's ratio
index_row = index_row + 1
Poisson_label_1 = tk.Label(tab1, text="Poisson's ratio: ", font = ('Helvetica', font_size, 'bold'))
Poisson_label_1.grid(row = index_row, column=0, padx=10, pady=10, sticky="sw")
Poisson_Entry_1_var = tk.StringVar(tab1)
Poisson_Entry_1_var.set('0.3')  # Default value for A1
Poisson_Entry_1 = tk.Entry(tab1, textvariable = Poisson_Entry_1_var, width=10)
Poisson_Entry_1.grid(row = index_row, column=1, padx=10, pady=10, sticky="sw")

# =======Create tab 2 for homogenization==================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Effective elastic properties')
font_size = 10
# ===========Main Run=========================
TPMS_1, Density_TPMS, Young_1, Poisson_1 = Frame_Tab_1(tab1,tab2,row_range)
# Add button to update
update_button_tab1 = tk.Button(tab1, text = 'Update and Plot', command = lambda: Frame_Tab_1(tab1,tab2,row_range), font = ('Helvetica', font_size + 2, 'bold'), bg='#fff', fg='red')
update_button_tab1.grid(row = 0, column = 0, columnspan=2, padx = 20, pady = 10)
# Add button to exit
exit_button = tk.Button(tab1, text="Exit", font=('Helvetica', font_size, 'bold'), command=root.destroy)
exit_button.grid(row=0, column=4, padx=5, pady=10, sticky="n")
# ----------------------------
# Make the plot_frame adjust its size when the root is resized
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(2, weight=1)
# Add button to update
update_button_tab2 = tk.Button(tab2, text = 'Update and Plot', command = lambda: Frame_Tab_1(tab1,tab2,row_range), font = ('Helvetica', font_size + 2, 'bold'), bg='#fff', fg='red')
update_button_tab2.grid(row = 0, column = 0, columnspan=2, padx = 20, pady = 10)
# Add button to exit
exit_button = tk.Button(tab2, text="Exit", font=('Helvetica', font_size, 'bold'), command=root.destroy)
exit_button.grid(row=0, column=4, padx=5, pady=10, sticky="n")
# Make the plot_frame adjust its size when the root is resized
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(2, weight=1)
#------------------------------------------------------------------------------
root.mainloop()
# End



