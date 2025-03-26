from tkinter import *
from tkinter import messagebox
import sqlite3

class SeatingPage(Tk):
    def __init__(self, db_file, frame):
        "Initalize the vairbales thar will be used throughout the program"
        self.db_file = db_file
        self.frame = frame #created the variables to be used throughout

        self.conn = sqlite3.connect(self.db_file)
        
        with self.conn: #create the seating_arrangement table if it doesn't exist
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS seating_arrangement (
                    student_name TEXT PRIMARY KEY,
                    row INTEGER,
                    col INTEGER
                )
            ''')

        self.selected_student = None
        self.students_per_row_var = StringVar() #string variable since using student names
        self.students_per_row_var.set("3") #inital is always three

        self.buttons = []

        self.student_names = self.fetch_student_names() #gets the student names

        #create buttons for each student using grid
        self.create_widgets()

        #load the seating arrangement from the database
        self.load_arrangement()


    def fetch_student_names(self):
        "Fetches student names from the Students table"
        with self.conn: 
            cursor = self.conn.execute('SELECT name FROM Students') #gets all names from the student table
            return [row[0] for row in cursor.fetchall()]

    def create_widgets(self):
        "Creates and placed all the widgets on the page"
        #entry for the user to specify students per row
        entry_label = Label(self.frame, text="Students Per Row:", font=("Courier", 13), fg="black", bg="#d3d3b1")
        entry_label.grid(row=0, column=0, pady=10)

        entry_students_per_row = Entry(self.frame, textvariable=self.students_per_row_var,  font=("Courier", 14), fg="black", bg="#b1caa4", width=3)
        entry_students_per_row.grid(row=0, column=1, pady=10)

        #button to update arrangement
        update_button = Button(self.frame, text="Update Arrangement", command=self.update_arrangement, font=("Courier", 14), bg="#d1fdd1", fg="black")
        update_button.grid(row=0, column=2, pady=10)

        #create buttons for each student using grid
        for i, student_name in enumerate(self.student_names):
            button = Button(self.frame, text=student_name, command=lambda i=i: self.select_student(i),
                               font=("Courier", 16), bg="dark green", fg="black")
            self.buttons.append(button)
            button.grid(row=i // int(self.students_per_row_var.get()) + 1, column=i % int(self.students_per_row_var.get()),
                        padx=20, pady=20)  #using grid for better layout control

    def select_student(self, student_index):
        "Get the selected student and inform user who was selected"
        if self.selected_student is None:
            self.selected_student = student_index #uses the index to find selected student
            messagebox.showinfo("Selected", f"{self.student_names[student_index]} selected") #tells user who was selected
        else:
            self.swap_seats(self.selected_student, student_index)
            self.selected_student = None

    def swap_seats(self, index1, index2):
        "Swaps the postions of the two students"
        students_per_row = int(self.students_per_row_var.get())
        row1, col1 = index1 // students_per_row, index1 % students_per_row #caluclated the positions of the students
        row2, col2 = index2 // students_per_row, index2 % students_per_row

        #updates the database with the new seating arrangement
        with self.conn: #creates the table if it doesnr exist
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS seating_arrangement (
                    student_name TEXT PRIMARY KEY,
                    row INTEGER,
                    col INTEGER
                )
            ''')
            self.conn.execute('''
                UPDATE seating_arrangement
                SET row = ?, col = ?
                WHERE student_name = ?
            ''', (row2 + 1, col2, self.student_names[index1])) #uses rows and columns defined before

            self.conn.execute('''
                UPDATE seating_arrangement
                SET row = ?, col = ?
                WHERE student_name = ?
            ''', (row1 + 1, col1, self.student_names[index2]))  #uses rows and columns defined before
 
        #update the format of where the buttons are placed
        self.buttons[index1].grid(row=row2 + 1, column=col2, padx=20, pady=20, sticky="nsew")
        self.buttons[index2].grid(row=row1 + 1, column=col1, padx=20, pady=20, sticky="nsew")

    def update_arrangement(self):
        "Updates the arrangement when the button is clicked"
        row, col = 1, 0
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            col += 1
            if col == int(self.students_per_row_var.get()):
                col = 0
                row += 1

        #save the new seating arrangement to the database
        with self.conn:
            self.conn.execute('DELETE FROM seating_arrangement')

            for i in range(len(self.buttons)):
                button = self.buttons[i]
                row, col = i // int(self.students_per_row_var.get()) + 1, i % int(self.students_per_row_var.get())  #uses rows and columns defined before
                self.conn.execute('''
                    INSERT INTO seating_arrangement (student_name, row, col)
                    VALUES (?, ?, ?)
                ''', (self.student_names[i], row, col)) #adds to the table


    def load_arrangement(self):
        "Loads the seating arrangement from the database"
        with self.conn:
            cursor = self.conn.execute('SELECT student_name, row, col FROM seating_arrangement')
            for row in cursor: #get all the infomation and split it
                student_name, row, col = row
                try:
                    index = self.student_names.index(student_name)
                    self.buttons[index].grid_forget()  # forget the previous grid location
                    self.buttons[index].grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
                except ValueError:
                    pass  #ignore if the student name is not in the current list

    def close_connection(self):
        "Close the database connection"
        if self.conn:
            self.conn.close()
