from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
import os
import sqlite3
import sys
from adding_tables import MarkbookProcessor
from students_page import StudentPage
from helper_functions import HelperFunctions
from login_page import LoginPage
from setup_page import SetupPage
from main_page import MainPage
from tests_page import TestsPage
from report_page import ReportPage
from exporting_functions import ExportingFunctions
from edit_setup_page import SetupInfoPage
from seating_page import SeatingPage
from attendance_page import AttendancePage



class markbook(Tk):
    def __init__(self):
        "Initalize the variables that will be used throughout the program as well as the initial features (size, logo)"
        try:
            super().__init__()
            self.geometry("900x600+300+100") #size of window
            self.resizable(False,False) #not resizable
            mainlogoimage = PhotoImage(file="mainlogo.png")
            self.iconphoto(True, mainlogoimage) #same logo for all pages
            self.db_file = "markbook.db"
            self.setup_table_name = "setup" #set the markbook name and the setup table name
            try:
                self.connection = sqlite3.connect(self.db_file)
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"SELECT * FROM {self.setup_table_name}") #get all info from setup page if avilable
                self.login_page() #if available, go to login
            except sqlite3.OperationalError:
                self.setup_page() #if not available then go to setup page
            except sqlite3.DatabaseError:
                self.setup_page()
            self.mainloop()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def setup_page(self):
        "Creates the initial setup page by calling the module and the functions within"
        try:
            self.helpers = HelperFunctions() #define module
            self.title("Setup Page")
            self.setup = SetupPage(self.setup_table_name, self.cursor,self.connection, self.login_page) #define module, assign the values
            self.setup.setup_page_temp() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def login_page(self):
        "Creates the initial login page by calling the module and the functions within"
        try:
            self.helpers = HelperFunctions() #define module
            self.title("Login Page")
            self.login = LoginPage(self.setup_table_name, self.cursor, self.main_page) #define module
            self.login.login_page_temp() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 
  
    def main_page(self):
        "Creates the initial main page by calling the module and the functions within"
        try:
            self.title("SmartMarks - Markbook App") #define module
            self.menubar = Menu(self)
            #define module
            self.mainscreen = MainPage(self.menubar, self.cursor, self.connection, self.db_file, self.exit, self.edit_students, self.edit_tests, self.print_report, self.edit_setup, self.seating_page, self.attendance_page)
            self.mainscreen.main_page_temp() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def exit(self):
        "Exits out of the program when exit is selected"
        try:
            self.destroy() #exits out of program
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
                
    def edit_students(self):
        "Creates the initial edit students page by calling the module and the functions within"
        try:
            self.studentmainframe = Frame(width=900, height=600, bg="#d3d3b1")#create base frame
            self.studentmainframe.place(x=0, y=0)
            add_treeview = StudentPage(self.db_file,self.studentmainframe)#define module
            add_treeview.create_treeview() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def edit_tests(self):
        try:
            self.testmainframe = Frame(width=900, height=600, bg="#d3d3b1")
            self.testmainframe.place(x=0, y=0)
            add_treeview2 = TestsPage(self.db_file,self.testmainframe) #define module
            add_treeview2.create_treeview() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def print_report(self):
        try:
            self.reportmainframe = Frame(width=900, height=600, bg="#d3d3b1") #create base frame
            self.reportmainframe.place(x=0, y=0)
            report = ReportPage(self.db_file,self.reportmainframe) #define module
            report.place_elements() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def edit_setup(self):
        try:
            self.setupmainframe = Frame(width=900, height=600, bg="#d3d3b1") #create base frame
            self.setupmainframe.place(x=0, y=0)
            edit_info = SetupInfoPage(self.db_file,self.setupmainframe) #define module
            edit_info.place_elements() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def seating_page(self):
        try:
            self.bigframe = Frame(width=900, height=600, bg="#d3d3b1") #create base frame
            self.bigframe.place(x=0, y=0)
            self.seating_label = Label(self.bigframe, text= "Editable Seating Arrangement", font=("Courier", 30, "bold"), fg="red", bg="#d3d3b1") #title for page
            self.seating_label.place(x=120, y=50)
            self.text = Label(self.bigframe, font=("Courier",11), fg="black", bg="#b1caa4", text="INSTRUCTIONS:" + "\n" + "CHANGE NUMBER OF STUDENTS PER ROW -> Enter number and press 'Update Arrangement'" + "\n" "SWAP STUDENTS -> Select first student, and then the student you want to swap them with")
            self.text.place(x=80, y=555, anchor = "w") #instructions for page
            self.seatingmainframe = Frame(self.bigframe,width=900, height=600, bg="#d3d3b1")
            self.seatingmainframe.place(x=10, y=200)
            seating_arrangement = SeatingPage(self.db_file,self.seatingmainframe) #define module

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def attendance_page(self):
        try:
            self.attendacemainframe = Frame(width=900, height=600, bg="#d3d3b1")
            self.attendacemainframe.place(x=0, y=0) #create base frame
            edit_info = AttendancePage(self.db_file,self.attendacemainframe) #define module
            edit_info.place_elements() #go to first function of module
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

myapp = markbook()
