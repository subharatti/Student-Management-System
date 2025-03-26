from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import os
import sys
import sqlite3
from adding_tables import MarkbookProcessor

class SetupInfoPage():
    def __init__(self, db_file, frame):
        "Initalize the vairables that will be used throughout the program (file, frame)"
        try:
            self.db_file = db_file
            self.frame = frame #define variables to be used throughout
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def place_elements(self):
        "Places the widgets of the program on the screen and formats them correctly, linking them to corresponding functions"
        try:
            self.title = Label(self.frame, text="Edit Setup Info Below", font=("Courier", 20, "bold"), fg="red", bg="#d3d3b1")
            self.title.place(x=280, y=30) #places title

            right_frame = Frame(self.frame, width=350, height=370, bg="#d3d3b1")
            right_frame.place(x=500, y=70) #created right frame for the image

            logoimage = PhotoImage(file="books.png")
            logolbl = Label(right_frame, image=logoimage,bg="#d3d3b1")
            logolbl.place(x=40,y=10) #adds image to right frame
            logolbl.image = logoimage
            
            self.fullname_lbl = Label(self.frame, text="Full Name", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.fullname_lbl.place(x=20, y=110) #full name widgets

            self.fullname_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.fullname_entry.place(x=190, y=112)

            self.course_name_lbl = Label(self.frame, text="Course Name", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.course_name_lbl.place(x=20, y=160) #course name widgets

            self.course_name_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.course_name_entry.place(x=210, y=162)

            self.course_code_lbl = Label(self.frame, text="Course Code", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.course_code_lbl.place(x=20, y=210) #course code widgets

            self.course_code_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.course_code_entry.place(x=210, y=212)

            self.category1_name_lbl = Label(self.frame, text="Category 1 Name", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.category1_name_lbl.place(x=20, y=260) #categeory 1 wigets

            self.category1_name_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.category1_name_entry.place(x=280, y=262)

            self.category1_percent_lbl = Label(self.frame, text="Category 1 %", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.category1_percent_lbl.place(x=20, y=310) #category 1 percentage widgets

            self.category1_percent_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.category1_percent_entry.place(x=230, y=312)

            self.category2_name_lbl = Label(self.frame, text="Category 2 Name", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.category2_name_lbl.place(x=20, y=360) #category 2 name widgets

            self.category2_name_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.category2_name_entry.place(x=280, y=362)

            self.category2_percent_lbl = Label(self.frame, text="Category 2 %", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.category2_percent_lbl.place(x=20, y=410) #categiry 2 percentage widgets

            self.category2_percent_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.category2_percent_entry.place(x=230, y=412)

            self.username_lbl = Label(self.frame, text="Username", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.username_lbl.place(x=20, y=460) #username widgets

            self.username_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15)
            self.username_entry.place(x=190, y=462)

            self.password_lbl = Label(self.frame, text="Password", font=("Courier", 20), fg="dark green", bg="#d3d3b1")
            self.password_lbl.place(x=20, y=510) #password widgets

            self.password_entry = Entry(self.frame, font=("Courier", 20), fg="black", bg="#b1caa4", width=15, show="*")
            self.password_entry.place(x=190, y=512)

            self.update_button = Button(self.frame, text="Update Information", command=self.update_info, font=("Courier", 20), bg="dark green", fg="black")
            self.update_button.place(x=530, y=460) #update button to update the info in database + entries

            self.add_info()
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def old_info(self):
        "Gets the category 1 and 2 names currently in the database to be used for furture comparisons"
        try:
            self.categorys = {}
            conn = sqlite3.connect(self.db_file) #fetched the catgeory 1 and 2 names from the setup database
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 Name",))
            cat1 = cursor.fetchone()
            self.cat1 = cat1[0] #assigns name to variable fokr future reference

            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 Name",))
            cat2 = cursor.fetchone()
            self.cat2 = cat2[0] #assigns name to variable fokr future reference
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def add_info(self):
        "Obtains the changes made in the entries and updates the entries accoridingly, gets information to update the database"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            keys = ["Full Name", "Course Name", "Course Code", "Category 1 Name", "Category 1 %", "Category 2 Name", "Category 2 %", "Username", "Password"]

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[0],))
            full_name = cursor.fetchone() #get the fullname currently in the setup file
            full_name = full_name[0]

            self.fullname_entry.delete(0, END) #update the entry with the new full name
            self.fullname_entry.insert(0, full_name)
            
            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[1],))
            name = cursor.fetchone()
            name = name[0]  #get the course name currently in the setup file
            self.course_name_entry.delete(0, END)
            self.course_name_entry.insert(0, full_name) #update the entry with the new course name

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[2],))
            code = cursor.fetchone()
            code = code[0] #get the course code currently in the setup file

            self.course_code_entry.delete(0, END)
            self.course_code_entry.insert(0, code) #update the entry with the new course code

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[3],))
            cat1 = cursor.fetchone()
            cat1 = cat1[0] #get the category 1 name currently in the setup file

            self.category1_name_entry.delete(0, END)
            self.category1_name_entry.insert(0, cat1) #update the entry with the new category 1 name

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[4],))
            cat1per = cursor.fetchone()
            cat1er = cat1per[0] #get the category 1 percent currently in the setup file

            self.category1_percent_entry.delete(0, END)
            self.category1_percent_entry.insert(0, cat1per) #update the entry with the category 1 percent

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[5],))
            cat2 = cursor.fetchone()
            cat2 = cat2[0] #get the category 2 name currently in the setup file

            self.category2_name_entry.delete(0, END)
            self.category2_name_entry.insert(0, cat2) #update the entry with the category 2 name

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[6],))
            cat2per = cursor.fetchone()
            cat2per = cat2per[0] #get the category 2 percent currently in the setup file

            self.category2_percent_entry.delete(0, END)
            self.category2_percent_entry.insert(0, cat2per)  #update the entry with the category 2 percent

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[7],))
            username = cursor.fetchone()
            username = username[0] #get the username currently in the setup file
            
            self.username_entry.delete(0, END)
            self.username_entry.insert(0, username) #update the entry with the username

            cursor.execute("SELECT value FROM setup WHERE key=?", (keys[8],))
            password = cursor.fetchone()
            password = password[0] #get the password currently in the setup file

            self.password_entry.delete(0, END)
            self.password_entry.config(show="")

            self.password_entry.insert(0, password) #update the entry with the category password
            self.old_info()
            
            conn.commit()
            conn.close()
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def update_info(self):
        "Updates the info with the changes in the database, also validates all the information to make sure formats are correct"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            values = [] #will hold new values for keys
            keys = ["Full Name", "Course Name", "Course Code", "Category 1 Name", "Category 1 %", "Category 2 Name", "Category 2 %", "Username", "Password"] #holds the keys in setup table

            values.append(self.fullname_entry.get()) #append the values to the list
            values.append(self.course_name_entry.get())
            values.append(self.course_code_entry.get())
            values.append(self.category1_name_entry.get())
            values.append(self.category1_percent_entry.get())
            values.append(self.category2_name_entry.get())
            values.append(self.category2_percent_entry.get())
            values.append(self.username_entry.get())
            values.append(self.password_entry.get())

            total_percentage = 0 #check if percentages are numbers and add up to 100
            for i in range(len(keys)):
                if keys[i].endswith("%"): 
                    try:
                        percentage = float(values[i]) #looks for the key with %, then gets index of value and checks (because same indexs)
                        total_percentage += percentage
                    except ValueError:
                        showwarning("Invalid Input", f"The value for {keys[i]} must be a number.") #error if not a number
                        return

            if total_percentage != 100: #if they dont add to 100 then error
                showwarning("Invalid Input", "Category percentages must add up to 100.")
                return

            for i in range(len(keys)): #update each key-value pair in values and keys lists
                cursor.execute("UPDATE setup SET value=? WHERE key=?", (values[i], keys[i]))

            cursor.execute("SELECT category from Tests") #get the category from the tests table
            results = cursor.fetchall()
            for i in results:
                category = i[0]
                if category == self.cat1 and category != (self.category1_name_entry.get()): #if the category  1did change from the older one, 
                    cursor.execute("UPDATE Tests SET category=? WHERE category=?", (self.category1_name_entry.get(), self.cat1)) #update in database
                if category == self.cat2 and category != (self.category2_name_entry.get()): #if the category2 did change from the older one, 
                    cursor.execute("UPDATE Tests SET category=? WHERE category=?", (self.category2_name_entry.get(), self.cat2)) #update in database

            conn.commit()
            conn.close()

            showinfo("Successful Update", "Setup Info Successfully Updated")

            self.add_info() #refresh the displayed information after the update
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
