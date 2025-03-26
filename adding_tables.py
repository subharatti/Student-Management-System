import csv
import os
import sys
import sqlite3

class MarkbookProcessor:
    def __init__(self, student_file_path, tests_file_path, db_file_path):
        "This initalizes all my main functions that are needed to process the data (file paths, etc.)"
        try: 
            self.student_file_path = student_file_path #initialize the paths used plus future variables to use (data, tests)
            self.tests_file_path = tests_file_path
            self.db_file_path = db_file_path
            self.students_data = {}
            self.tests_data = {}
            self.current_test = None
            self.header_processed = False 
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def process_student_file(self):
        "Proccess the student file by opening the selected path and extracting the data"
        try:
            with open(self.student_file_path, newline="") as csvfile: #open the file as a csv file
                reader = csv.reader(csvfile)

                first_row = True

                for row in reader: #skip the header 
                    if first_row:
                        first_row = False
                        continue

                    first_name, last_name, student_number, *phone_number = row
                    phone_number = phone_number[0] if phone_number else None #assigns the values (if the phone_number wasnt in the file, set to None

                    self.students_data[student_number] = {
                        'Name': f'{first_name} {last_name}',
                        'Tests': {},
                        'Phone_Number': phone_number #add the data to the student data dictionary where key is student number
                    }
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def process_tests_file(self):
        "Process the test file by opening the selected path and extracting the data"
        try:
            self.tests_data = {}
            self.current_test = None
            self.header_processed = False #creates these variables to hold test data

            with open(self.tests_file_path, newline="") as csvfile:
                reader = csv.reader(csvfile) #open the tests file as a csv file

                for row in reader:
                    if not self.header_processed: #skip the header
                        self.header_processed = True
                        continue

                    if len(row) >= 4: #if the row is a test header, assign and add the into to the test data
                        if self.current_test is None and self.tests_data == {}: #adds if there is a test + no previous info
                            test_info = {'Category': row[1], 'Weight': int(row[2]), 'OutOf': int(row[3])}
                            self.current_test = row[0]
                            self.tests_data[self.current_test] = test_info
                        elif self.current_test: #adds if there is a test
                            test_info = {'Category': row[1], 'Weight': int(row[2]), 'OutOf': int(row[3])}
                            self.current_test = row[0]
                            self.tests_data[self.current_test] = test_info
                        self.current_test = row[0]

                    elif len(row) == 2 and self.current_test: #if the row is a mark for a stundet, add it to to the stundets data dictionary
                        student_number, mark = row 
                        self.students_data[student_number]['Tests'][self.current_test] = mark
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def create_and_insert_tables(self):
        "Creates the tables within the database and populating the tables"
        try:
            with sqlite3.connect(self.db_file_path) as conn: #sets up the connection
                cursor = conn.cursor()

                self._drop_tables(cursor) #calls the function to drop the tables if they exist

                #create the students table with the values (plus autoincrement id so i can access it globally)
                cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS Students (
                        id INTEGER PRIMARY KEY,
                        student_number TEXT UNIQUE,
                        name TEXT,
                        phone_number TEXT
                    )
                ''')

                #create the tests table with the values (plus autoincrement id so i can access it globally)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Tests (
                        id INTEGER PRIMARY KEY,
                        test_name TEXT UNIQUE,
                        category TEXT,
                        weight INTEGER,
                        out_of INTEGER
                    )
                ''')

                #create the marks table with the values (plus autoincrement id so i can access it globally, uses the student and tests ids)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Marks (
                        id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        test_id INTEGER,
                        mark REAL
                    )
                ''')

                for student_number, data in self.students_data.items():
                    cursor.execute('INSERT INTO Students (student_number, name, phone_number) VALUES (?, ?, ?)',
                                   (student_number, data['Name'], data['Phone_Number'])) #add the student into in
                    student_id = cursor.lastrowid #gets the id, the one thats the key/autoincremented

                    for test_name, test_info in self.tests_data.items(): #check if the test already exists in the tests table
                        cursor.execute('SELECT id FROM Tests WHERE test_name = ?', (test_name,)) 
                        existing_test = cursor.fetchone()

                        if existing_test: 
                            test_id = existing_test[0] #if it exists then change the test id
                        else:
                            # If the test doesn't exist, insert it into the tests table
                            cursor.execute('INSERT INTO Tests (test_name, category, weight, out_of) VALUES (?, ?, ?, ?)',
                                           (test_name, test_info.get('Category', ''), test_info.get('Weight', 0),
                                            test_info.get('OutOf', 0)))
                            test_id = cursor.lastrowid

                        mark = data['Tests'].get(test_name)
                        if mark is not None: #if the test isnt in the students file, add in the mark for the stufent
                            cursor.execute('INSERT INTO Marks (student_id, test_id, mark) VALUES (?, ?, ?)',
                                           (student_id, test_id, mark))

                conn.commit()
                
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 


    def _drop_tables(self, cursor):
        "Drops the tables to make sure no errors occur"
        try: #commands to drop all the needed tables
            cursor.execute('DROP TABLE IF EXISTS Marks')
            cursor.execute('DROP TABLE IF EXISTS Students')
            cursor.execute('DROP TABLE IF EXISTS Tests')
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno)) 
