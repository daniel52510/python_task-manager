import tkinter as tk
import csv
import os
import re
import datetime
from email.message import EmailMessage
import smtplib
email_sender = 'taskmanagerforyou@gmail.com'
email_password = 'nvcpwrpjcjhqzwkc'
email_receiver = 'danielblazquez640@gmail.com'
import ssl
from tkinter import messagebox
filepath = 'task_list.csv'
class AppWindow:
    def __init__(self, root):
        root.geometry('800x700')
        root.title('Task Manager for Everyday Life')
        root.wm_resizable(width=False, height=False)
        menu = tk.Menu(root)
        item = tk.Menu(menu)
        item.add_command(label='Create New Task',command=self.create_task_popup)
        item.add_command(label='Delete A Task',command=self.delete_task_popup)
        item.add_command(label='Settings', command=self.settings_popups)
        menu.add_cascade(label="File", menu=item)
        root.config(menu=menu)

        self.task_title = tk.Label(root,text='Welcome!',font=('Arial', 16))
        self.task_title.grid(row=0,column=0,columnspan=2,sticky=tk.NSEW)
        self.task_title.grid_rowconfigure(0, weight=1)

        self.task_notes_area = tk.Text(root, font=('Arial', 16))
        self.task_notes_area.grid(row=1,column=1,sticky=tk.NSEW)

        self.task_list_GUI = tk.Listbox(root, font=('Arial', 20))
        self.task_list_GUI.grid(row=1,column=0,sticky=tk.NSEW)

        self.open_task = tk.Button(root, text="Open Selected Task",command=lambda: Task.select_task(self.task_list_GUI,self.task_notes_area,self.task_title))
        self.open_task.grid(row=3,column=0,padx=10,pady=10,sticky=tk.SW)

        self.save_task = tk.Button(root,text="Save Notes",command=lambda: Task.save_notes(self.task_notes_area,self.task_title.cget('text'),self.task_title))
        self.save_task.grid(row=3,column=1,padx=10,pady=10,sticky=tk.SE)

        root.grid_rowconfigure(1,weight=1)
        root.grid_columnconfigure(1,weight=1)
        Task.create_file()
        taskTab.load_task(self.task_list_GUI)
        found_task = self.check_task_dates()
        self.email_message(email_sender, email_password, email_receiver, found_task)

    #def get_email(self):
    def set_email(self, email,email_in):
        text = email_in.get()
        print(f"Here is your email: {text}")
        email = text
        found_task = self.check_task_dates()
        self.email_message(email_sender, email_password, email_receiver, found_task)
    def settings_popups(self):
        top = tk.Toplevel()
        top.wm_resizable(width=False, height=False)
        top.geometry('700x150')
        top.title("Settings")
        # Label for Prompt
        lbl = tk.Label(top, text='Provide your Email:', font=('Arial', 18))
        lbl.grid(column=0, row=0, padx=10, pady=10)
        email_in = tk.Entry(top)
        email_in.grid(column=1, row=0)
        email_submit = tk.Button(top,text="Submit",command=lambda: self.set_email(email_receiver,email_in))
        email_submit.grid(column=1,row=0)
    def check_task_dates(self):
        print(f"Today's Date- {datetime.datetime.now()}")
        task_due_arr = []
        with open('task_list.csv','r') as file:
           reader = csv.reader(file)
           next(reader)
           for line in reader:
                print(f'Dates Found: {line[2]}')
                task_date = line[2]
                x = task_date.replace('/','')
                month = x[:2]
                day = x[2:4]
                year = x[4:]
                month = int(month)
                day = int(day)
                print(f'day: {day}')
                year = int(year)
                date_obj = datetime.datetime(year, month, day)
                today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                difference = date_obj - today_date
                print(f'Difference: {difference}')
                if difference.days == 1:
                    print(f'{line[0]} is due tomorrow!')
                    task_due_arr.append(line[0])
                else:
                    print(f'{line[0]} is due in the future!')
        return task_due_arr
    def email_message(self, sender, passwd, receiver,task_arr):
        for i in task_arr:

            subject = "Attention: A Task is Due!"
            body = f"""
            Hello! I am here to bring to your attention that your {i} task is due!
            Please complete it at your earliest convenience!
            Sincerely,
            Your Task Manager
            """
            em = EmailMessage()
            em['From'] = sender
            em['To'] = receiver
            em['Subject'] = subject
            em.set_content(body)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender, passwd)
                smtp.sendmail(sender, receiver, em.as_string())

    def create_task_popup(self):
        top = tk.Toplevel()
        top.wm_resizable(width=False, height=False)
        top.geometry('700x150')
        top.title("Create Your Task")
        # Label for Prompt
        lbl = tk.Label(top, text='Name your new task:', font=('Arial', 18))
        lbl.grid(column=0, row=0, padx=10, pady=10)
        lbl = tk.Label(top, text='Describe your new task:', font=('Arial', 17))
        lbl.grid(column=0, row=1, padx=10, pady=10)
        lbl = tk.Label(top, text='What Day and Time?: (Enter MM/DD/YYYY)', font=('Arial', 17))
        lbl.grid(column=0, row=2, padx=10, pady=10)
        create_entry = tk.Entry(top)
        create_entry.grid(column=1, row=0)
        description = tk.Entry(top)
        description.grid(column=1, row=1)
        date = tk.Entry(top)
        date.grid(column=1, row=2)
        create_button = tk.Button(top, text='Create Task', command=lambda: self.re_task(create_entry, description, date, top))
        create_button.grid(column=2, row=1)
    def re_task(self, create_entry, description, date, window):
        name = create_entry.get()
        describe = description.get()
        date_task = date.get()
        errors = []
        MAX_TASK_NAME_LENGTH = 50
        MAX_DESCRIPTION_LENGTH = 100

        if len(name) > MAX_TASK_NAME_LENGTH:
            errors.append("Task name exceeds the character limit.")
        if len(describe) > MAX_DESCRIPTION_LENGTH:
            errors.append("Description exceeds the character limit.")
        if not re.match(r'\d{2}/\d{2}/\d{4}', date_task):
            errors.append("Invalid date format. Please use MM/DD/YYYY.")
        else:
            # Validate date is in the future
            current_date = datetime.datetime.now().date()
            entered_date = datetime.datetime.strptime(date_task, "%m/%d/%Y").date()
            if entered_date <= current_date:
                errors.append("Date must be a future date.")

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        new_task = Task(taskName=name, taskDescription=describe, taskDue=date_task, taskNotes=" ")
        Task.add_task(new_task)
        taskTab.load_task(self.task_list_GUI)
        window.destroy()

    # Create Task csv row
    def show_error(self,message):
        messagebox.showerror("Error", message)
    def delete_task_popup(self):
        top = tk.Toplevel()
        top.wm_resizable(width=False, height=False)
        top.geometry('400x300')
        top.title("Which Task to Delete?")
        delete_list = tk.Listbox(top, font=('Arial', 12))
        delete_list.pack()
        taskTab.load_task(delete_list)
        delete_button = tk.Button(top,text="Delete",command=lambda: self.warning_popup(delete_list))
        delete_button.pack()
    def warning_popup(self, list):
        top_final = tk.Toplevel()
        top_final.wm_resizable(width=False, height=False)
        top_final.geometry('400x200')
        top_final.title("Warning")
        lbl = tk.Label(top_final, text="Are You Sure You Want to Delete This Task?",font="bold",fg='red')
        yes_button = tk.Button(top_final, text="Yes",command=lambda: Task.delete_task(list, top_final, self.task_list_GUI,self.task_title))
        yes_button.pack()
        no_button = tk.Button(top_final, text="No",command=lambda: top_final.destroy())
        no_button.pack()
        self.task_notes_area.delete('1.0',tk.END)
        lbl.pack(pady=20)
