from tkinter import *
import os
import sqlite3
from tkinter.messagebox import *
from helper_functions import HelperFunctions

class SetupPage():
    def __init__(self, setup_table_name, cursor, connection, login_page_callback):
        "Initalize the variables to be used throughout the program"
        try:
            super().__init__()
            self.connection = connection
            self.setup_table_name = setup_table_name
            self.cursor = cursor
            self.login_page_callback = login_page_callback #define the variables to be used throughout
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def setup_page_temp(self):
        "Create the setup page by creating the widgets, placing them, and binding the functions where needed"
        try:
            self.helpers = HelperFunctions() #define module to be used
            def save_setup():
                "Formats all the information provided and calls the save setup function to save the information"
                default_texts = [ #default keys for the setup file
                    "Enter Full Name",
                    "Enter Course Name",
                    "Enter Course Code",
                    "Enter C1 Name",
                    "Enter C1 %",
                    "Enter C2 Name",
                    "Enter C2 %",
                    "Enter Username",
                    "Enter Password"
                ]

                entry_fields = [ #gets the entry files and text entered
                    entry_full_name,
                    entry_course_name,
                    entry_course_code,
                    entry_category1_name,
                    entry_category1_value,
                    entry_category2_name,
                    entry_category2_value,
                    entry_username,
                    self.entry_password
                ]

                empty_fields = []
                for i in range(len(entry_fields)):
                    if entry_fields[i].get() == default_texts[i]:
                        empty_fields.append(default_texts[i]) #populates the lists with the fields that are empty 

                if len(empty_fields) > 0:
                    empty_fields_str = "\n".join(empty_fields)
                    showwarning("Empty Fields", f"The following fields are empty:\n{empty_fields_str}") #tells user whichs ones are empty
                else:
                    try:
                        #gets all the information in the fields eneters by the user
                        full_name = entry_full_name.get()
                        course_name = entry_course_name.get()
                        course_code = entry_course_code.get()
                        category1_name = entry_category1_name.get()
                        category1_value = entry_category1_value.get()
                        category2_name = entry_category2_name.get()
                        category2_value = entry_category2_value.get()
                        username = entry_username.get()
                        password = self.entry_password.get()

                        float_category1 = float(category1_value)
                        float_category2 = float(category2_value) #converts percentages to floast

                        if float_category1 + float_category2 != 100:
                            showwarning("Percentages Error", "Error: Percentages don't add up to 100!")
                        else:
                            setup_data = { #makes the setup dictionary with the keys and assigned values
                                "Full Name": full_name,
                                "Course Name": course_name,
                                "Course Code": course_code,
                                "Category 1 Name": category1_name,
                                "Category 1 %": category1_value,
                                "Category 2 Name": category2_name,
                                "Category 2 %": category2_value,
                                "Username": username,
                                "Password": password
                            }

                            self.save_setup_to_db(setup_data) #call functions to save the information to setup table
                            status_lbl.configure(text="Setup Successful!")
                            status_lbl.after(1000, self.login_page_callback) #after 1000ms, go to the login page callback
                            
                    except ValueError:
                        showwarning("Value Error", "Error: Percentages are not valid numbers!") #error if percentages not valid

            mainframe = Frame(width=900, height=600, bg="#d3d3b1")
            mainframe.place(x=0, y=0) #created base frame

            self.text = Label(mainframe, font=("Courier",12), fg="black", bg="#b1caa4", text="WELCOME:" + "\n" + "Enter your setup details and press 'Save'!")
            self.text.place(x=230, y=555, anchor = "w") #welcome message for the page

            left_frame = Frame(mainframe, width=450, height=500, bg="#d3d3b1")
            left_frame.place(x=0, y=0) #creates left frame to hold the image
            bgimage = PhotoImage(file="login.png")
            bglbl = Label(left_frame, image=bgimage, bg="#d3d3b1") #loads and adds image
            bglbl.place(x=50, y=50)
            bglbl.image = bgimage

            right_frame = Frame(mainframe, width=450, height=500, bg="#d3d3b1") #creates right frame to hold info and widgets
            right_frame.place(x=450, y=0)
            title = Label(right_frame, font=("Courier", 20, "bold"), text="Setup Page", bg="#d3d3b1", fg="dark green")
            title.place(x=120, y=30) #title for right frame

            labels_default_text = [ #the label texsrs
                ("Full Name:", "Enter Full Name"),
                ("Course Name:", "Enter Course Name"),
                ("Course Code:", "Enter Course Code"),
                ("Category 1 Name:", "Enter C1 Name"),
                ("Category 1 %:", "Enter C1 %"),
                ("Category 2 Name:", "Enter C2 Name"),
                ("Category 2 %:", "Enter C2 %"),
                ("Username:", "Enter Username"),
                ("Password:", "Enter Password")
            ]

            #creates and places all the entries
            entry_full_name = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_full_name.focus()
            entry_course_name = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_course_code = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_category1_name = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_category1_value = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_category2_name = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_category2_value = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            entry_username = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_password = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_password.configure(show="", text="Enter Password")  # initially show the password as plain text

            entry_fields = [ #holds the entry fields variables
                entry_full_name,
                entry_course_name,
                entry_course_code,
                entry_category1_name,
                entry_category1_value,
                entry_category2_name,
                entry_category2_value,
                entry_username,
                self.entry_password
            ]

            for idx in range(len(labels_default_text)):
                label_text, default_text = labels_default_text[idx] #places the labels in the labels_default_texsts
                label = Label(right_frame, text=label_text, bg="#d3d3b1", font=("Courier", 14), fg="dark green")
                label.place(x=30, y=100 + idx * 30)
                entry = entry_fields[idx]
                entry.place(x=230, y=100 + idx * 30)
                self.helpers.draw_separator(right_frame, 175, 2, 230, 120 + idx * 30) #creates the seperator aswell
                self.helpers.format_entry(entry, default_text)

            self.entry_password.bind("<FocusIn>", lambda event: self.helpers.show_password(event, self.entry_password)) #binds the password entry
            self.entry_password.bind("<FocusOut>", lambda event: self.helpers.hide_password(event, self.entry_password, "Enter Password")) #binds the password entry

            save_button = Button(right_frame, text="Save", command=save_setup, font=("Courier", 14), bg="dark green", fg="black")
            save_button.place(x=200, y=380) #create, link, and place the save button
            status_lbl = Label(right_frame, text="", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            status_lbl.place(x=140, y=430) #create and place status bar
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def save_setup_to_db(self, setup_data):
        "Saved the setup information by creating the table (if not exist) and inserting each key and value inside"
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.setup_table_name} (key TEXT, value TEXT)")
            for key, value in setup_data.items():
                self.cursor.execute(f"INSERT INTO {self.setup_table_name} VALUES (?, ?)", (key, value)) #adds each key and value in the setup table
            self.connection.commit()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            showwarning("Database Error", "Error occurred while saving setup information.")
