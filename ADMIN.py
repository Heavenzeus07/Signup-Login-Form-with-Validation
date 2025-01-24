import customtkinter as ctk
import sys
import tkinter
from tkinter import ttk
import openpyxl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import subprocess
from FORM import GeneratedForm
import json
ctk.set_appearance_mode("light")

def toggle_access():
    config_path = "config.json"
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        # If the file is empty or not valid JSON, create an initial configuration
        config = {"access_enabled": False}

    if config["access_enabled"]:
        config["access_enabled"] = False
        enable_button.configure(text="Enable Form Access")
    else:
        config["access_enabled"] = True
        enable_button.configure(text="Disable Form Access")

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)

def enable_access():
    config_path = "config.json"
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        # If the file is empty or not valid JSON, create an initial configuration
        config = {"access_enabled": False}

    config["access_enabled"] = True

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)

def disable_access():
    config_path = "config.json"
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        # If the file is empty or not valid JSON, create an initial configuration
        config = {"access_enabled": False}

    config["access_enabled"] = False

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)


def load(my_tag):
    list_values = list(sheet.values)
    #print(list_values)
    for col_name in list_values[0]:
        treeview.heading(col_name,text=col_name)
    for index, row in data.iterrows():
        my_tag = 'oddrow' if my_tag=='evenrow'else 'evenrow'
        treeview.insert("", "end", values=(row['Unique id'] ,row['First Name'], row['Last Name'], row['Title'],row["Guardian's Name"],
                                           row['Age'], row['Date of Birth'], row['Address'],row["Mobile No."],
                                           row['Email id'], row['Gender'], row['Religion'],row["Caste"],
                                           row['Department'], row['Year'], row['Semester'],row["Terms Accepted"],),tags=(my_tag))
        #my_tag = 'oddrow' if my_tag=='evenrow'else 'evenrow'
        #treeview.insert('',tkinter.END,values=value_tuple,tags=(my_tag))

def count_dept(path,  column_name2):
    df = pd.read_excel(path)
    return df[column_name2].value_counts()

def count_year(path,  column_name1):
    df = pd.read_excel(path)
    return df[column_name1].value_counts()

def update_bar1():
    year_counts = count_year(path, column_name1)
    year = {}
    for element, count in year_counts.items():
    #print(f"{element}: {count}")
        year[element] = count
    
    fig1, ax1 = plt.subplots(figsize = (4,3))
    ax1.clear()
    ax1.bar(year.keys(), year.values())
    ax1.set_title("Year")
    #ax1.set_xlabel("Year")
    ax1.set_ylabel("No. of students")
    #plt.show()
    canvas1 = FigureCanvasTkAgg(fig1, mat_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0,column=0,padx=15,pady=(15,7.5),sticky = "news")
    
def update_bar2():
    dept_counts = count_dept(path, column_name2)
    dept = {}
    for element, count in dept_counts.items():
        #print(f"{element}: {count}")
        dept[element] = count
    
    fig2, ax3 = plt.subplots(figsize = (4,3))
    ax3.clear()
    ax3.pie(dept.values(), labels=dept.keys(), autopct='%1.1f%%')
    ax3.set_title("Department")
    # plt.show()
    canvas2 = FigureCanvasTkAgg(fig2, mat_frame)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row = 1,column=0,padx=15,pady=(7.5,15),sticky = "news")


def filter_data(*args):
    search_text = search_var.get().lower()
    treeview.delete(*treeview.get_children())
    data= pd.read_excel(path)
    filtered_data = data[(data['First Name'].str.lower().str.contains(search_text, na=False))|(data['Unique id'].astype(str).str.contains(search_text,na = False))]
    
    list_values = list(sheet.values)
    #print(list_values)
    for col_name in list_values[0]:
        treeview.heading(col_name,text=col_name)
    
    treeview.tag_configure('oddrow',background="#EBF8FF")
    treeview.tag_configure('evenrow',background="#E3CBB1")
    my_tag = 'evenrow'

    for index, row in filtered_data.iterrows():
        my_tag = 'oddrow' if my_tag=='evenrow'else 'evenrow'
        treeview.insert("", "end", values=(row['Unique id'],row['First Name'], row['Last Name'], row['Title'],row["Guardian's Name"],
                                           row['Age'], row['Date of Birth'], row['Address'],row["Mobile No."],
                                           row['Email id'], row['Gender'], row['Religion'],row["Caste"],
                                           row['Department'], row['Year'], row['Semester'],row["Terms Accepted"]),tags=(my_tag))
