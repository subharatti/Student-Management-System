from tkinter import *
import os
import sys
from tkinter.messagebox import *

class HelperFunctions:
    def on_entry_click(self, entry_widget, default_text):
        "Sets the entry widget when it is clicked on, changes the font colour and deletes existing content"
        try:
            if entry_widget.get() == default_text: #if there is the placeholder text in the entry
                entry_widget.delete(0, "end") #delete the entry
                entry_widget.configure(fg="black") #change the font colour to black
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 

    def on_focus_out(self, entry_widget, default_text):
        "When the entry widget is not clicked on, update the text within it"
        try:
            if not entry_widget.get():
                entry_widget.insert(0, default_text) #insert the placeholder text
                entry_widget.configure(fg="gray") #change the colour to gray
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def show_password(self, event, entry_password):
        "Function to show the password when clicked on"
        try:
            if entry_password.get() == "Enter Password":
                entry_password.delete(0, END) #clear the password entry
                entry_password.configure(show="*", fg="black") #show the password
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def hide_password(self, event, entry_password, default_text):
        "Function to side the password when needed"
        try:
            if not entry_password.get():
                entry_password.delete(0, END) #clear the passwird entry
                entry_password.insert(0, default_text) #add in the deafult text
                entry_password.configure(show="", fg="gray") #show the default text
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def draw_separator(self, parent, w, h, xcoordinate, ycoordinate):
        "Draws a horizontal line (mini long frame) when called"
        try:
            frame = Frame(parent, width=w, height=h, bg="dark green") #create the small frame
            frame.place(x=xcoordinate, y=ycoordinate) #place the small frame
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) #put in in the summative

    def format_entry(self, entry_widget, default_text):
        "Format the entry widget depending on the binding command (jump to the binding command when needed)"
        try:
            entry_widget.insert(0, default_text) #add in the default text
            entry_widget.bind("<FocusIn>", lambda event: self.on_entry_click(entry_widget, default_text)) #bind to when entry box clicked
            entry_widget.bind("<FocusOut>", lambda event: self.on_focus_out(entry_widget, default_text)) #bind to when entry box not clicked
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 

    def save_setup_to_db(self, setup_data):
        "Save the setup information to the setup table (create it if not exist) when called"
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.setup_table_name} (key TEXT, value TEXT)") #create the setup table
            for key, value in setup_data.items():
                self.cursor.execute(f"INSERT INTO {self.setup_table_name} VALUES (?, ?)", (key, value)) #insert all the rows in the setup page into the file
            self.connection.commit()
        except Exception as e:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            self.connection.rollback()
            showwarning("Database Error", "Error occurred while saving setup information.")
