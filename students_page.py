from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import os
import sys
import sqlite3
from adding_tables import MarkbookProcessor


class StudentPage():
    def __init__(self, db_file, frame):
        "Initalized the variables used throghout the code"
        try:
            self.db_file = db_file
            self.frame = frame
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def on_marks_entry_focus_in(self, event):
        "Function for when the marks entry is clicked"
        try:
            if self.marks_entry.get("1.0", "end-1c") == self.marks_placeholder:
                self.marks_entry.delete("1.0", END) #updates the entry box to have the proper attributes
                self.marks_entry.config(fg="black")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def on_marks_entry_focus_out(self, event):
        "Function for when marks entry is not clicked"
        try:
            if not self.marks_entry.get("1.0", "end-1c").strip(): #adds back the placeholder text
                self.marks_entry.insert("1.0", self.marks_placeholder)
                self.marks_entry.config(fg="grey")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def create_treeview(self):
        "Created the treeview to display all the student information"
        try:
            mycolumns = ["Student Number", "Student Name", "Phone Number"] #columnds for the treeview
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Tests")
            tests_data = cursor.fetchall()

            for test in tests_data:
                test_name = test[1]
                mycolumns.append(test_name)

            mycolumns = tuple(mycolumns)
            
            style = ttk.Style() 
            style.theme_use("clam") #creates the styling for the treeview to make it more appealing and cohesive
            style.configure("Treeview", background="#b1caa4", 
                    fieldbackground="#b1caa4", foreground="black", font=("Courier",10))
            style.configure('Treeview.Heading', background="#7ca666", font=("Courier",10))

            self.tree = ttk.Treeview(self.frame, columns=mycolumns, show="headings", selectmode="browse")

            for column in mycolumns:
                self.tree.column(column, anchor=CENTER, width=120)
                self.tree.heading(column, text=column, anchor=CENTER)

            cursor.execute("SELECT * FROM Students")
            students_data = cursor.fetchall()

            students = {}
            for student in students_data:
                student_number, name, phone_number = student[1], student[2], student[3]
                students[student_number] = {
                    "Name": name,
                    "Phone Number": phone_number
                }

            cursor.execute("SELECT student_id, test_id, mark FROM Marks")
            marks_data = cursor.fetchall()

            for mark in marks_data:
                student_id, test_id, mark_value = mark
                student_number = [student[1] for student in students_data if student[0] == student_id][0] #splits up the data accordingly
                test_name = [test[1] for test in tests_data if test[0] == test_id][0]
                students[student_number][test_name] = mark_value


            for student_number, info in students.items():
                values = [info["Name"], info["Phone Number"]] + [info.get(column, "") for column in self.tree["columns"][3:]]
                self.tree.insert("", "end", values=[student_number] + values, tags=('item',)) #assigns data to the treeview

            conn.close()

            self.tree.column("#0", width=0, stretch=NO)

            vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
            vsb.place(in_=self.frame, x=887, y=0, relheight=0.4)

            self.tree.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
            hsb.place(in_=self.frame, x=0, y=240, relwidth=1) #adding all my scroll bars

            self.tree.configure(xscrollcommand=hsb.set)

            self.tree.place(in_=self.frame, x=0, y=0, width=886, height=240)
            
            self.place_elements()
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def place_elements(self):
        "Create and placee all the elements and widgets"
        try:
            self.instruction_lbl = Label(self.frame, text="*Click on a Student to Begin!*", font=("Courier", 14), fg="red", bg="#d3d3b1")
            self.instruction_lbl.place(x=20,y=260)
            
            self.studentnum_lbl = Label(self.frame, text="Student Number", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.studentnum_lbl.place(x=20,y=310)

            self.studentnum_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.studentnum_entry.place(x=190,y=312)

            self.name_lbl = Label(self.frame, text="Student Name", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.name_lbl.place(x=20,y=360)

            self.name_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.name_entry.place(x=190,y=362)

            self.phonenum_lbl = Label(self.frame, text="Phone Number", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.phonenum_lbl.place(x=20,y=410)

            self.phonenum_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.phonenum_entry.place(x=190,y=412)

            self.marks_lbl = Label(self.frame, text="Marks", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.marks_lbl.place(x=480,y=260)

            self.tree.bind("<ButtonRelease-1>", self.on_student_select) #binding to function

            self.listbox = Listbox(self.frame, font=("Courier", 11), fg="black", bg="#b1caa4", width=22, height=8)
            self.listbox.place(x=410, y=285)
            self.listbox.bind("<<ListboxSelect>>", self.on_test_item_select) #bidning to function

            self.marks_entry = Text(self.frame, font=("Courier", 11), fg="black", bg="#b1caa4", width=20, height=9, wrap="word")
            self.marks_entry.place(x=680, y=285)
            self.text = Label(self.frame, font=("Courier",9), fg="black", bg="#b1caa4", text="INSTRUCTIONS:" + "\n" + "ADD STUDENT -> Fill in entries and press 'Add'   DELETE STUDENT -> Select student and press 'Delete'" + "\n" + "ADD TEST TO STUDENT -> Select student, enter test in above entry with format, and press 'Update'" + " \n" + "DELETE TEST FROM STUDENT-> Select from listbox and press 'Delete'" + "\n" + "UPDATE TEST -> Select from listbox, edit in entry box above, and press 'Update' (ensure test still selected)")
            self.text.place(x=100, y=555, anchor = "w")
            self.entry_text = Label(self.frame, font=("Courier",9), fg="black",bg="#d3d3b1", text="Test Format: testname - mark")
            self.entry_text.place(x=680,y=450)
            self.marks_placeholder = "Enter test(s) in this format: (NO NEW LINE, JUST COMMAS)" + "\n"*2 + "testname - mark, testname - mark," + "\n" + "..."
            self.marks_entry.insert("1.0", self.marks_placeholder)
            self.marks_entry.config(fg="grey")
            self.marks_entry.bind("<FocusIn>", self.on_marks_entry_focus_in) #bidning to function
            self.marks_entry.bind("<FocusOut>", self.on_marks_entry_focus_out) #binding to function


            scrollbar = Scrollbar(self.frame, command=self.marks_entry.yview)
            scrollbar.place(x=865, y=285, height=160)  
            self.marks_entry.config(yscrollcommand=scrollbar.set)

            self.add_button = Button(self.frame, text="Add", command=self.add_student, font=("Courier", 14), bg="#d1fdd1", fg="black", width=8)
            self.update_button = Button(self.frame, text="Update", command = self.update_student, font=("Courier", 14), bg="#ffffbf", fg="black", width=8)
            self.delete_button = Button(self.frame, text="Delete", command=self.delete_student, font=("Courier", 14), bg="#DD635D", fg="black", width=8)

            self.clear_button = Button(self.frame, text="Clear", command=self.clear_fields, font=("Courier", 14), bg="#C3B1E1", fg="black", width=8)

            self.clear_button.place(x=220, y=460)
            self.add_button.place(x=330, y=460)
            self.update_button.place(x=440, y=460)
            self.delete_button.place(x=550, y=460)
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def update_entry_widgets(self):
        "Updates and places all the widgets when this function is called with new infomation"
        try:
            if self.selected_student:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Students WHERE student_number=?", (self.selected_student,))
                student_data = cursor.fetchone()

                if student_data:
                    studentid, student_number, name, phone_number = student_data
                    self.studentnum_entry.delete(0,END)
                    self.studentnum_entry.insert(0,student_number)
                    self.name_entry.delete(0, END)
                    self.name_entry.insert(0, name)
                    self.phonenum_entry.delete(0, END)
                    if phone_number == None:
                        self.phonenum_entry.insert(0, "None")
                    else:
                        self.phonenum_entry.insert(0, phone_number)

                    cursor.execute('''
                                    SELECT Tests.test_name, Marks.mark
                                    FROM Marks
                                    JOIN Tests ON Marks.test_id = Tests.id
                                    WHERE Marks.student_id = ?
                                ''', (studentid,)) #joining the tables to retrive the information in one line

                    marks_data = cursor.fetchall()

                    self.listbox.delete(0, END)
                    for test_name, mark in marks_data:
                        self.listbox.insert(END, f"{test_name} - {mark}")
                conn.close()
                
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def on_test_item_select(self, event):
        "Function for when a test item is selected from the listbox"
        try:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_test_item = self.listbox.get(selected_index)
                test_name, mark = selected_test_item.split(" - ")

                self.marks_entry.delete(0, END)
                self.marks_entry.insert(0, mark)
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def on_student_select(self, event):
        "Function for when a student is selected from the treeview"
        try:
            selected_item = self.tree.selection()
            if selected_item:
                self.selected_student = self.tree.item(selected_item, "values")[0]
                self.update_entry_widgets()
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def on_test_item_select(self, event):
        "Function for when a student is selected from the lsitbox"
        try:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_test_item = self.listbox.get(selected_index)
                test_name, mark = selected_test_item.split(" - ")

                self.marks_entry.delete("1.0", END)
                self.marks_entry.insert("1.0", mark)
                self.marks_entry.config(fg="black")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def update_student(self):
        "Function to update the information about the student"
        try:
            if not self.selected_student:
                showerror("Error", "No student selected for update.")
                return

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM Students WHERE student_number=?", (self.selected_student,))
            student_id = cursor.fetchone()

            self.new_student_number = self.studentnum_entry.get()
            new_name = self.name_entry.get()
            self.new_phone_number = self.phonenum_entry.get() or None

            if student_id and self.is_valid_student_number() and self.is_valid_phone_number(): #validating the information provided
                student_id = student_id[0]

                cursor.execute("UPDATE Students SET student_number=?, name=?, phone_number=? WHERE id=?",
                               (self.new_student_number, new_name, self.new_phone_number, student_id))

                selected_index = self.listbox.curselection()
                if selected_index:
                    selected_test_item = self.listbox.get(selected_index)
                    test_name, _ = selected_test_item.split(" - ")
                    new_mark = self.marks_entry.get("1.0", "end-1c").strip()

                    cursor.execute("SELECT id FROM Tests WHERE test_name=?", (test_name,))
                    test_id = cursor.fetchone()

                    if test_id and new_mark:
                        test_id = test_id[0]

                        cursor.execute("UPDATE Marks SET mark=? WHERE student_id=? AND test_id=?",
                                       (new_mark, student_id, test_id))

                        self.listbox.delete(selected_index)
                        self.listbox.insert(selected_index, f"{test_name} - {new_mark}")
                else:
                    new_mark_entry = self.marks_entry.get("1.0", "end-1c").strip().split(",")
                    listplaceholder = ['Enter test(s) in this format: (NO NEW LINE', ' JUST COMMAS)\n\ntestname - mark', ' testname - mark', '\n...']
                    if new_mark_entry and new_mark_entry != listplaceholder:
                        try:
                            for i in new_mark_entry:
                                test_name, new_mark = i.split("-")
                                test_name = test_name.strip()
                                new_mark = new_mark.strip()

                                cursor.execute("SELECT id FROM Tests WHERE test_name=?", (test_name,))
                                test_id = cursor.fetchone()
                                
                                if test_id:
                                    test_id = test_id[0]

                                    cursor.execute("INSERT INTO Marks (student_id, test_id, mark) VALUES (?, ?, ?)",
                                                   (student_id, test_id, new_mark))

                                    self.listbox.insert(END, f"{test_name} - {new_mark}")
                                else:
                                    showerror("Error", f"Test with name '{test_name}' not found.")

                        except ValueError:
                            showerror("Error", "Invalid entry format. Use 'Test Name - Mark'.")
            else:
                showerror("Error", "An error has occured, check your entered info again")
                
            conn.commit()
            conn.close()

            self.clear_fields()
            self.update_treeview()
                
        except AttributeError:
            showerror("Error", "Please fill out all the required fields.")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))


    def add_student(self):
        "Function to add the information for the student when the user clicks add"
        try:
            self.new_student_number = self.studentnum_entry.get()
            name = self.name_entry.get()
            self.new_phone_number = self.phonenum_entry.get()
            if self.new_phone_number == "":
                self.new_phone_number = None

            if not self.new_student_number or not name:
                showerror("Error", "Please fill out all the required fields.")
                return

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM Students WHERE student_number=?", (self.new_student_number,))
            existing_student = cursor.fetchone()

            if existing_student and self.is_valid_student_number() and self.is_valid_phone_number():
                showwarning("Error", "Student already exists. Press 'Update' instead.")

            else:
                entry = self.marks_entry.get("1.0", "end-1c")
                self.clear_fields()
                if entry != "" and self.is_valid_student_number() and self.is_valid_phone_number():
                    lines = entry.split(",")
                    cursor.execute("INSERT INTO Students (student_number, name, phone_number) VALUES (?, ?, ?)",
                                    (self.new_student_number, name, self.new_phone_number))
                    cursor.execute("SELECT id FROM Students WHERE student_number=?", (self.new_student_number,))
                    student_id = cursor.fetchone()[0]
                    if entry != self.marks_placeholder and self.is_valid_student_number() and self.is_valid_phone_number():
                        for line in lines:
                            line = line.strip()
                            if line:
                                try:
                                    test_name, mark = line.split("-")
                                    test_name = test_name.strip()
                                    mark = mark.strip()
                                    cursor.execute("SELECT id FROM Tests WHERE test_name=?", (test_name,))
                                    test_id = cursor.fetchone()
                                    if test_id is not None:
                                        test_id = test_id[0]
                                        cursor.execute("INSERT INTO Marks (student_id, test_id, mark) VALUES (?, ?, ?)",
                                                        (student_id, test_id, mark))
                                    else:
                                        showerror("Error", f"Test '{test_name}' does not exist.")
                                except ValueError as error:
                                    showerror("Error", "Invalid entry format. Use 'Test Name - Mark'.")
                        self.clear_fields()
                else:
                    if self.is_valid_phone_number() != True:
                        showerror("Error", "An error has occured, phone number not in phone number format {XXX-XXX-XXXX) or left blank")
                    elif self.is_valid_student_number() != True:
                        showerror("Error", "An error has occured, student number not a number")
                        
                    
            conn.commit()
            conn.close()

            self.update_treeview()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def update_treeview(self):
        "Function to update the treeview when information is updated or changed"
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Students")
            students_data = cursor.fetchall()

            students = {}
            for student in students_data:
                student_number, name, phone_number = student[1], student[2], student[3]
                students[student_number] = {
                    "Name": name,
                    "Phone Number": phone_number
                }

            cursor.execute("SELECT * FROM Tests")
            tests_data = cursor.fetchall()

            cursor.execute("SELECT student_id, test_id, mark FROM Marks")
            marks_data = cursor.fetchall()

            for mark in marks_data:
                student_id, test_id, mark_value = mark
                student_number = [student[1] for student in students_data if student[0] == student_id][0]
                test_name = [test[1] for test in tests_data if test[0] == test_id][0]
                students[student_number][test_name] = mark_value

            for student_number, info in students.items():
                values = [info["Name"], info["Phone Number"]] + [info.get(column, "") for column in self.tree["columns"][3:]]
                self.tree.insert("", "end", values=[student_number] + values, tags=('item',))

            conn.close()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def on_marks_entry_focus_in(self, event):
        "Function for when the marks entry is clicked on"
        try:
            if self.marks_entry.get("1.0", "end-1c") == self.marks_placeholder:
                self.marks_entry.delete("1.0", END)
                self.marks_entry.config(fg="black")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def on_marks_entry_focus_out(self, event):
        "Function for when the marks entry is not clicked on"
        try:
            if not self.marks_entry.get("1.0", "end-1c").strip():
                self.marks_entry.insert("1.0", self.marks_placeholder)
                self.marks_entry.config(fg="grey")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def clear_fields(self):
        "Function for clearing the fields of the entries and lsitbox/treeview"
        try:
            self.studentnum_entry.delete(0, END)
            self.name_entry.delete(0, END)
            self.phonenum_entry.delete(0, END)
            self.listbox.delete(0, END)
            self.marks_entry.delete("1.0", END)
            self.marks_entry.insert("1.0", self.marks_placeholder)
            self.marks_entry.config(fg="grey")
            selected_item = self.tree.selection()
            self.tree.selection_remove(selected_item)
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def delete_student(self):
        "Function to delete a student when the user presses delete"
        try:
            if not self.selected_student:
                showerror("Error", "No student selected for deletion.")
                return
            listbox_has_items = self.listbox.size() > 0
            
            # Check if an item is selected in the listbox
            selected_indices = self.listbox.curselection()
            delete_only_marks = not not selected_indices  # Converts an empty tuple to False, and non-empty to True


            # Determine whether to delete only marks based on listbox selection

            confirmation_msg = ""
            if delete_only_marks == False and listbox_has_items == True:
                confirmation_msg += "Are you sure you want to delete the selected student AND their marks?"
            else:
                confirmation_msg += "Are you sure you want to delete the selected mark?"
                
            confirmation = askyesno("Confirmation", confirmation_msg)
            if not confirmation:
                return

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            
            cursor.execute("SELECT id FROM Students WHERE student_number=?", (self.selected_student,))
            student_id = cursor.fetchone()


            if student_id:  
                student_id = student_id[0]
                if delete_only_marks and listbox_has_items == True:
                    title = self.listbox.get(selected_indices).split("-")
                    test_title = (title[0]).strip()
                    cursor.execute("SELECT id FROM Tests WHERE test_name=?", (test_title,))
                    test_id = cursor.fetchone()
                    test_id = test_id[0]
                    # Delete only from the Marks table
                    cursor.execute("DELETE FROM Marks WHERE test_id=? AND student_id = ?", (test_id,student_id))
                else:
                    # Delete from both Marks and Students tables
                    cursor.execute("DELETE FROM Marks WHERE student_id = ?", (student_id,))
                    cursor.execute("DELETE FROM Students WHERE id=?", (student_id,))

                conn.commit()
                conn.close()

                self.update_treeview()
                self.clear_fields()
            else:
                showerror("Error", "Selected student not found in the database.")
        except AttributeError:
            showerror("Error", "Please fill out all the required fields.")
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def is_valid_student_number(self):
        "Function to validate the student number provided by the user"
        return str(self.new_student_number).isdigit()

    def is_valid_phone_number(self):
        "Function to validate the phone number provided by the user"
        if self.new_phone_number == "None" or self.new_phone_number == None:
            return True
        else:
            return len(str(self.new_phone_number)) == 12 and str(self.new_phone_number).replace('-', '').isdigit()
