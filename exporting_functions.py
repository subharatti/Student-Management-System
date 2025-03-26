from tkinter import *
from tkinter import ttk
import sys
import os
import sqlite3
import csv
from tkinter.messagebox import *
from tkinter import filedialog
from students_page import StudentPage
from adding_tables import MarkbookProcessor


class ExportingFunctions:
    def __init__(self, db_file_path, cursor, connection):
        "Initialize variables to be used throughout the program (file, etc.)"
        try:
            self.db_file = db_file_path
            self.cursor = cursor
            self.connection = connection #assigns variables that will be used through program

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def export_students(self):
        "Exports the students by fetching the data for the student, and writing it to a new text file with the formatted rows"
        try:
            conn = sqlite3.connect(self.db_file)
            self.cursor = conn.cursor()
            self.cursor.execute('SELECT name, student_number, phone_number FROM Students') #select all the information corresponing to the student to be exported

            rows = self.cursor.fetchall()

            with open("students_exported.txt", 'w', newline='') as csvfile: #write to a new text file
                csv_writer = csv.writer(csvfile)

                csv_writer.writerow(['[First Name', 'Last Name', 'Student Number', 'Phone Number]']) #add the header row

                for row in rows:
                    full_name, student_number, phone_number = row #split the first, last name, and student number and phonenumber
                    full_name = full_name.split(" ")
                    first_name = full_name[0]
                    last_name = full_name[1]
                    csv_writer.writerow([first_name, last_name, student_number, phone_number]) #write the information into the row

            showinfo("Export Successfull",f"Student information exported to folder containing this program, titled 'students_exported.txt'") #showinfo that exported txt file
            conn.close()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def export_tests(self):
        "Exports the tests by fetching the data for the test, and writing it to a new text file with the formatted rows"
        try:
            conn = sqlite3.connect(self.db_file)
            self.cursor = conn.cursor()

            self.cursor.execute("SELECT id, test_name, category, weight, out_of FROM Tests") #select all the information corresponing to the test to be exported
            test_rows = self.cursor.fetchall()

            self.cursor.execute("SELECT test_id, student_id, mark FROM Marks") #select the student and test id from marks to get the marks of the students
            mark_rows = self.cursor.fetchall()

            with open("tests_exported.txt", 'w', newline='') as csvfile: #write to a new text file
                csv_writer = csv.writer(csvfile)

                csv_writer.writerow(['[Test Title', 'Test Category', 'Test Weight', 'Test Out Of]']) #write the header line

                for test_row in test_rows:
                    test_id, test_name, category, weight, out_of = test_row #split the row info the correspoining varavles
                    csv_writer.writerow([test_name, category, weight, out_of]) #write the text header

                    for mark_row in mark_rows: #now aloso check for the marks row (where we retrived marks info)
                        if mark_row[0] == test_id:  #check if test_id matches
                            student_id = mark_row[1] #if matched, get the student id and mark (assign index)
                            mark = mark_row[2]

                            self.cursor.execute("SELECT student_number FROM Students WHERE id = ?", (student_id,)) #get student number from Students table
                            student_number = self.cursor.fetchone()[0]

                            csv_writer.writerow([student_number, mark]) #write the row with the student number and mark

            showinfo("Export Successful", "Test information exported to 'tests_exported.txt'")  #showinfo that exported txt file
            conn.close()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
