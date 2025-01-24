import customtkinter as ctk
import sys
import tkinter
from tkinter import ttk
import pandas as pd
import webbrowser
from PIL import Image
from tkcalendar import DateEntry
from datetime import datetime
ctk.set_appearance_mode("light")
#ctk.set_default_color_theme("dark-blue")
import json
class GeneratedForm(ctk.CTkToplevel):
    def __init__(self, parent):
        #ctk.CTkToplevel.__init__(self, parent)
        #self.title("Generated Form")
        #self.geometry("400x400")

        # Load configuration
        self.config_path = "config.json"
        self.config = self.load_config()

        # Check access when the form is created
        if not self.check_access():
            # If access is not allowed, you might want to handle this case.
            # For example, you can show a message and then destroy the form.
            tkinter.messagebox.showinfo("Access Denied", "Access to the form is disabled.")
            self.destroy()

   

        # rest of your __init__ method...

    def load_config(self):
        try:
            with open(self.config_path, 'r') as config_file:
                config = json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case when the file is not found or not valid JSON
            # You might want to create an initial configuration here.
            config = {"access_enabled": True}

        return config

    def check_access(self):
        return self.config.get("access_enabled", False)

    def reset_action(self):
        # Clear entry widgets
        first_name_entry.delete(0, "end")
        last_name_entry.delete(0, "end")
        gd_name_entry.delete(0, "end")
        age_spin.delete(0, "end")

        # Clear DateEntry widget
        dob_cal.delete(0, "end")

        address_entry.delete(0, "end")
        mobile_entry.delete(0, "end")
        email_entry.delete(0, "end")

        # Reset combo boxes
        title_combo.set("")
        gender_combo.set("")
        relegion_combo.set("")
        caste_combo.set("")
        dept_combo.set("")
        year_combo.set("")
        sem_combo.set("")

        # Uncheck the check box
        terms_check.deselect()

    def is_valid_mobile_no(self,mobile_value):
        return mobile_value.isdigit() and len(mobile_value)==10
    
    def submit_action(self):
        if not self.check_access():
            tkinter.messagebox.showerror('Access Denied', 'Form submission is not allowed. Please contact the admin.')
            return
         # Get values from the entry widgets
        unique_id1 = datetime.now().strftime("%Y%m%d%H%M%S"),
        unique_id= int(unique_id1[0])   
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        title_value = title_combo.get()
        guardian_name = gd_name_entry.get()
        age_value = age_spin.get()
        dob_value = dob_cal.get()
        address_value = address_entry.get()
        mobile_value = mobile_entry.get()
        email_value = email_entry.get()
        gender_value = gender_combo.get()
        religion_value = relegion_combo.get()
        caste_value = caste_combo.get()
        dept_value = dept_combo.get()
        year_value = year_combo.get()
        sem_value = sem_combo.get()
        terms_accepted = terms_check.get()

        if not self.is_valid_mobile_no(mobile_value):
            tkinter.messagebox.showerror('Error', 'Mobile number must be 10 digits')
            return
    # Check if all the fields are filled
        if not all([first_name, last_name, title_value, guardian_name, age_value, dob_value, address_value, mobile_value, email_value, gender_value, religion_value, caste_value, dept_value, year_value, sem_value, terms_accepted]):
            tkinter.messagebox.showerror('Error', 'Please fill all the fields')
            return
        confirm = tkinter.messagebox.askyesno("Confirmation", "Do you want to submit the form?")
        if confirm :

    # Create a dictionary with the collected data
            data = {
                "Unique id":[unique_id],
                "First Name": [first_name],
                "Last Name": [last_name],
                "Title": [title_value],
                "Guardian's Name": [guardian_name],
                "Age": [age_value],
                "Date of Birth": [dob_value],
                "Address": [address_value],
                "Mobile No.": [mobile_value],
                "Email id": [email_value],
                "Gender": [gender_value],
                "Religion": [religion_value],
                "Caste": [caste_value],
                "Department": [dept_value],
                "Year": [year_value],
                "Semester": [sem_value],
                "Terms Accepted": [terms_accepted],
                }


        # Create a DataFrame from the dictionary
            df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file
            try:
                    existing_df = pd.read_excel('students.xlsx')
                    new_df = pd.concat([existing_df, df], ignore_index=True)
            except FileNotFoundError:
                    new_df = df
            new_df.to_excel('students.xlsx', index=False)
            self.reset_action()   
            tkinter.messagebox.showinfo('Success',f"Student information saved successfully , Unique id :{unique_id}")
    


window = ctk.CTk()
window.title("SSRS & Company")
window.config(bg="#EBF8FF")
style = ttk.Style(window)

my_image = ctk.CTkImage(light_image=Image.open("STCET-Logo.png"),size = (90,90))

# Create a CTkLabel with the CTkImage
p_label = ctk.CTkLabel(window, image=my_image, text=" ",bg_color="#EBF8FF")
p_label.pack(padx=20, pady=10)

college_label = ctk.CTkLabel(window,text="St. Thomas' College of Engineering & Technology",
                             font=ctk.CTkFont(family = "Old English Text MT",size=30,weight="bold"),bg_color = "#EBF8FF",text_color="#264D61")
