# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.



#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====== FUNCTION DEFINITIONS ======
# 4 functions for the menu are defined here:    
    

# FUNCTION 1 - REGISTER A NEW USER
def reg_user():
    new_username = input("New Username: ").strip()  #  .strip() to avoid whitespace
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # ensure passwords match
    if new_password != confirm_password:
        print("Passwords do not match")
        return 
    
   # Check for duplicate usernames in the user.txt file
    with open("user.txt", "r") as file:
        existing_usernames = [line.split(';')[0] for line in file]
        if new_username in existing_usernames:
            print("Sorry - username already taken - please try again")
            return
        
    # Write the new user data to the dictionary
    username_password[new_username] = new_password
    
     # Write the new user data to the user.txt file
    with open("user.txt", "a") as out_file:
        out_file.write(f"\n{new_username};{new_password}")

    print("New user added")
    
                
# FUNCTION 2 - ADD A TASK
    
# Allow a user to add a new task to task.txt file
# Prompt a user for the following: 
#  - A username of the person whom the task is assigned to,
#  - A title of a task,
#  - A description of the task and 
#  - the due date of the task.'''

def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return      #   changed 'continue' to return to avoid syntax error (continue not in loop)
    
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    # Add the data to the file task.txt and Include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# FUNCTION 3 - VIEW ALL TASKS
# Reads the task from task.txt file and prints to the console in the format of Output 2 
def view_all():
        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

# FUNCTION 4 - VIEW MINE
# Similar to function 3, but this is specific to the user's tasks         


def view_mine():
    task_number = 1
    selected_task = None
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task number: \t\t {task_number}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
            task_number += 1
    
    vm_task_choice = input("""-------------TASK MENU--------------
Here you may alter the completion status, due date, or assignee for a task
    \nplease enter the task number corresponding to the task you wish to modify                          
    \nAlternatively, enter '-1' to return to the previous menu
CHOICE: """).strip()

    if vm_task_choice == '-1':
        return

    try:
        vm_task_choice = int(vm_task_choice)
    except ValueError:
        print("Invalid task number. Please enter a valid task number.")
        return

    count = 0
    selected_task = None
    for t in task_list:
        if t['username'] == curr_user:
            count += 1
            if count == vm_task_choice:
                selected_task = t
                break

    if selected_task is None:
        print("Invalid task number. Please enter a valid task number.")
        return
    
    if selected_task['completed']:
        print("This task has already been completed and cannot be edited.")
        return

    edit_choice = input("Please enter 'status', 'date', or 'user' depending on what you wish to change: ").lower()

    if edit_choice == 'status':
        selected_task['completed'] = not selected_task['completed']
        print(f"Task marked as {'completed' if selected_task['completed'] else 'incomplete'} successfully.")

    elif edit_choice == 'date':
        new_date = input("Please enter the new due date (YYYY-MM-DD): ")
        try:
            new_date = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
            selected_task['due_date'] = new_date
            print("Due date updated successfully.")
        except ValueError:
            print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")

    elif edit_choice == 'user':
        new_user = input("Please enter the username of the new assignee: ")
        if new_user in [t['username'] for t in task_list]:
            selected_task['username'] = new_user
            print("Assigned user updated successfully.")
        else:
            print("Invalid user. Please enter a valid username.")

    else:
        print("Invalid choice. Please enter 'status', 'date', or 'user'.")

    # Update tasks.txt with the modified task list
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


# FUNCTION 5 - generate reports
        
