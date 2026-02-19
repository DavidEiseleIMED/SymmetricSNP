import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd


file_path1 = None
file_path2 = None
def get_file_path1():
    global dir_list1
    global file_path1
    file_path1= filedialog.askdirectory(title = "Select A File")
    l1 = tk.Label(root, text = "Path 1: " + str(file_path1), 
                  font=("Arial", 15)).pack()
    l1
    dir_list1 = os.listdir(file_path1)
    check_ready()

def get_file_path2():
    global dir_list2
    global file_path2
    file_path2= filedialog.askdirectory(title = "Select A File")
    print(file_path2)
    l1 = tk.Label(root, text = "Path 2: " + str(file_path2), 
                  font=("Arial", 15)).pack()
    l1
    dir_list2 = os.listdir(file_path2)
    check_ready()

def check_ready():
    if file_path1 is not None and file_path2 is not None:
        b3.config(state="normal")
        save_button.config(state="normal")

    
def import_command(dir_list, path):
    set_dict = {}
    for item in dir_list:
        if item in dir_list:
            try:
                cp = pd.read_csv(path + "/" + item + 
                                 "/annotated_variants.tab", delimiter="\t")
                cp = cp[cp['is_snp'] == True]
                set_dict[item] = set(cp['#Uploaded_variation'])
            except Exception:
                pass
    return set_dict
    
def execute_program():
    global df
    set_dict1 = import_command(dir_list1, file_path1)
    set_dict2 = import_command(dir_list2, file_path2)

    dict1 = {}
    for key1, value1 in set_dict1.items():
        dict2= {}
        for key2, value2 in set_dict2.items():
            dict2[key2] = len(value1.symmetric_difference(value2))
        dict1[key1] = dict2

    df = pd.json_normalize([{'index': k, **v} for k, v in dict1.items()])
    df = df.set_index('index')
    l1 = tk.Label(root, text = "Minimum symmetric SNP difference: " + 
                  str(df.min().min()), font=("Arial", 15)).pack()
    l2 = tk.Label(root, text = "Mean symmetric SNP-difference (rounded): " 
                  + str(int(round(df.mean().mean(), 0))), 
                  font=("Arial", 15)).pack()
    l3 = tk.Label(root, text = "Maximum symmetric SNP difference: " + 
                  str(df.max().max()), font=("Arial", 15)).pack()
    l1
    l2
    l3
    
def save_file():
    file = filedialog.asksaveasfile(title = "Save File", 
                                    defaultextension=".csv")
    if file:
        df.to_csv(file)
        
def Close():
    root.destroy()

root = tk.Tk()
root.tk.call('tk', 'scaling', 2)
root.geometry("1000x700")
root.wm_title("SymmetricSNP")
root.configure(bg="#508ca6")


b1 = tk.Button(root, text = "Select Path 1", height=2, width=20, bg='#557a90', 
               fg= "white", font=('Helvetica', '12'), 
               command = get_file_path1).pack()
b2 = tk.Button(root, text = "Select Path 2", height=2, width=20, bg='#557a90',
               fg= "white", font=('Helvetica', '12'), 
               command = get_file_path2).pack()
b3 = tk.Button(root, text = "Symmetric SNP difference: ", height=2, width=20, 
               bg='#557a90', fg= "white", font=('Helvetica', '12'),  
               command = execute_program)
b3.pack()
b3.config(state="disabled")
save_button = tk.Button(root, text="Save Matrix", height=2, width=20, 
                        bg='#557a90', fg= "white", font=('Helvetica', '12'), 
                        command=save_file)
save_button.pack()
save_button.config(state="disabled")
exit_button = tk.Button(root, text="Exit", height=2, width=20, 
                        bg='#557a90', fg= "white", font=('Helvetica', '12'), 
                        command=Close).pack()
root.mainloop()