def load_data(my_tag):
    #treeview.delete(*treeview.get_children())
    data= pd.read_excel(path)
    for index , row in data.iterrows():
        my_tag = 'oddrow' if my_tag=='evenrow'else 'evenrow'
        treeview.insert("", "end", values=(row ['Unique id'],row['First Name'], row['Last Name'], row['Title'],row["Guardian's Name"],
                                           row['Age'], row['Date of Birth'], row['Address'],row["Mobile No."],
                                           row['Email id'], row['Gender'], row['Religion'],row["Caste"],
                                           row['Department'], row['Year'], row['Semester'],row["Terms Accepted"]),tags=(my_tag))
def refresh():
    #data= pd.read_excel(path)
    treeview.delete(*treeview.get_children())
    '''
    for index , row in data.iterrows():
        my_tag = 'oddrow' if my_tag=='evenrow'else 'evenrow'
        treeview.insert("", "end", values=(row ['Unique id'],row['First Name'], row['Last Name'], row['Title'],row["Guardian's Name"],
                                           row['Age'], row['Date of Birth'], row['Address'],row["Mobile No."],
                                           row['Email id'], row['Gender'], row['Religion'],row["Caste"],
                                           row['Department'], row['Year'], row['Semester'],row["Terms Accepted"]),tags=(my_tag))'''
    load_data(my_tag)                                       
    update_bar1()
    update_bar2()
        
# ("First Name","Last Name","Title","Guardian's Name","Age","Date of Birth","Address","Mobile No."
#,"Email id","Gender","Religion","Caste","Department","Year","Semester","Terms Accepted")

path = "students.xlsx"
data = pd.read_excel(path)
workbook = openpyxl.load_workbook(path)
sheet = workbook.active

column_name1 = 'Year'
column_name2 = 'Department'

plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#2F5E87", "#EBF8FF", "#6DA5C0", "#E3CBB1", "#FEFEFE"])

        

window = ctk.CTkToplevel()
#window = tkinter.Toplevel()
window.title("SSRS & Company")
window.state('zoomed')
window.config(bg="#EBF8FF")
style = ttk.Style(window)
style.theme_use('clam')

my_image = ctk.CTkImage(light_image=Image.open("STCET-Logo.png"),size = (70,70))

# Create a CTkLabel with the CTkImage
p_label = ctk.CTkLabel(window, image=my_image, text=" ",bg_color="#EBF8FF")
p_label.pack(padx=20, pady=5)

college_label = ctk.CTkLabel(window,text="St. Thomas' College of Engineering & Technology",
                             font=ctk.CTkFont(family = "Old English Text MT",size=30,weight="bold"),bg_color = "#EBF8FF",text_color="#264D61")
college_label.pack(padx = 10,pady =5)
title_label = ctk.CTkLabel(window,text="Admin Page",font=ctk.CTkFont(family = "Arial",size=25,weight = "bold"),bg_color = "#EBF8FF",text_color="#264D61")
title_label.pack(padx = 10,pady =5)

frame = ctk.CTkFrame(window,fg_color="#FEFEFE",bg_color="#EBF8FF",corner_radius=15,border_width=2,border_color="#264D61")
frame.pack(fill = "x",padx = 100,pady = (5,10))

tree_label = ctk.CTkLabel(frame,text="Data Sheet of Students Information",font=ctk.CTkFont(family = "Arial",size=25,weight = "bold"),text_color="#264D61")
tree_label.grid(row = 0,column = 1,padx = 5,pady = (10,5),sticky = "news")

#search frame.......

search_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
search_frame.grid(row = 1,column = 1,padx = (10,20),pady = (10,10),sticky = "news")

search_label = ctk.CTkLabel(search_frame,text="Search by First Name/Unique id   :",font=ctk.CTkFont(family = "Arial",size=15,weight = "bold"),text_color="#264D61")
search_label.pack(side =tkinter.LEFT, padx=(10,5),pady = 10)

search_var = tkinter.StringVar()
search_entry = ctk.CTkEntry(search_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#264D61",textvariable=search_var,
                          font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),height = 30,corner_radius = 15)
search_entry.pack(side = tkinter.LEFT,padx = (5,10),pady = 10,fill = "x",expand = True)