def generate_report():
    task_counter = 0
    completed_counter = 0
    incomplete_counter = 0
    overdue_counter = 0
    user_tasks = {}  # Dictionary to store the number of tasks assigned to each user
    user_completed_tasks = {}  # Dictionary to store the number of completed tasks assigned to each user
    user_overdue_tasks = {}  # Dictionary to store the number of overdue tasks assigned to each user
    

      # Read tasks from tasks.txt file
    with open('tasks.txt', 'r') as taskdb:
        for line in taskdb:
            task_components = line.strip().split(';')
            task_counter += 1
            if task_components[-1] == "Yes":
                completed_counter += 1
            elif task_components[-1] == "No":
                incomplete_counter += 1
                # Check for overdue tasks
                if datetime.strptime(task_components[3], "%Y-%m-%d").date() < datetime.today().date():
                    overdue_counter += 1
                    assigned_user = task_components[0]
                    if assigned_user in user_overdue_tasks:
                        user_overdue_tasks[assigned_user] += 1
                    else:
                        user_overdue_tasks[assigned_user] = 1

            # Count tasks assigned to each user
            assigned_user = task_components[0]
            if assigned_user in user_tasks:
                user_tasks[assigned_user] += 1
            else:
                user_tasks[assigned_user] = 1

    # Generate task report
    if task_counter == 0:
        print("No tasks have been generated and tracked.")
    else:
        print("Task report generated successfully")
        incompletion_percentage = (incomplete_counter / task_counter) * 100
        overdue_percentage = (overdue_counter / task_counter) * 100
        with open('task_overview.txt', 'w') as t:
            t.write(f"The number of tasks generated and tracked is: {task_counter} \n"
                    f"The number of completed tasks is: {completed_counter} \n"
                    f"The number of incomplete tasks is: {incomplete_counter} \n"
                    f"The number of incomplete and overdue tasks is: {overdue_counter} \n"
                    f"The percentage of tasks that are incomplete: {incompletion_percentage}% \n"
                    f"The percentage of tasks that are overdue is: {overdue_percentage}%")

        # Read user data from user.txt file
    with open('user.txt', 'r') as userdb:
        users = [line.strip().split(';') for line in userdb.readlines() if line.strip()]  # Split lines and exclude empty lines
        user_counter = len(users)

    if user_counter == 0:
        print("No users have been registered")
    else:
        print("User report generated successfully")

    for t in task_list:  #  count each user's completed tasks
        assigned_user = t['username']
        if t['completed']:
            if assigned_user in user_completed_tasks:
                user_completed_tasks[assigned_user] += 1
            else:
                user_completed_tasks[assigned_user] = 1
                                               
        # write to the user_overview report
        with open('user_overview.txt', 'w') as x:
            x.write(f"The number of users registered is: {user_counter} \n"
                    f"The number of tasks generated and tracked is: {task_counter} \n")

            for user, _ in users:  # Iterate over username/password pairs
                tasks_assigned = user_tasks.get(user, 0)
                completed_tasks = user_completed_tasks.get(user, 0)
                overdue_tasks = user_overdue_tasks.get(user, 0)
                percentage_of_total_tasks = (tasks_assigned / task_counter) * 100
                if tasks_assigned != 0:
                    completion_percentage = (completed_tasks / tasks_assigned) * 100
                    outstanding_completion_percentage = 100 - completion_percentage
                    overdue_tasks_percentage = (overdue_tasks / tasks_assigned) * 100
                else:
                    completion_percentage = 0
                    overdue_tasks_percentage = 0

                    
                x.write(f"User: {user}, Tasks Assigned: {tasks_assigned}, Tasks Completed: {completed_tasks}, Percentage of total tasks assigned to user: {percentage_of_total_tasks} , Completion Percentage: {completion_percentage:.2f}%, Percentage of Tasks still needed to be completed: {outstanding_completion_percentage:.2f}%, Overdue and Incomplete Tasks Percentage: {overdue_tasks_percentage:.2f}%\n")

# FUNCTION 6 - DISPLAY STATISTICS

def display_statistics():
    generate_report() # call the code to generate the text files
    task_contents = ""
    user_contents = ""
    with open('task_overview.txt','r') as task_report:
        for line in task_report:
            task_contents = task_contents + line
    with open('user_overview.txt','r')   as user_report:
        for line in user_report:
            user_contents = user_contents + line   
        
    print(f"\n\nTask Report:\n\n{task_contents}\n\nUser Report: \n\n{user_contents}")
    

#====Login Section====
# This code reads usernames and password from the user.txt file to allow a user to login
    
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports (admin only)                
ds - Display statistics (admin only)
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()
        
    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'gr'and curr_user == 'admin':
        generate_report()

    elif menu == 'ds' and curr_user == 'admin': 
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")