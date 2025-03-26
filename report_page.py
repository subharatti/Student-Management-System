from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import os
import sys
import sqlite3
from adding_tables import MarkbookProcessor


class ReportPage():
    def __init__(self, db_file, frame):
        "Initalize all the variables that will be used throughout the program"
        try:
            self.db_file = db_file #assign the vairbales to be used throughout the program
            self.frame = frame
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def place_elements(self):
        "Place all the widgets and format them accordingly"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM Students") #get all the student names
            self.student_names = [row[0] for row in cursor.fetchall()] #make student names list
            conn.close()

            self.listbox = Listbox(self.frame, selectmode="single", font=("Courier", 12), fg="black", bg="#b1caa4")
                
            self.listbox.bind("<<ListboxSelect>>", self.calculate_average) #bind the listbox to a function when item selected

            scrollbar = Scrollbar(self.frame, command=self.listbox.yview)
            scrollbar.place(x=247, y=50, relheight=0.6) #make scrollbar and set to listbox
            self.listbox.config(yscrollcommand=scrollbar.set)

            #placing all the labels and canvas
            label = Label(self.frame, text="Select a student:", font=("Courier", 14), fg="black", bg="#d3d3b1")
            label.place(x=35, y=20) 

            self.listbox.place(x=20, y=50, relwidth=0.25, relheight=0.6)
            self.auto_calculate_averages()

            self.student_lbl = Label(self.frame, text="", font=("Courier", 14), fg="black", bg="#d3d3b1")
            self.student_lbl.place(x=140, y=450, anchor="center")            
            
            self.student_average_lbl = Label(self.frame, text="", font=("Courier", 20, "bold"), fg="dark green", bg="#d3d3b1")
            self.student_average_lbl.place(x=148, y=490, anchor="center")

            self.class_average_function()

            self.classaverage_lbl = Label(self.frame, text= f"Class Average: {self.class_ave}%", font=("Courier", 20, "bold"), fg="red", bg="#d3d3b1")
            self.classaverage_lbl.place(x=550, y=20, anchor="center")

            self.canvas = Canvas(self.frame, width=500, height=150, bg="#d3d3b1") #canvas for line graph
            self.canvas.place(x=330,y=50)

            self.canvas2 = Canvas(self.frame, width=500, height=200, bg="#d3d3b1")#canvas for bargraph
            self.canvas2.place(x=330,y=280)

            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def auto_calculate_averages(self):
        "Automatically calculated the average of all students and places beside their name in the listbox"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            self.class_average = 0
            
            for student in self.student_names:
                cursor.execute("SELECT id FROM Students WHERE name=?", (student,)) #get the studebt id
                student_id = cursor.fetchone()
                
                if not student_id:
                    return #if no id then break

                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Marks WHERE student_id=?", student_id) #get all marks for the student
                marks_info = cursor.fetchall()

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 Name",)) #get the category names and percentages
                category1_name = cursor.fetchone()
                category1_name = category1_name[0]

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 Name",))
                category2_name = cursor.fetchone()
                category2_name = category2_name[0]

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 %",))
                category1_percent = cursor.fetchone()
                category1_percent = int(category1_percent[0])/100

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 %",))
                category2_percent = cursor.fetchone()
                category2_percent = int(category2_percent[0])/100
                
                category1_marks = 0
                category2_marks = 0
                category1_weights = 0
                category2_weights = 0

                for info in marks_info:
                    mark = info[3]
                    if not mark:
                        continue #make sure mark is given
                    mark = int(mark)#convert to integer
                    test_id = info[2]
                    cursor.execute("SELECT id, test_name, category, weight, out_of from Tests where id=?", (test_id,)) #get the test info based on the id
                    test_info = cursor.fetchone() #break down info into parts (info is the line with test info)
                    category = test_info[2]
                    weight = int(test_info[3])
                    out_of = int(test_info[4])

                    total_mark = (mark/out_of)*weight #get the total mark for that test

                    if category1_name == category: #if the category matches with category1 name in setup
                        category1_marks += total_mark  #add marks to category1 marks
                        category1_weights += weight #add weight to category 1 weights
                    if category2_name == category: #if the category matches with category2 name in setup
                        category2_marks += total_mark #add marks to category2 marks
                        category2_weights += weight #add weight to category 2 weights

                category1_total = (category1_marks/category1_weights) * category1_percent #find the category 1 total mathmatically
                category2_total = (category2_marks/category2_weights) * category2_percent #find the category 2 total mathematically
                self.average = round((category1_total+category2_total)*100, 2) #get the student avergae
                formatted_student = student + " - " + str(self.average) + "%" #format the student to be added to listbox
                self.listbox.insert(END, formatted_student) #add to the listbox
                
            conn.commit()
            conn.close()
            
            self.class_ave = round(self.class_average / len(self.student_names), 2) #get the total place average aswell
            
        except ZeroDivisionError:
            showwarning("Error", "Cannot print student overage due to error in marks provided")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def class_average_function(self):
        "Calculated the class average by finding average for each student and adding to variable called class average"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            self.class_average = 0
            
            for student in self.student_names:
                cursor.execute("SELECT id FROM Students WHERE name=?", (student,)) #get student id for student
                student_id = cursor.fetchone()
                
                if not student_id:
                    return

                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Marks WHERE student_id=?", student_id) #get marks
                marks_info = cursor.fetchall()

                #get category name and percentage info
                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 Name",))
                category1_name = cursor.fetchone()
                category1_name = category1_name[0]

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 Name",))
                category2_name = cursor.fetchone()
                category2_name = category2_name[0]

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 %",))
                category1_percent = cursor.fetchone()
                category1_percent = int(category1_percent[0])/100

                cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 %",))
                category2_percent = cursor.fetchone()
                category2_percent = int(category2_percent[0])/100
                
                category1_marks = 0 #variables to hold total marks and weights
                category2_marks = 0
                category1_weights = 0
                category2_weights = 0

                for info in marks_info:
                    mark = info[3]
                    if not mark:
                        continue #make sure mark is there or else skip
                    mark = int(mark) #make sure mark is integer
                    test_id = info[2]
                    cursor.execute("SELECT id, test_name, category, weight, out_of from Tests where id=?", (test_id,))
                    test_info = cursor.fetchone() #get the test info and break info parts
                    category = test_info[2]
                    weight = int(test_info[3])
                    out_of = int(test_info[4])

                    total_mark = (mark/out_of)*weight #calcualte the total_mark

                    if category1_name == category: #add to category dependsing on which name matched
                        category1_marks += total_mark
                        category1_weights += weight
                    if category2_name == category:
                        category2_marks += total_mark
                        category2_weights += weight

                category1_total = (category1_marks/category1_weights) * category1_percent #calculate category 1 total
                category2_total = (category2_marks/category2_weights) * category2_percent #calculate categroy 2 total
                self.average = round((category1_total+category2_total)*100, 2) #get class average
                self.class_average += self.average #add to class avaergae
                
            conn.commit()
            conn.close()
            
            self.class_ave = round(self.class_average / len(self.student_names), 2) #find class average
            
        except ZeroDivisionError:
            showwarning("Error", "Cannot print student overage due to error in marks provided")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
        
    def calculate_average(self, event):
        "Calculate the average of each individual student to be displaying in a Label and onward when clicked on"
        try:
            selected_item_index = self.listbox.curselection() #get the student selected
            if not selected_item_index: 
                return #if no item selected then break
            selected_student_name = self.listbox.get(selected_item_index)
            selected_student_name = selected_student_name.split(" - ") #get the student name by spliting the listbox title of item
            selected_student_name = selected_student_name[0]

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Students WHERE name=?", (selected_student_name,)) #get the id for the student
            student_id = cursor.fetchone()
            conn.close()

            if not student_id:
                return #if no id then break

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Marks WHERE student_id=?", student_id) #get marks for student
            marks_info = cursor.fetchall()

            #get category info for student
            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 Name",))
            category1_name = cursor.fetchone()
            category1_name = category1_name[0]

            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 Name",))
            category2_name = cursor.fetchone()
            category2_name = category2_name[0]

            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 1 %",))
            category1_percent = cursor.fetchone()
            category1_percent = int(category1_percent[0])/100

            cursor.execute("SELECT value FROM setup WHERE key=?", ("Category 2 %",))
            category2_percent = cursor.fetchone()
            category2_percent = int(category2_percent[0])/100
            
            category1_marks = 0 #create vairbales to hold info
            category2_marks = 0
            category1_weights = 0
            category2_weights = 0

            for info in marks_info:
                mark = info[3]
                if not mark:
                    continue #if no mark then break
                mark = int(mark) #make sure mark is integer
                test_id = info[2]
                cursor.execute("SELECT id, test_name, category, weight, out_of from Tests where id=?", (test_id,))
                test_info = cursor.fetchone()
                category = test_info[2] #get test info and break into parts
                weight = int(test_info[3])
                out_of = int(test_info[4])

                total_mark = (mark/out_of)*weight #get total mark

                if category1_name == category: #add to corresponing category
                    category1_marks += total_mark
                    category1_weights += weight
                if category2_name == category:
                    category2_marks += total_mark
                    category2_weights += weight

            category1_total = (category1_marks/category1_weights) * category1_percent #get category total
            category2_total = (category2_marks/category2_weights) * category2_percent #get category total
            self.average = str(round((category1_total+category2_total)*100, 2)) 

            self.student_lbl.config(text=f" {selected_student_name}'s Average") #change label to hold student name 
            self.student_average_lbl.config(text=f"{self.average}%") #and add there average to the average label

            self.bar_graph() #call function to create bar graph
            self.line_graph() #call function to create line graoh
            
            conn.commit()

            conn.close()
        except  ZeroDivisionError:
            showwarning("Error", "Cannot print student overage due to error in marks provided")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def bar_graph(self):
        "Create a bargraph for the selected student using their marks information"
        selected_student = self.listbox.curselection()

        if selected_student:
            result = selected_student[0] + 1 #get the result for the student

            if result:
                self.student_id = result

                marks_data = self.get_student_marks() #get the marks info

                self.canvas.delete('all') #clear the canvas

                canvas_width = 500
                canvas_height = 150

                numeric_marks = [mark for test_name, mark in marks_data if type(mark) in {int, float}] #filters out non-numeric marks and calculate max_mark
                max_mark = max(numeric_marks, default=1) #default to 1 if there are no numeric marks

                normalized_marks = [mark / max_mark * (canvas_height - 20) if type(mark) in {int, float} else "" for _, mark in marks_data] #normalize marks to fit within canvas height scale (so it doesnt overlap)

                bar_width = min((canvas_width - 30) / 7, canvas_width / len(marks_data) / 2) #calculated bar width
                gap = bar_width + 2 #create variableto hold the gap

                left_margin = 30

                i = 0
                for test_name, normalized_mark in marks_data:
                    x1 = left_margin + i * (bar_width + gap) #calculate the x corrdiant by adding the left marigen and the test mark with the width and gap
                    y1 = canvas_height - normalized_mark if type(normalized_mark) in {int, float} else canvas_height #calculate the y accordingly
                    x2 = x1 + bar_width #strecthes the bar to width of bar defined before
                    y2 = canvas_height #height is the canvas height

                    if type(normalized_mark) in {int, float}:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='dark green') #create the bar
                    self.canvas.create_text((x1 + x2) / 2, y1 - 5, text=test_name, anchor='s') #add the text ontop
                    i += 1
            else:
                print(f"No matching student found for '{selected_student}'")
                
    def line_graph(self):
        "Create a linegraph for the selected student using their marks information"
        selected_student = self.listbox.curselection()

        if selected_student:
            result = selected_student[0] + 1

            if result:
                self.student_id = result #get the student mark and name (call the function that linkes the test and marks)

                marks_data = self.get_student_marks() 

                self.canvas2.delete('all') #clear canvas

                canvas_width = 500 #canvas heights/widths
                canvas_height = 200

                numeric_marks = [mark for _, mark in marks_data if type(mark) in (int, float)] #filters out non-numeric marks and calculate max_mark
                max_mark = max(numeric_marks, default=1)  #default to 1 if there are no numeric marks

                normalized_marks = [
                    mark / max_mark * (canvas_height - 20) if type(mark) in (int, float) else None #normalize marks to fit within canvas height scale (so it doesnt overlap)
                    for _, mark in marks_data
                ]

                canvas_height -= 30

                point_spacing = canvas_width / (len(marks_data) + 1) #calculate point spacing depending on how many tests

                previousx = 0
                previousy = 0
                i = 1
                for test_name, normalized_mark in marks_data:
                    x = i * point_spacing
                    y = canvas_height - normalized_mark if type(normalized_mark) in (int, float) else None #as long as the test is actually there (not a "" string)

                    if type(normalized_mark) in (int, float):
                        self.canvas2.create_oval(x - 5, y - 5, x + 5, y + 5, fill='dark green') #draw the dot, where the subtarcts 5 from the x and y (subtract 5 from x to make
                                                                                                #sure it fits in the canvas, and the additions of x just add 5 to the mark to fit in canvas scale
                        self.canvas2.create_text(x, y - 10, text=f"{test_name}\n{normalized_mark:.2f}", anchor='s') #adds test name text to the point

                        if i > 1 and type(normalized_marks[i - 1]) in (int, float) and (previousx != 0 and previousy != 0): #draw a line only when both current and previous marks are numeric
                            x1 = (i - 1) * point_spacing
                            y1 = canvas_height - normalized_marks[i - 1] #adjusted y coordinates for the line to make sure it actually passes through the point
                            self.canvas2.create_line(previousx, previousy, x, y, fill='dark green') #previous x and y are the values of the dot before (0 ohterwise)

                        previousx = x
                        previousy = y
                        
                    i += 1
            else:
                print(f"No matching student found for '{selected_student}'")
          
    def get_student_marks(self):
        "Gets the students marks for the specificed student by joing the database tables accordingly"
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor() #the gets the marks and tests data in one line, so it goes through tests and gets the name, then to marks and gets the mark, joins then for the result (links)
                                #and its all based on the student_id
        cursor.execute(''' 
            SELECT Tests.test_name, Marks.mark
            FROM Marks
            JOIN Tests ON Marks.test_id = Tests.id
            WHERE Marks.student_id = ?
        ''', (self.student_id,))

        result = cursor.fetchall() 
        conn.commit()
        conn.close()

        return result #returns the tuple of data to the function

