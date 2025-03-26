from tkinter import *
import os
import sys
from tkinter.messagebox import *
from helper_functions import HelperFunctions

class LoginPage():
    def __init__(self, setup_table_name, cursor, main_page_callback):
        "Initalize the variables that will be used throughout the program"
        try:
            super().__init__()
            self.setup_table_name = setup_table_name #create the variables that will be used throughout the program
            self.cursor = cursor
            self.main_page_callback = main_page_callback
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def login_page_temp(self):
        "Create the login page by placing the widgets, validating the informaiton entered, and then switching to the main page when validated"
        try:
            self.helpers = HelperFunctions()
            def validate_login():
                "Validate the information by going through the setup table and checking to see if the information matched"
                username = self.entry_username.get()
                password = self.entry_password.get() #get the username and password entered by the user

                try:
                    self.cursor.execute(f"SELECT value FROM {self.setup_table_name} WHERE key='Username'") #get username in setup file
                    saved_username = self.cursor.fetchone()[0]
                    self.cursor.execute(f"SELECT value FROM {self.setup_table_name} WHERE key='Password'") #get password in setup file
                    saved_password = self.cursor.fetchone()[0]

                    if saved_username == username and saved_password == password: #validate it (are they equal)
                        status_lbl.configure(text="Login Successful!") #if yes, change staus to successful
                        status_lbl.after(1000, self.main_page_callback) #call the mainpage callback after 1000ms
                    else:
                        showwarning("Login Failed", "Incorrect username or password. Please try again.") #not successful = warnning
                except Exception as e:
                    print(f"Error validating login: {e}")
                    showwarning("Login Failed", "Error occurred while validating login credentials.")

            mainframe = Frame(width=900, height=600, bg="#d3d3b1")
            mainframe.place(x=0, y=0) #create the main frame
            self.text = Label(mainframe, font=("Courier",12), fg="black", bg="#b1caa4", text="WELCOME:" + "\n" + "Enter your login details and press 'Log In'!")
            self.text.place(x=230, y=555, anchor = "w") #add in the inital text

            left_frame = Frame(mainframe, width=450, height=500, bg="#d3d3b1")
            left_frame.place(x=0, y=0) #create and place left frame to hold image
            bgimage = PhotoImage(file="login.png")
            bglbl = Label(left_frame, image=bgimage, bg="#d3d3b1") #get and place image
            bglbl.place(x=50, y=50)
            bglbl.image = bgimage

            right_frame = Frame(mainframe, width=450, height=500, bg="#d3d3b1")
            right_frame.place(x=450, y=0)
            title = Label(right_frame, font=("Courier", 20, "bold"), text="Login Page", bg="#d3d3b1", fg="dark green")
            title.place(x=120, y=70) #create the right frame and place login page title

            labels_default_text = [
                ("Username:", "Enter Username"),
                ("Password:", "Enter Password")
            ] #default label text

            #create the entries and bind them accordingly
            self.entry_username = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_username.focus() 
            self.entry_password = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_password = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_password = Entry(right_frame, font=("Courier", 12), bg="#d3d3b1", fg="gray", border=0)
            self.entry_password.insert(0, "Enter Password")
            self.entry_password.bind("<FocusIn>", lambda event: self.helpers.on_entry_click(event, self.entry_password, "Enter Password")) #bind the password entry
            self.entry_password.bind("<FocusOut>", lambda event: self.helpers.on_focus_out(event, self.entry_password, "Enter Password")) #bind the password entry for focus out
            self.entry_password.configure(show="", fg="gray")
            self.entry_password.delete(0, "end")  #clear the password field


            entry_fields = [self.entry_username, self.entry_password]

            for idx in range(len(labels_default_text)): #this places the entries accordingly (to make them all evenly spaced)
                label_text, default_text = labels_default_text[idx]
                label = Label(right_frame, text=label_text, bg="#d3d3b1", font=("Courier", 14), fg="dark green")
                label.place(x=30, y=180 + idx * 80)
                entry = entry_fields[idx]
                entry.place(x=230, y=180 + idx * 80)
                self.helpers.draw_separator(right_frame, 175, 2, 230, 200 + idx * 80) #draw the seperaterator 
                self.helpers.format_entry(entry, default_text) #format the entry by setting the binding in the helperfunctions
                
            self.entry_password.bind("<FocusIn>", lambda event: self.helpers.show_password(event, self.entry_password))
            self.entry_password.bind("<FocusOut>", lambda event: self.helpers.hide_password(event, self.entry_password, "Enter Password"))

            login_button = Button(right_frame, text="Log In", command=validate_login, font=("Courier", 14), bg="dark green", fg="black")
            login_button.place(x=170, y=350) #create the login button and place
            status_lbl = Label(right_frame, text="", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            status_lbl.place(x=125, y=400) #create the status button and place
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