refresh_button = ctk.CTkButton(search_frame, text="Refresh",width=150, command=refresh,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
refresh_button.pack(side = tkinter.LEFT,padx = (5,10),pady = 10)


treeFrame = ttk.Frame(frame)
treeFrame.grid(row=2,column=1,pady=(10,10),padx=(10,20),sticky = "news")
treescy = ttk.Scrollbar(treeFrame,orient = 'vertical')
treescy.pack(side="right",fill="y")
#treescx = ttk.Scrollbar(treeFrame,orient='horizontal')
#treescx.pack(side="bottom",fill="x")

cols = ("Unique id","First Name","Last Name","Title","Guardian's Name","Age","Date of Birth","Address","Mobile No."
        ,"Email id","Gender","Religion","Caste","Department","Year","Semester","Terms Accepted")
treeview = ttk.Treeview(treeFrame,show="headings",yscrollcommand=treescy.set,columns=cols,height=18)
for col in cols:
    treeview.column(col,width=58)
treeview.pack(fill = "x")
treescy.config(command=treeview.yview)
#add style........

style.configure("Treeview",background = "#EBF8FF",fieldbackground ="#EBF8FF",foreground = "#264D61",rowheight = 25)
style.configure("Treeview.Heading",background ="#264D61",foreground = "#E3CBB1",hover = "#2F5E87")
style.map('Treeview',background = ([('selected',"#2F5E87")]))
style.configure("Vertical.TScrollbar",background = "#264D61",troughcolor ="#EBF8FF"  )
treeview.tag_configure('oddrow',background="#EBF8FF")
treeview.tag_configure('evenrow',background="#E3CBB1")
my_tag = 'evenrow'

load(my_tag)
search_entry.bind("<KeyRelease>", filter_data)
#treescx.config(command=treeview.xview)

mat_label = ctk.CTkLabel(frame,text="Dashboard",font=ctk.CTkFont(family = "Arial",size=25,weight = "bold"),text_color="#264D61")
mat_label.grid(row = 0,column = 0,padx = (20,10),pady = (10,5),sticky = "news")

mat_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
mat_frame.grid(row = 1,column = 0,rowspan = 3,sticky = "news",padx = (20,10),pady = (10,20))

update_bar1()
update_bar2()

for i in range(2):
    mat_frame.grid_rowconfigure(i,weight=1)
for i in range(1):
    mat_frame.grid_columnconfigure(i,weight=1)

button_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
button_frame.grid(row = 3,column = 1,padx = (10,20),pady = (10,20),sticky = "news")

def open_generated_form():
    # Run the form_generator.py script to generate the form
    subprocess.Popen(['python', 'FORM.py'], shell=True)

    
    
Edit_button = ctk.CTkButton(button_frame, text="Fill Form", command=open_generated_form,fg_color="#264D61",
                            hover_color="#2F5E87",height = 30,corner_radius = 15)
Edit_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="news")

def open_excel_sheet():
    subprocess.Popen(['start', 'excel', path], shell=True)

Excel_button = ctk.CTkButton(button_frame, text="View Excel Sheet", command=open_excel_sheet,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
Excel_button.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="news")

# Add buttons to enable and disable access
enable_button = ctk.CTkButton(button_frame, text="Disable Form Access", command=toggle_access,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
enable_button.grid(row=0, column=2, padx=(5, 5), pady=10, sticky="news")

#edit buttons.........

def remove_all():
    data= pd.read_excel(path)
    for item in treeview.get_children():
        treeview.delete(item)
        
    data.drop(data.index,inplace=True)
    data.to_excel(path,index=False)
    refresh()

remove_all_button = ctk.CTkButton(button_frame, text="Remove All",command=remove_all,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
remove_all_button.grid(row=0, column=3, padx=(5, 5), pady=10, sticky="news")

def remove_row():
    data= pd.read_excel(path)
    selected_item = treeview.selection()
    for item in selected_item:
        values = treeview.item(item,"values")
        if values:
            item_text = values[1]
            index_to_remove = data[data['First Name']==item_text].index[0]
            data.drop(index_to_remove,inplace=True)
            treeview.delete(item)
            data.to_excel(path,index=False)
            
        else:
            treeview.delete(item)
            data.to_excel(path,index=False)
    refresh()
def exit_action():
        confirm = tkinter.messagebox.askyesno("Return", "Are you sure you want to return to login page?")
        if confirm:
            window.destroy()
            sys.exit()
    

remove_rows_button = ctk.CTkButton(button_frame, text="Remove One or More", command=remove_row,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
remove_rows_button.grid(row=0, column=4, padx=(5, 5), pady=10, sticky="news")

exit_button = ctk.CTkButton(button_frame,text="Return",command=exit_action,fg_color="#264D61",hover_color="#2F5E87",height = 30,corner_radius = 15)
exit_button.grid(row=0, column=5, padx=(5, 10), pady=10, sticky="news")


for i in range(1):
    button_frame.grid_rowconfigure(i,weight=1)
for i in range(6):
    button_frame.grid_columnconfigure(i,weight=1)

for i in range(4):
    frame.grid_rowconfigure(i,weight=1)
for i in range(2):
    frame.grid_columnconfigure(i,weight=1)

window.mainloop()
