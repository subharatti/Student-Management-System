from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import os
import sys
import sqlite3
from datetime import datetime, timedelta

class AttendancePage():
    def __init__(self, db_file, frame):
        "Initialize the functions that will be used throughout (file, database)"
        try:
            self.db_file = db_file #initializes all the main variables used
            self.frame = frame
            self.selected_student = None
            self.create_attendance_table()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def create_attendance_table(self):
        "Creates the Attendance table in the database (won't exist on inital run)"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            #create the attendance table (it wont be autocreated because it doesn't exist), add an id to access the attendace record
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT,
                    date TEXT,
                    current_attendance TEXT,
                    total_lates INTEGER,
                    total_absences INTEGER,
                    total_presents INTEGER
                )
            ''')

            conn.commit()
            conn.close()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def create_listbox(self):
        "Create the listbox holding all the students for the user to select from"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            self.students_listbox = Listbox(self.frame, selectmode=SINGLE, font=("Courier", 14), width=20, bg="#b1caa4") #created the listbox to hold the students
            self.students_listbox.place(x=20, y=10)

            cursor.execute("SELECT * FROM Students") #select all the student into from the stiudents file
            students_data = cursor.fetchall()

            for student in students_data:
                student_name = student[2] #get the student name, its the third item 
                self.students_listbox.insert(END, student_name) #add name to the listbox

            conn.close()

            self.students_listbox.bind("<<ListboxSelect>>", self.on_student_selected) #bind the listbox to this function so its executed when the studetns selected

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def create_treeview(self):
        "Create the treeview to hold all the Attendance information"
        try:
            mycolumns = ["Date", "Current Attendance", "Total Lates", "Total Absences", "Total Presents"] #creates columns for the attendance treeview

            style = ttk.Style()  #this adds style to the treeview, where I can add a theme to make it more appealing, and change out the colours aswell
            style.theme_use("clam")
            style.configure("Treeview", background="#b1caa4", 
                    fieldbackground="#b1caa4", foreground="black", font=("Courier",10))
            style.configure('Treeview.Heading', background="#7ca666", font=("Courier",10)) #configures the style to the treeview

            self.tree = ttk.Treeview(self.frame, columns=mycolumns, show="headings", selectmode="browse") #create the treeview to hold attendance records
            self.tree.place(x=270, y=10)

            for column in mycolumns:
                self.tree.column(column, anchor=CENTER, width=120) #adds the columns and headings (center means it is in the middle)
                self.tree.heading(column, text=column, anchor=CENTER)

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def on_student_selected(self, event):
        "Function binded to listbox student select to commands to update combobox and current attendance"
        try:
            selected_index = self.students_listbox.curselection() #if there is a selection
            if selected_index:
                student_name = self.students_listbox.get(selected_index) #get the selected student name
                self.selected_student = student_name

                attendance_data = self.fetch_attendance_data(student_name) #get attendance info for that student (calls function)
                self.display_attendance_data(attendance_data) #display the attendace in the treeview (calls function)

                current_attendance = self.fetch_current_attendance(student_name)
                self.current_attendance_combobox.set(current_attendance) #sets the attendance listbox
                self.current_attendance_selection = current_attendance #update attendance selection

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def fetch_attendance_data(self, student_name):
        "Gets the attendance data for the specific selected student when called"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Attendance WHERE student_name=?", (student_name,)) #goes through Attendance table to fetch all data for student
            attendance_data = cursor.fetchall()

            conn.close()

            return attendance_data #returns to called variable

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def fetch_current_attendance(self, student_name):
        "Gets the current attendance for the specific selected student when called"
        try:
            conn = sqlite3.connect(self.db_file) 
            cursor = conn.cursor()

            cursor.execute("SELECT current_attendance FROM Attendance WHERE student_name=?", (student_name,)) #get the current attendance for the student name
            current_attendance = cursor.fetchone()
            if current_attendance:
                return current_attendance[0] #extracts the attendance (single the fetchone returns a tuple)
            else:
                return '' #returns empty string if no current attendance

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def entry_exists_for_date(self, student_name, today_date):
        "Fetches the attendance information on today's date for if the student does exist" 
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Attendance WHERE student_name=? AND date=?", (student_name, today_date)) #selects information for student using today's date
            existing_entry = cursor.fetchone()

            conn.close()

            return existing_entry is not None #returns none if entry with that date doesnt exist

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def display_attendance_data(self, attendance_data):
        "Displays the attendace records on the treeview"
        try:
            for item in self.tree.get_children():
                self.tree.delete(item) #delete the item in the treeview if exisist (get rid of old value)

            if attendance_data:
                for record in attendance_data:
                    self.tree.insert("", "end", values=record[2:]) #add the values, starting from third item (date)

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def update_attendance_data(self):
        "Updates the attendance record with new current attendance when a change is made"
        try:
            if self.selected_student:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()

                today_date = datetime.today().strftime('%Y-%m-%d') #using datetime module, gets date and time in year-month-date form
                
                if self.entry_exists_for_date(self.selected_student, today_date): #if there is an entry to the today day, work to edit it
                    current_attendance = self.current_attendance_combobox.get() 

                    if current_attendance != self.current_attendance_selection:
                            today_day_info = today_date.split("-")
                            year = int(today_day_info[0])
                            month = int(today_day_info[1])
                            day = int(today_day_info[2]) #split the information to get year,motn-date

                            if day == 1:
                                if month == 1: #check all these parameters to obtain the previoys day info
                                    year -= 1
                                    month = 12
                                else:
                                    month -= 1
                                    if month in [1, 3, 5, 7, 8, 10, 12]:
                                        day = 31
                                    elif month == 2:
                                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0): #checks for leap year
                                            day = 29 
                                        else:
                                            day = 28
                                    else:
                                        day = 30

                            else:
                                day -= 1

                            previous_day_str = f"{year:04d}-{month:02d}-{day:02d}" #convert previous day info into string
                            cursor.execute('''
                                SELECT current_attendance, total_lates, total_absences, total_presents
                                FROM Attendance
                                WHERE student_name = ? AND date = ?
                            ''', (self.selected_student, previous_day_str)) #get attendance info of student for previous day

                            previous_day_data = cursor.fetchone()
                            if previous_day_data == None: #if there isnt information for the previous day, then all values begin with 0 
                                presents =0
                                lates = 0
                                absences = 0
                            else:            
                                presents = int(previous_day_data[3]) #if there is, split them accordining
                                lates = int(previous_day_data[1])
                                absences = int(previous_day_data[2])
      
                            if current_attendance == 'P': #updates database if P is selected
                                cursor.execute('UPDATE Attendance SET total_presents = ? WHERE student_name=? AND date=?', (presents + 1, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_lates = ? WHERE student_name=? AND date=?', (lates, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_absences = ? WHERE student_name=? AND date=?', (absences, self.selected_student, today_date))

                            elif current_attendance == 'A': #updates database if A is selected
                                cursor.execute('UPDATE Attendance SET total_presents = ? WHERE student_name=? AND date=?', (presents, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_lates = ? WHERE student_name=? AND date=?', (lates, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_absences = ? WHERE student_name=? AND date=?', (absences +1, self.selected_student, today_date))
                            elif current_attendance == 'L': #updates database if L is selected
                                cursor.execute('UPDATE Attendance SET total_presents = ? WHERE student_name=? AND date=?', (presents, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_lates = ? WHERE student_name=? AND date=?', (lates+ 1, self.selected_student, today_date))
                                cursor.execute('UPDATE Attendance SET total_absences = ? WHERE student_name=? AND date=?', (absences, self.selected_student, today_date))

                            self.current_attendance_selection = current_attendance #updates attendance selection

                else:
                    today_day_info = today_date.split("-")
                    year = int(today_day_info[0])
                    month = int(today_day_info[1])
                    day = int(today_day_info[2])

                    if day == 1:
                        if month == 1:  #check all these parameters to obtain the previoys day info
                            year -= 1
                            month = 12
                        else:
                            month -= 1
                            if month in [1, 3, 5, 7, 8, 10, 12]:
                                day = 31
                            elif month == 2:
                                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0): #checks for leap year
                                    day = 29  
                                else:
                                    day = 28 
                            else:
                                day = 30

                    else:
                        day -= 1

                    previous_day_str = f"{year:04d}-{month:02d}-{day:02d}" #convert previous day info into string


                    cursor.execute('''
                        SELECT current_attendance, total_lates, total_absences, total_presents
                        FROM Attendance
                        WHERE student_name = ? AND date = ?
                    ''', (self.selected_student, previous_day_str))

                    previous_day_data = cursor.fetchone() #get attendance info of student for previous day

                    if previous_day_data:
                        presents = int(previous_day_data[3])  #if there is, split them accordining
                        lates = int(previous_day_data[1])
                        absences = int(previous_day_data[2])
                        cursor.execute('''
                            INSERT INTO Attendance (student_name, date, current_attendance, total_lates, total_absences, total_presents)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            self.selected_student,
                            today_date,
                            self.current_attendance_combobox.get(),
                            lates,  # use total_lates from the previous day
                            absences,  # use total_absences from the previous day
                            presents   # use total_presents from the previous day
                        ))
                    else:
                        #if no data for the previous day, insert with default values
                        cursor.execute('''
                            INSERT INTO Attendance (student_name, date, current_attendance, total_lates, total_absences, total_presents)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            self.selected_student,
                            today_date,
                            self.current_attendance_combobox.get(),
                            0,
                            0,
                            0
                        ))
                    current_attendance = self.current_attendance_combobox.get()
                    if current_attendance == 'P':  #updates database if P is selected
                        cursor.execute('UPDATE Attendance SET total_presents = total_presents + 1 WHERE student_name=? AND date=?', (self.selected_student, today_date))
                    elif current_attendance == 'A':  #updates database if A is selected
                        cursor.execute('UPDATE Attendance SET total_absences = total_absences + 1 WHERE student_name=? AND date=?', (self.selected_student, today_date))
                    elif current_attendance == 'L':  #updates database if L is selected
                        cursor.execute('UPDATE Attendance SET total_lates = total_lates + 1 WHERE student_name=? AND date=?', (self.selected_student, today_date))

                    self.current_attendance_selection = current_attendance  # update current selection

                #reupdates the student and their current attedance selection (the new one they chose)
                cursor.execute('UPDATE Attendance SET current_attendance = ? WHERE student_name=? AND date=?', ( self.current_attendance_selection, self.selected_student, today_date))

                conn.commit()
                conn.close()
                
                attendance_data = self.fetch_attendance_data(self.selected_student) #fetched new attendaced data
                self.display_attendance_data(attendance_data) #displaying new attendance data 

                
                self.update_treeview_cell(today_date, "Current Attendance", self.current_attendance_selection) #updates the current attendance treeview cell for student

                

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))


    def update_treeview_cell(self, date, column, new_value):
        "Update the current attendance treeview cell when the current attendance is changed for a student"
        try:
            item_id = None
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == date: #find the item with the todays date and get the id
                    item_id = item
                    break

            if item_id:
                values = self.tree.item(item_id, 'values')
                values = list(values) 
                column_index = self.tree['columns'].index(column) #gets the current attendance colum  index
                values[column_index] = new_value #updated the value using the new test id
                self.tree.item(item_id, values=values)
                
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def place_elements(self):
        "Places all display elements on the screen and formats them accordingly"
        try:
            self.create_listbox() #run the treeview and listbox functions
            self.create_treeview()

            Label(self.frame, text="Current Attendance", font=("Courier", 14), fg="dark green", bg="#d3d3b1").place(x=20, y=310)
            self.current_attendance_combobox = ttk.Combobox(self.frame, values=['P', 'A', 'L'], font=("Courier", 14), state="readonly") #Create the label and combobox for current attendance
            self.current_attendance_combobox.place(x=230, y=310)

            self.save_button = Button(self.frame, font=("Courier", 14), text="Save", fg="black", bg="dark green", command=self.update_attendance_data) #created and adds funtionaility to save button
            self.save_button.place(x=500, y=305)
            
        except Exception as error:
                print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