college_label.pack(padx = 10,pady =10)
title_label = ctk.CTkLabel(window,text="Student Information Form",font=ctk.CTkFont(family = "Arial",size=25,weight = "bold",),bg_color="#EBF8FF",text_color="#264D61")
title_label.pack(padx = 10,pady =(10,10))

frame = ctk.CTkFrame(window,fg_color="#FEFEFE",bg_color="#EBF8FF",corner_radius=15,border_width=2,border_color="#264D61")
frame.pack(fill = "x",padx = 100,pady = 10)

#create widgets.............

#create basic details frame.............

user_info_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
user_info_frame.grid(row = 0,column = 0,columnspan = 2,padx = 50,pady = (20,1),sticky = "news")

first_name_label = ctk.CTkLabel(user_info_frame,text="First Name   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
first_name_label.grid(row=0,column=2)
last_name_label = ctk.CTkLabel(user_info_frame,text="Last Name   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
last_name_label.grid(row=0,column=4)

first_name_entry = ctk.CTkEntry(user_info_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
first_name_entry.grid(row=0,column=3,sticky = "ew")
last_name_entry = ctk.CTkEntry(user_info_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
last_name_entry.grid(row=0,column=5,sticky = "ew")

title = ctk.CTkLabel(user_info_frame,text="Title   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264d61")
title.grid(row=0,column=0)
title_combo = ctk.CTkComboBox(user_info_frame,values=["","Mr.","Ms.","Dr.","Prof."],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                              button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
title_combo.grid(row=0,column=1,sticky = "ew")

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=15,pady=15)
    
rows = 1
columns = 6
for i in range(rows):
    user_info_frame.grid_rowconfigure(i,weight=1)
for i in range(columns):
    user_info_frame.grid_columnconfigure(i,weight=1)

user_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
user_frame.grid(row = 1,column = 0,padx = (50,10),pady = (20,10),sticky = "news")


gd_name = ctk.CTkLabel(user_frame,text="Gurdian's Name   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
gd_name.grid(row = 0,column = 0)
gd_name_entry = ctk.CTkEntry(user_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
gd_name_entry.grid(row = 0,column = 1,sticky = "ew",columnspan = 3,padx =25 )

age_label = ctk.CTkLabel(user_frame,text="Age   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
age_label.grid(row = 2,column = 0)
age_spin = tkinter.Spinbox(user_frame,from_=18,to=25,font=ctk.CTkFont(size=15),bg="#EBF8FF",border = 2,fg = "#9c6644",buttonbackground = "#EBF8FF")
age_spin.grid(row=2,column=1,sticky = "news")

dob_label = ctk.CTkLabel(user_frame,text="Date of Birth   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
dob_label.grid(row = 2,column = 2)
dob_cal = DateEntry(user_frame, width=20, style = 'my.DateEntry' ,background = "#264d61" ,borderwidth=2,font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15))
dob_cal.grid(row=2, column=3,sticky = "news")
style.configure('my.DateEntry', background="#264d61",foreground ="#9c6644",arrowcolour = "grey")

address_label = ctk.CTkLabel(user_frame,text="Address   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
address_label.grid(row = 1,column = 0)
address_entry = ctk.CTkEntry(user_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
address_entry.grid(row = 1,column = 1,sticky = "ew",columnspan = 3,padx = 25)

mobile_label = ctk.CTkLabel(user_frame,text="Mobile No.   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
mobile_label.grid(row = 3,column = 0)
mobile_entry = ctk.CTkEntry(user_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
mobile_entry.grid(row = 3,column = 1,sticky = "ew")


email_lable = ctk.CTkLabel(user_frame,text="Email id   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
email_lable.grid(row = 3,column = 2)
email_entry = ctk.CTkEntry(user_frame,fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644")
email_entry.grid(row = 3,column = 3,sticky = "ew")



for widget in user_frame.winfo_children():
    widget.grid_configure(padx=15,pady=15)
    
rows = 4
columns = 4
for i in range(rows):
    user_frame.grid_rowconfigure(i,weight=1)
for i in range(columns):
    user_frame.grid_columnconfigure(i,weight=1)

address_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
address_frame.grid(row = 1,column = 1,padx = (10,50),pady = (20,10),sticky = "news")

gender_label = ctk.CTkLabel(address_frame,text="Gender   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
gender_label.grid(row = 0,column = 0)
gender_combo = ctk.CTkComboBox(address_frame,values=["Male","Female","Others"],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                            button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
gender_combo.grid(row = 0,column = 1,sticky = "ew")

relegion_label = ctk.CTkLabel(address_frame,text="Religion   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
relegion_label.grid(row = 1,column = 0)
relegion_combo = ctk.CTkComboBox(address_frame,values=[" ","Hinduism","Islam", "Sikhism", "Buddhism","Jainism","Judaism"],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                                 button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
relegion_combo.grid(row = 1,column = 1,sticky = "ew")

caste_label = ctk.CTkLabel(address_frame,text="Caste   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
caste_label.grid(row = 2,column = 0)
caste_combo = ctk.CTkComboBox(address_frame,values=["","General","SC","ST","OBC-A","OBC-B"],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                               button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
caste_combo.grid(row =2,column = 1,sticky = "ew")

for widget in address_frame.winfo_children():
    widget.grid_configure(padx=15,pady=10)
    
rows1 = 3
columns1 = 2
for i in range(rows1):
    address_frame.grid_rowconfigure(i,weight=1)
for i in range(columns1):
    address_frame.grid_columnconfigure(i,weight=1)

course_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
course_frame.grid(row = 2,column =0,columnspan = 2,padx = 50,pady = (10,10),sticky = "news")

dept_label = ctk.CTkLabel(course_frame,text="Department   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
dept_label.grid(row = 0,column = 0)
dept_combo = ctk.CTkComboBox(course_frame,values=["CSE","IT","AIML","ECE","EE"],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                             button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
dept_combo.grid(row = 0,column = 1,sticky = "ew")

year_label = ctk.CTkLabel(course_frame,text="Year   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
year_label.grid(row = 0,column = 2)
year_combo = ctk.CTkComboBox(course_frame,values=["1st","2nd","3rd","4th"],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                             button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
year_combo.grid(row = 0,column = 3,sticky = "ew")

sem_lable = ctk.CTkLabel(course_frame,text="Semester   :",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),text_color="#264D61")
sem_lable.grid(row = 0,column = 4)
sem_combo = ctk.CTkComboBox(course_frame,values=["1st","2nd","3rd","4th","5th", "6th","7th", "8th" ],fg_color= "#EBF8FF",border_color="#264d61",text_color="#9c6644",
                          button_color="#264d61",button_hover_color="#2F5E87",dropdown_fg_color="#EBF8FF",dropdown_hover_color="#2F5E87",dropdown_text_color="#000000")
sem_combo.grid(row = 0,column = 5,sticky = "ew")

for widget in course_frame.winfo_children():
    widget.grid_configure(padx=15,pady=15)
    
for i in range(1):
    course_frame.grid_rowconfigure(i,weight=1)
for i in range(6):
    course_frame.grid_columnconfigure(i,weight=1)

terms_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
terms_frame.grid(row = 3,column = 0,columnspan = 2,padx = 50,pady = (10,10),sticky = "news")
def open_html_file():
    html_file_path = 'TC.html'
    webbrowser.open(html_file_path)
    # Specify the path to the text file


term_label = ctk.CTkLabel(terms_frame,text="Terms & Conditions",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15,underline = True),text_color = 'blue',cursor="hand2")
term_label.grid(row = 0,column = 0)
term_label.bind("<Button-1>", lambda event: open_html_file())

   
terms_check = ctk.CTkCheckBox(terms_frame, text="I accept the terms & conditions",text_color="#264D61",font=ctk.CTkFont(family = "Times New Roman" ,weight="bold",size = 15),
                              checkmark_color="#264d61",fg_color = "#EBF8FF",hover_color = "#2F5E87")
terms_check.grid(row=1, column=0)

for widget in terms_frame.winfo_children():
    widget.grid_configure(padx=13,pady=5)
    

button_frame = ctk.CTkFrame(frame,fg_color="#E3CBB1",bg_color="#FEFEFE",corner_radius=15,border_width=2,border_color="#264D61")
button_frame.grid(row = 4,column = 0,columnspan = 2,padx = 50,pady = (10,20),sticky = "news")
    

r = 2
c=1

for i in range(r):
    terms_frame.grid_rowconfigure(i,weight=1)
for i in range(c):
    terms_frame.grid_columnconfigure(i,weight=1)
    
for i in range(1):
    button_frame.grid_rowconfigure(i,weight=1)
for i in range(3):
    button_frame.grid_columnconfigure(i,weight=1)


for i in range(5):
    frame.grid_rowconfigure(i,weight=1)
for i in range(2):
    frame.grid_columnconfigure(i,weight=1)

def exit_action():
        confirm = tkinter.messagebox.askyesno("Return", "Are you sure you want to return to login page?")
        if confirm:
            window.destroy()
            sys.exit()
 #exit button....
return_button = ctk.CTkButton(button_frame,text="RETURN",command=exit_action,fg_color="#264D61",hover_color="#2F5E87",height = 28,corner_radius = 14)
return_button.grid(row = 0,column = 0,padx = (15,7.5),pady = 13,sticky = "ew")
 


if __name__ == "__main__":
    form = GeneratedForm(window)
    # Add functionality to the submit button
    submit = ctk.CTkButton(button_frame, text="SUBMIT", command=form.submit_action,fg_color="#264D61",hover_color="#2F5E87",height = 28,corner_radius = 14)
    submit.grid(row=0, column=1, padx=(7.5,7.5), pady=13, sticky="ew")
    reset = ctk.CTkButton(button_frame, text="RESET", command=form.reset_action,fg_color="#264D61",hover_color="#2F5E87",height = 28,corner_radius = 14)
    reset.grid(row=0, column=2, padx=(7.5,15), pady=13, sticky="ew")
   
    window.mainloop()