class Task:
    def __init__(self, taskName, taskDescription, taskDue,taskNotes):
        self.name = taskName
        self.description = taskDescription
        self.due_date = taskDue
        self.notes = taskNotes
    def __str__(self):
        return f"Task Name: {self.name}\nDescription: {self.description}\nDue Date: {self.due_date}"
    def create_file():
        # Need to add a check function that ensures the name is unique.
        if os.path.exists(filepath):
            print("File Exist! Skipping Creation!")
        else:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["name","description","due_date","notes"])
    def add_task(task):
        # adding to csv
        with open('task_list.csv','a') as file:
            writer = csv.writer(file)
            writer.writerow([task.name,task.description,task.due_date,task.notes])
    def delete_task(listbox, window, GUI, task_title):
        indices = listbox.curselection()
        taskDelete = ''
        revise_list = []
        if indices:
            index = indices[0]
            selected_item = listbox.get(index)
            taskDelete = selected_item
            print(f"Selected Item: {selected_item}")
        else:
            print("There are no task!")

        with open('task_list.csv','r') as file:
            reader = csv.reader(file)
            for line in reader:
                if line[0] == taskDelete:
                    print(line[0], " is equal to ", taskDelete)
                    line.pop()
                else:
                    revise_list.append(line)
        with open('task_list.csv', 'w') as file:
            writer = csv.writer(file)
            for i in revise_list:
                writer.writerow(i)

        taskTab.load_task(listbox)
        taskTab.load_task(GUI)
        task_title.config(text="Welcome!")
        window.destroy()
    def select_task(task_list,text_box,task_title):
        indices = task_list.curselection()
        if indices:
            index = indices[0]
            selected_item = task_list.get(index)
            print(f'listbox item: {selected_item}')
            task_title.config(text=selected_item)
            Task.load_notes(text_box,selected_item)
        else:
            task_title.config(text="Welcome!")
            print("Cannot find task!")
    def load_notes(text_box,task_name):
        with open('task_list.csv','r') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                if line[0] == task_name:
                    task_notes = line[3]
                    print(f'task-notes: {task_notes}')
                    text_box.delete('1.0',tk.END)
                    text_box.insert(tk.END,task_notes)
    def save_notes(text_box,task_name,task):
        task_notes = text_box.get('1.0', tk.END)

        # Read the entire CSV file into a list
        with open(filepath, 'r') as file:
            rows = list(csv.reader(file))

        # Update the notes in the list
        for row in rows[1:]:
            if row[0] == task_name:
                row[3] = task_notes.strip()

        # Write the updated list back to the CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        messagebox.showinfo("Notes Saved", "Notes have been saved!")
        text_box.delete('1.0', tk.END)
        task.config(text='Welcome!')
class taskTab:
    def __init__(self, name, due_date):
        self.name = name
        self.due_date = due_date
    def load_task(listbox):
        listbox.delete(0,tk.END)
        #loading t_list to GUI
        with open('task_list.csv','r') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                taskName = line[0]
                #could be because of index below
                listbox.insert(tk.END,taskName)



