from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import os
import sys
import sqlite3
from adding_tables import MarkbookProcessor

class TestsPage():
    def __init__(self, db_file, frame):
        "Initialzies the variables that will be used throughout the program (file, frame)"
        try:
            self.db_file = db_file
            self.frame = frame #created variables for information to be used throughout program
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def create_treeview(self):
        "Creates the treeview that will display all the test information"
        try:
            mycolumns = ["Test Name", "Category", "Weight", "Out of"] #default column anmes
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Tests") #gets all the test informaiton
            tests_data = cursor.fetchall()

            mycolumns = tuple(mycolumns)

            style = ttk.Style()  #sets the style and theme of the treeview to make it more appealing
            style.theme_use("clam")
            style.configure("Treeview", background="#b1caa4", 
                    fieldbackground="#b1caa4", foreground="black", font=("Courier",10))
            style.configure('Treeview.Heading', background="#7ca666", font=("Courier",10))


            self.tree = ttk.Treeview(self.frame, columns=mycolumns, show="headings", selectmode="browse") #creates the treeview

            for column in mycolumns:
                self.tree.column(column, anchor=CENTER, width=120) #adds the columns and formats them accordingly
                self.tree.heading(column, text=column, anchor=CENTER)

            for test_info in tests_data:
                test_name, category, weight, out_of = test_info[1], test_info[2], test_info[3], test_info[4]
                self.tree.insert("", "end", values=[test_name, category, weight, out_of], tags=('item',)) #adds all the info to the according column

            conn.close()

            self.tree.column("#0", width=0, stretch=NO)

            vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
            vsb.place(in_=self.frame, x=887, y=0, relheight=0.4) #created vertical scrollbar for treeview

            self.tree.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
            hsb.place(in_=self.frame, x=0, y=240, relwidth=1) #created horizonal scrollbar for treeview

            self.tree.configure(xscrollcommand=hsb.set)

            self.tree.place(in_=self.frame, x=0, y=0, width=886, height=240)
            self.place_elements() #function to place all the remaining elements
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def place_elements(self):
        "Creates and places all the elements on the main screen including texts, labels, etc."
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            #places all the labels and extries and buttons required
            self.instruction_lbl = Label(self.frame, text="*Click on a Test to Begin!*", font=("Courier", 14), fg="red", bg="#d3d3b1")
            self.instruction_lbl.place(x=20,y=260)
            
            self.testname_lbl = Label(self.frame, text="Test Name", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.testname_lbl.place(x=20,y=315)

            self.testname_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.testname_entry.place(x=150,y=315)

            self.testname_entry.bind("<KeyRelease>", self.check_entries) #bind the test name when a key is realesed from user (when they are typing)

            self.category_lbl = Label(self.frame, text="Category", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.category_lbl.place(x=20,y=375)
            name1 = "Category 1 Name"
            name2 = "Category 2 Name"
            

            cursor.execute("SELECT value FROM setup where key=?", (name1,)) #get categroy 1 name
            category1 = cursor.fetchone()
            cursor.execute("SELECT value FROM setup where key=?", (name2,)) #get categiry 2 name
            category2 = cursor.fetchone()

            values = []
            values += category1[0], category2[0] #add category names to values to be values for combobox drop downs

            self.categorycombo = ttk.Combobox(state="readonly",values=values, font=("Courier", 14), width=14)
            self.categorycombo.place(x=150, y=375)

            self.categorycombo.bind("<Button-1>", self.check_entries) #bind click on combobox item to function
            self.categorycombo.bind("<<ComboboxSelected>>", self.check_entries) #bind click on combobox to function

            self.outof_lbl = Label(self.frame, text="Out Of", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.outof_lbl.place(x=360, y=375)

            self.outof_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.outof_entry.place(x=460, y=377)

            self.outof_entry.bind("<KeyRelease>", self.check_entries) #bind entry key realse to function (when use typing)

            self.weight_lbl = Label(self.frame, text="Weight", font=("Courier", 14), fg="dark green", bg="#d3d3b1")
            self.weight_lbl.place(x=360, y=315)

            self.weight_entry = Entry(self.frame, font=("Courier", 14), fg="black", bg="#b1caa4", width=15)
            self.weight_entry.place(x=460, y=312)
            
            self.weight_entry.bind("<KeyRelease>", self.check_entries) #bind entry key realse to function (when use typing)

            self.placeholdertext = "When adding new test, students will show up here to allow addition of marks aswell..."
            self.marks_entry = Text(self.frame, font=("Courier", 11), fg="grey", bg="#b1caa4", width=20, height=9, wrap="word")
            self.marks_entry.insert("1.0", self.placeholdertext)
            self.marks_entry.place(x=680, y=285)

            scrollbar = Scrollbar(self.frame, command=self.marks_entry.yview)
            scrollbar.place(x=865, y=285, height=160)  #create scrollbar for marks entry
            self.marks_entry.config(yscrollcommand=scrollbar.set)

            self.marks_entry.bind("<Key>", self.prevent_text_deletion)  #bind entry key to function

            self.tree.bind("<ButtonRelease-1>", self.on_test_select)  #bind buttin realse to function

            self.add_button = Button(self.frame, text="Add", command=self.add_test, font=("Courier", 14), bg="#d1fdd1", fg="black", width=8)
            self.update_button = Button(self.frame, text="Update", command=self.update_test, font=("Courier", 14), bg="#ffffbf", fg="black", width=8)
            self.delete_button = Button(self.frame, text="Delete", command=self.delete_test, font=("Courier", 14), bg="#DD635D", fg="black", width=8)

            self.clear_button = Button(self.frame, text="Clear", command = self.clear_fields, font=("Courier", 14), bg="#C3B1E1", fg="black", width=8)

            self.clear_button.place(x=220, y=460) #created and placed buttons 
            self.add_button.place(x=330, y=460)
            self.update_button.place(x=440, y=460)
            self.delete_button.place(x=550, y=460)
            self.text = Label(self.frame, font=("Courier",9), fg="black", bg="#b1caa4", text="INSTRUCTIONS:" + "\n" +"ADD TEST -> Fill in the blank entries, add marks for students in the textbox, and press 'Add'" + "\n" + "UPDATE TEST -> Select test, edit information and press 'Update'" + "\n" + "DELETE TEST -> Select test and press 'Delete'")
            self.text.place(x=100, y=555, anchor = "w")
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
                
    def on_test_select(self, event):
        "Function for when a test is selected from the treeview"
        try:
            selected_item = self.tree.selection() #get selected item
            if selected_item:
                self.selected_test = self.tree.item(selected_item, "values")[0] #get the test name of selected item
                self.update_entry_widgets() #update the entry
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def check_entries(self, event):
        "Checks to see if all the entries are full, and if they are and nothing in the treeview is selected, it adds text to the marks entry"
        selected_item = self.tree.selection()
        if self.testname_entry.get() and self.categorycombo.get() and self.outof_entry.get() and self.weight_entry.get() and not selected_item: #checks all entries
            self.marks_entry.delete("1.0", END) #when all full + no text selected, change the properties of the entry
            self.marks_entry.config(fg="black")
            self.marks_entry.insert("1.0", "Enter Marks for the New Test for Each Student Here!" + "\n"*2)
            self.fetch_student_names() #get the student names
        else:
            self.marks_entry.delete("1.0", END) #if not, change entry back to placeholder
            self.marks_entry.config(fg="grey")
            self.marks_entry.insert("1.0", self.placeholdertext)
            
    def fetch_student_names(self):
        "Gets all the student names in the students file and formats them correctly"
        conn = sqlite3.connect("markbook.db") 
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM Students") #get the students names 
        student_names = [row[0] for row in cursor.fetchall()] #extracts the student names

        for name in student_names:
            self.marks_entry.insert(END, f"{name} - " + "\n") #formats the names corrected and adds to the entry box

        conn.close()
        
    def prevent_text_deletion(self, event):
        "Makes sure that the user cannot delete existing text (student names and instructions) in the entry box"
        cursor_position = self.marks_entry.index(CURRENT)

        if self.marks_entry.compare(cursor_position, ">", "1.0"): #checks to see where the cursor is in the entry box (above first character)
            character = str(cursor_position).split(".") #gets the cursor row and exact character
            prev_character = character[0] + "." + str(int(character[1]) - 1) #subtarcts one from charater to see the previous character
            prev_char = self.marks_entry.get(prev_character) #gets what that previous character is

            if not prev_char.isdigit() and event.keysym == 'BackSpace': #if that character is not a digit and the user hit backspace, DONOT let them delete it
                return 'break' #break
            
    def update_entry_widgets(self):
        "Update the entry widgets when the function is called by inserting the information for the test in"
        try:
            if self.selected_test:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()

                cursor.execute('''
                                SELECT test_name, category, weight, out_of
                                FROM Tests
                                WHERE test_name = ?
                            ''', (self.selected_test,)) #gets all the test informaiton

                test_data = cursor.fetchall()

                for test_name, category, weight, out_of in test_data: #clears and adds in all the text information into according entries

                    self.testname_entry.delete(0, END)
                    self.testname_entry.insert(0, test_name)

                    self.weight_entry.delete(0, END)
                    self.weight_entry.insert(0, weight)

                    self.outof_entry.delete(0, END)
                    self.outof_entry.insert(0, out_of)

                    self.categorycombo.set(category)
                    
                conn.commit()
                conn.close()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))
            
    def add_test(self):
        "Function from when the user is adding a new test and the add button is clicked"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            test_name = self.testname_entry.get()
            category = self.categorycombo.get()
            weight = self.weight_entry.get()
            out_of = self.outof_entry.get()

            if not test_name or not category or not weight or not out_of:
                showerror("Error", "All fields must be filled") #make sure all entries are full
                return

            try:
                weight = int(weight) #make sure weight and outof are integers
                out_of = int(out_of)
            except ValueError:
                showerror("Error", "Weight and Out Of must be integers")
                return

            cursor.execute('''
                            INSERT INTO Tests (test_name, category, weight, out_of)
                            VALUES (?, ?, ?, ?)
                        ''', (test_name, category, weight, out_of)) #add the information into the tests table

            self.tree.insert("", "end", values=[test_name, category, weight, out_of], tags=('item',)) #add the info into the treeview
            
            conn.commit()
            
            text = (self.marks_entry.get("1.0", END)).split("\n") #check the marks entry and split at each student
            mark = 0
            for line in text:
                row = line.split("-")
                try:
                    mark = int(row[1]) #get the mark, it is a integer, it will continue, if not, it will stop for that line and move to next
                    student_name = (row[0]).strip()
                    cursor.execute("SELECT id FROM Students WHERE name=?", (student_name,)) #get the student id
                    student_id = cursor.fetchone()
                    student_id = student_id[0]

                    cursor.execute("SELECT id FROM Tests WHERE test_name=?", (test_name,)) #get the test id for the test that got added
                    test_id = cursor.fetchone()
                    test_id = test_id[0]
                    
                    cursor.execute("INSERT INTO Marks (student_id, test_id, mark) VALUES (?, ?, ?)", (student_id, test_id, mark,)) #add the mark using the test id and studnet id
                    
                    conn.commit()
                    
                except (IndexError, ValueError): #errors for when mark not integer (/not added)
                    pass

            conn.close()
            self.clear_fields()
            
        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def update_test(self):
        "Function for when the user updates a test information and presses the update button"
        try:
            if not self.selected_test: #when no student is selected to update
                showerror("Error", "No student selected for update.")
                return

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            test_name = self.testname_entry.get() #get the information of all the entries
            category = self.categorycombo.get()
            weight = self.weight_entry.get()
            out_of = self.outof_entry.get()

            if not test_name or not category or not weight or not out_of: #if an entry is not filled out
                showerror("Error", "All fields must be filled")
                return

            try:
                weight = int(weight) #check to makre sure weight and out of are integers
                out_of = int(out_of)
            except ValueError:
                showerror("Error", "Weight and Out Of must be integers")
                return

            cursor.execute("SELECT id FROM Tests WHERE test_name=?", (self.selected_test,)) #get the test id for the test name
            test_id = cursor.fetchone()

            if test_id:
                test_id = test_id[0]

                cursor.execute('''UPDATE Tests 
                                  SET test_name=?, category=?, weight=?, out_of=?
                                      WHERE id=?
                               ''', (test_name, category, weight, out_of, test_id)) #update the information for that specific test id

                conn.commit()
                conn.close()

                selected_item = self.tree.selection()
                if selected_item:
                    self.tree.item(selected_item, values=[test_name, category, weight, out_of]) #update the treeview item
            self.clear_fields()
        
        except Exception as error:
            showerror("Error", f"An error occurred: {error}")

    def delete_test(self):
        "Function for when a test is deleted by the user and the delete button is clicked"
        try:
            if not self.selected_test: #check to make sure a student is selected
                showerror("Error", "No student selected for update.")
                return

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            confirm = askyesno("Confirmation", f"Are you sure you want to delete the test: {self.selected_test}?") #confirm they wanna delete the test
            if not confirm:
                return

            cursor.execute("SELECT id FROM Tests WHERE test_name=?", (self.selected_test,)) #get the test id using the test name
            test_id = cursor.fetchone()
            test_id = test_id[0]

            cursor.execute('''
                            DELETE FROM Tests
                            WHERE test_name=?
                        ''', (self.selected_test,)) #delete the test based on the test name
            conn.commit()
            cursor.execute('''
                            DELETE FROM Marks
                            WHERE test_id=?
                        ''', (test_id,)) #delete the test information where the marks table has the test id
            conn.commit()
            conn.close

            selected_item = self.tree.selection()
            if selected_item:
                self.tree.delete(selected_item) #delete the test in the treeview
            self.clear_fields()
            self.clear_fields()

        except Exception as error:
            print("Error:", error, "Line: {}".format(sys.exc_info()[-1].tb_lineno))

    def clear_fields(self):
        "Function for clearing all the widget fields when called or the clear button is pressed"
        self.testname_entry.delete(0, END) #clear all the entries
        self.categorycombo.set('') #clear comobobox selection
        self.weight_entry.delete(0, END)
        self.outof_entry.delete(0, END)
        selected_item = self.tree.selection()
        self.tree.selection_remove(selected_item) #clear treeview selection
        self.marks_entry.delete("1.0", END)
        self.marks_entry.config(fg="grey") #set text back to placeholder text
        self.marks_entry.insert("1.0", self.placeholdertext)
