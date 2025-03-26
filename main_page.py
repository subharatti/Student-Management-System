from tkinter import *
from tkinter import ttk
import sys
import os
import sqlite3
from tkinter.messagebox import *
from tkinter import filedialog
from students_page import StudentPage
from adding_tables import MarkbookProcessor
from exporting_functions import ExportingFunctions

class MainPage(Frame):
    def __init__(self, menu_bar, cursor, connection, db_file, exit_callback, edit_student_callback, edit_tests_callback, print_report_callback, edit_setup_callback, seating_page_callback, attendance_page_callback):
        "Initalize the variables that will be used throughout the program (fule, callbacks,etc.)"
        try:
            super().__init__()
            self.cursor = cursor #create all the vairables to be called within the program
            self.db_file = db_file
            self.connection = connection
            self.exit_callback = exit_callback
            self.edit_student_callback = edit_student_callback
            self.edit_tests_callback = edit_tests_callback
            self.edit_setup_callback = edit_setup_callback
            self.seating_page_callback = seating_page_callback
            self.attendance_page_callback = attendance_page_callback
            self.menubar = menu_bar
            self.print_report_callback = print_report_callback
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def main_page_temp(self):
        "Creates and places the widgets of the mainpage including the menu bar and text/pictures/buttons"
        try:
            mainframe = Frame(width=900, height=600, bg="#d3d3b1")
            mainframe.place(x=0, y=0) #place the main frame

            file_menu = Menu(self.menubar, tearoff=0,background="#7bba86", fg="black") #create the file menu
            file_menu.add_command(label="Exit", command=self.exit_callback) #add command to file menu (just exit)
            self.menubar.add_cascade(label="File", menu=file_menu)

            edit_menu = Menu(self.menubar, tearoff=0,background="#7bba86", fg="black") #create the edit menu
            edit_menu.add_command(label="Open/Edit Setup Information", command=self.edit_setup) #add the commands to the edit menu
            edit_menu.add_command(label="Add/Edit/Delete Students & Marks", command=self.edit_students)
            edit_menu.add_command(label="Add/Edit/Delete Tests", command=self.edit_tests)
            self.menubar.add_cascade(label="Edit", menu=edit_menu)

            report_menu = Menu(self.menubar, tearoff=0, background="#7bba86", fg="black") #create the report menu
            report_menu.add_command(label="Print Report", command=self.print_report) #add the command to report menu (just print report)
            self.menubar.add_cascade(label="Report", menu=report_menu)

            self.menubar.add_cascade(label="Seating Plan", command=self.seating_plan) #creating menu item for seating plan and link to function
            self.menubar.add_cascade(label="Attendance Page", command=self.attendance_page) #creating menu item for attendance page and link to function

            import_export_menu = Menu(self.menubar, tearoff=0,background="#7bba86", fg="black") #crea the import/export menu
            import_export_menu.add_command(label="Import Students", command=self.update_students) #add the commands to the menu
            import_export_menu.add_command(label="Export Students", command=self.export_students)
            import_export_menu.add_command(label="Import Tests", command=self.update_tests)
            import_export_menu.add_command(label="Export Tests", command=self.export_tests)
            self.menubar.add_cascade(label="Import/Export", menu=import_export_menu)

            self.master.config(menu=self.menubar) #configure the menu

            title = Label(font=("Courier", 30, "bold"), text="Welcome to SmartMarks,", bg="#d3d3b1", fg="dark green") #place the title
            title.place(x=190,y=10)
            subtitle = Label(font=("Courier", 25, "bold"), text="your go to Markbook App!", bg="#d3d3b1", fg="dark green") #add the subtitle
            subtitle.place(x=210,y=50)
            
            instructions = Label(font=("Courier", 14), text="Before selecting actions from the Menu, select your students/test files below.", bg="#d3d3b1", fg="dark green")
            instructions.place(x=15,y=100) #create and place insturctions
            note = Label(font=("Courier", 12), text="(Unless editing Setup Info - Can Edit Without Choosing Files)", bg="#d3d3b1", fg="dark green")
            note.place(x=150,y=120) #create and place note

            left_frame = Frame(mainframe, width=350, height=300, bg="#d3d3b1")
            left_frame.place(x=0, y=150) #create left frame to hold image
            logoimage = PhotoImage(file="logo.png")
            logolbl = Label(left_frame, image=logoimage,bg="#d3d3b1")
            logolbl.place(x=10,y=10) #load and add image to frame
            logolbl.image = logoimage
            
            right_frame = Frame(mainframe, width=550, height=300, bg="#d3d3b1")
            right_frame.place(x=350, y=150) #create right frame to hold buttons and text

            bottom_frame = Frame(mainframe, width=900, height=200, bg="#d3d3b1")
            bottom_frame.place(x=0, y=500)  #create bottom frame for border image

            borderimage = PhotoImage(file="border.png")
            borderlbl = Label(bottom_frame, image=borderimage, bg="#d3d3b1")
            borderlbl.place(x=0, y=0) #load and add image to frame
            borderlbl.image = borderimage

            bottom_frame.lift() #puts bottom frame above all (so its not blocked)

            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('Tests', 'Students', 'Marks')")
            existing_tables = self.cursor.fetchall() #get the existing tables in the database
            
            self.files_uploaded = False
            if len(existing_tables) == 3: #if the tables were already created
                self.files_uploaded = True
                self.full_status = Label(right_frame, text="Status: Files Selected" "\n" + "Select an Action from the Menu!", font=("Courier", 20), bg="#7ca666", fg="black")
                self.full_status.place(x=15,y=150) #status bar is success and user can select menubar commands
            else: #if tables not created
                upload_students_btn = Button(right_frame, text="Upload Students File", command=self.import_students, font=("Courier", 14), bg="dark green", fg="black")
                upload_students_btn.place(x=140,y=50) #add and place upload button

                self.students_status = Label(right_frame, text="Status: Students File Not Selected", font=("Courier", 14), fg="red", bg="#d3d3b1")
                self.students_status.place(x=70,y=100) #add and place status label

                upload_tests_btn = Button(right_frame, text="Upload Test File", command=self.import_tests, font=("Courier", 14), bg="dark green", fg="black")
                upload_tests_btn.place(x=170,y=160) #add and place upload button

                self.tests_status = Label(right_frame, text="Status: Tests File Not Selected", font=("Courier", 14), fg="red", bg="#d3d3b1")
                self.tests_status.place(x=100,y=210) #ass an dplace status label

                self.full_status = Label(right_frame, text="", font=("Courier", 14, "bold"), fg="dark green", bg="#d3d3b1")
                self.full_status.place(x=105,y=270) #place fill status lavel
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def import_students(self):
        "Asks user to select the students file and imports that information to the stundents file table (where the path is stored)"
        try:
            self.students_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Students File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            #ask to select a file
            
            if self.students_file_path: #if path is selected
                self.students_status.config(text="Status: Students File Selected!", fg="dark green") #change status bar text

                self.connection = sqlite3.connect(self.db_file)
                self.cursor = self.connection.cursor()

                self.cursor.execute('DROP TABLE IF EXISTS StudentsFile') #drop and create the studentsfile to holdthe path

                self.cursor.execute('''
                    CREATE TABLE StudentsFile (
                        id INTEGER PRIMARY KEY,
                        file_path TEXT NOT NULL
                    )
                ''')
                
                self.cursor.execute('INSERT INTO StudentsFile (file_path) VALUES (?)', (self.students_file_path,)) #add in the path

                self.connection.commit()

                self.students_status.place(x=90,y=100)
                self.check_both_files_selected() #check to see if both files were selected
                self.connection.close()
                
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def import_tests(self):
        "Asks user to select the tests file and imports that information to the tests file table (where the path is stored)"
        try:
            self.tests_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Test File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            #ask to select a file
            if self.tests_file_path: #if path selected
                self.tests_status.config(text="Status: Tests File Selected!", fg="dark green")

                self.connection = sqlite3.connect(self.db_file)
                self.cursor = self.connection.cursor()
                
                self.cursor.execute('DROP TABLE IF EXISTS TestsFile')  #drop and create the tests file to holdthe path

                self.cursor.execute('''
                    CREATE TABLE TestsFile (
                        id INTEGER PRIMARY KEY,
                        file_path TEXT NOT NULL
                    )
                ''')
                
                self.cursor.execute('INSERT INTO TestsFile (file_path) VALUES (?)', (self.tests_file_path,))  #add in the path

                self.connection.commit()


                self.tests_status.place(x=120,y=210)
                self.check_both_files_selected() #check to see if both files were selected

                self.connection.close()
                
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def check_both_files_selected(self):
        "Checks to see if both file paths were selected by the user, and if yes, changes the status bar and calls functions to add in the tables"
        try:
            students_status = self.students_status.cget("text")
            tests_status = self.tests_status.cget("text") #gets the status bar of both files

            if students_status == "Status: Students File Selected!" and tests_status == "Status: Tests File Selected!": #if both show selected
                self.full_status.config(text="Files Successfully Uploaded!\nChoose Actions from Menu Above")
                self.connection = sqlite3.connect(self.db_file)
                self.cursor = self.connection.cursor()
                link_data = MarkbookProcessor(self.students_file_path, self.tests_file_path, self.db_file) #call function to link data
                link_data.process_student_file()
                link_data.process_tests_file()
                link_data.create_and_insert_tables() #call all functions to link the data
                self.connection.close()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def validate_uploads(self):
        "Validates the uploads and prints the assignment warning depending on what still needs to be uploaded"
        try:
            if self.files_uploaded == False:
                    if self.students_status.cget("text") != "Status: Students File Selected!" and self.tests_status.cget("text") != "Status: Tests File Selected!":
                        showwarning("Files Not Selected", "Error: Select the Both Files before Proceeding") #warning if both files not selected
                    elif self.tests_status.cget("text") != "Status: Tests File Selected!" and self.students_status.cget("text") == "Status: Students File Selected!":
                        showwarning("File Not Selected", "Error: Select the Tests File before Proceeding") #warning if tests file not selected
                    elif self.students_status.cget("text") != "Status: Students File Selected!" and self.tests_status.cget("text") == "Status: Tests File Selected!":
                        showwarning("File Not Selected", "Error: Select the Student File before Proceeding")#warning if students file not selected
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def edit_students(self):
        "Occurs if the edit_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.edit_student_callback() #goes back to the edit student function in main page
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def edit_tests(self):
        "Occurs if the edit_tests is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.edit_tests_callback()
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def print_report(self):
        "Occurs if the print_report is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.print_report_callback()
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))  

    def update_students(self):
        "Occurs if the update_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.new_students_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Students File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
                #gets the new student file from the user
                if self.new_students_file_path: #if the file has been selected
                    self.connection = sqlite3.connect(self.db_file)
                    self.cursor = self.connection.cursor()

                    self.cursor.execute('SELECT file_path FROM TestsFile') #get the old tests file
                    self.old_tests_file_path = self.cursor.fetchone()
                    self.old_tests_file_path = self.old_tests_file_path[0]
                    
                    update_students = MarkbookProcessor(self.new_students_file_path, self.old_tests_file_path, self.db_file) #relink the data by creating the tables
                    update_students.process_student_file()
                    update_students.process_tests_file()
                    update_students.create_and_insert_tables()

                    showinfo("Successful Upload", "Students File Successfully Uploaded")
                    self.connection.close()
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def update_tests(self):
        "Occurs if the update_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.new_tests_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Students File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
                #gets the new tests file from the user
                if self.new_tests_file_path: #if the file has been selected
                    self.connection = sqlite3.connect(self.db_file)
                    self.cursor = self.connection.cursor()

                    self.cursor.execute('SELECT file_path FROM StudentsFile') #get the old students file
                    self.old_students_file_path = self.cursor.fetchone()
                    self.old_students_file_path = self.old_students_file_path[0]
                    
                    update_tests = MarkbookProcessor(self.old_students_file_path, self.new_tests_file_path, self.db_file) #relink the data by creating the tables
                    update_tests.process_student_file()
                    update_tests.process_tests_file()
                    update_tests.create_and_insert_tables()

                    showinfo("Successful Upload", "Tests File Successfully Uploaded")
                    self.connection.close()
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function           
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def export_students(self):
        "Occurs if the export_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                exportstudents = ExportingFunctions(self.db_file, self.cursor, self.connection) #calls the export function and exports students
                exportstudents.export_students()
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function          
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def export_tests(self):
        "Occurs if the export_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                exporttests = ExportingFunctions(self.db_file, self.cursor, self.connection) #calls the export function and exports tests
                exporttests.export_tests()
            else:
                self.validate_uploads()    #if status bar not proper, gets warning from validation function             
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 

    def edit_setup(self):
        "Occurs if the export_students is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.edit_setup_callback() #callsback to main if validated
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function   
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def seating_plan(self):
        "Occurs if the seating_plan is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.seating_page_callback() #callsback to main if validated
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function   
        except Exception as error: 
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def attendance_page(self):
        "Occurs if the attendance_page is pressed from the menu bar. Checks to make sure both tests and students file selected and then goes back to main page for future function calling"
        try:
            #validates the status bar to make sure selected
            if self.full_status.cget("text") == "Files Successfully Uploaded!\nChoose Actions from Menu Above" or self.full_status.cget("text") == "Status: Files Selected" "\n" + "Select an Action from the Menu!":
                self.attendance_page_callback() #callsback to main if validated
            else:
                self.validate_uploads() #if status bar not proper, gets warning from validation function   
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
