from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from tkinter import messagebox
from datetime import datetime

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

def add_employees(entry_firstname, entry_lastname, entry_religion, entry_nationality, entry_dob, entry_tel, entry_email, entry_department, entry_position, entry_salary):
    firstname = entry_firstname.get().strip()
    lastname = entry_lastname.get().strip()
    religion = entry_religion.get().strip()
    nationality = entry_nationality.get().strip()
    dob = entry_dob.get().strip()
    tel = entry_tel.get().strip()
    email = entry_email.get().strip()
    department = entry_department.get().strip()
    position = entry_position.get().strip()
    salary = entry_salary.get().strip()

    if firstname and lastname and department != "Select Department" and position != "Select Position":
        # Logic to save employee details to the database or other storage
        messagebox.showinfo("Success", "Employee added successfully")
    else:
        messagebox.showwarning("Input Error", "Please fill in all the required fields")
        
    # Database connection
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Insert data into the employees table
        insert_query = """
        INSERT INTO employees (firstname, lastname, religion, nationality, dob, tel, email, department, position, salary)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (firstname, lastname, religion, nationality, dob, tel, email, department, position, salary))

        # Commit the transaction
        connection.commit()

        # Success message
        messagebox.showinfo("Success", f"Employee {firstname} {lastname} has been added successfully.")

    except Exception as e:
        # Rollback in case of error
        if connection:
            connection.rollback()
        messagebox.showerror("Error", f"Failed to add employee. Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def check_database_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        connection.close()
        print("Database connection successful!")  # Changed to print to avoid tkinter dependency
    except Exception as e:
        print(f"Cannot connect to the database: {e}")

# ฟังก์ชันสร้างตาราง comments
def create_comments_table():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                employee_id INT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'comments' is ready.")  # แสดงผลใน console
    except Exception as e:
        print(f"Error creating comments table: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_table():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id SERIAL PRIMARY KEY,
                firstname VARCHAR(50),
                lastname VARCHAR(50),
                religion VARCHAR(50),
                nationality VARCHAR(50),
                dob DATE,
                tel VARCHAR(10),
                email VARCHAR(50),
                department VARCHAR(20),
                position VARCHAR(20),
                salary NUMERIC(10, 2)
            );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'employees' is ready.")  # Changed to print to avoid tkinter dependency
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def calculate_age(dob_entry, entry_age):
    dob = dob_entry.get().strip()
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        
        entry_age.configure(state='normal')
        entry_age.delete(0, "end")
        entry_age.insert(0, str(age))
        entry_age.configure(state='readonly')
    except ValueError:
        messagebox.showerror("Invalid Date Format", "Please enter the date in YYYY-MM-DD format.")

# Function to validate date format
def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format.")
        return False


#หาชื่อพนักงาน
def search_employee(search_entry):
    search_name = search_entry.get().strip()

    if not search_name:
        messagebox.showwarning("Input Error", "Please enter a name to search.")
        return

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # ค้นหาชื่อพนักงานจากฐานข้อมูล (ค้นหาจากชื่อหรือนามสกุล)
        search_query = """
            SELECT firstname, lastname, religion, nationality, dob, tel, email, department, position, salary 
            FROM employees 
            WHERE firstname ILIKE %s OR lastname ILIKE %s;
        """
        cursor.execute(search_query, (f"%{search_name}%", f"%{search_name}%"))
        results = cursor.fetchall()

        # ตรวจสอบว่ามีข้อมูลพนักงานที่ตรงกับการค้นหาหรือไม่
        if results:
            messagebox.showinfo("Search Results", f"Found {len(results)} result(s):\n\n" + 
                                "\n".join([f"Name: {r[0]} {r[1]}, Department: {r[7]}, Position: {r[8]}" for r in results]))
        else:
            messagebox.showinfo("No Results", "No employees found with that name.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to search employee. Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

#แก้ไขข้อมูลพนักงาน
def fetch_employee_details(edit_id_entry, entry_firstname, entry_lastname, entry_religion, entry_nationality, dob_entry, entry_tel, entry_email, department_menu, position_menu, entry_salary):
    employee_id = edit_id_entry.get().strip()

    if not employee_id:
        messagebox.showwarning("Input Error", "Please enter an Employee ID to edit.")
        return

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # ค้นหาข้อมูลพนักงานจากฐานข้อมูลตามรหัสพนักงาน
        fetch_query = """
            SELECT firstname, lastname, religion, nationality, dob, tel, email, department, position, salary 
            FROM employees 
            WHERE employee_id = %s;
        """
        cursor.execute(fetch_query, (employee_id,))
        result = cursor.fetchone()

        if result:
            # เติมข้อมูลลงในฟิลด์ต่าง ๆ
            entry_firstname.delete(0, "end")
            entry_firstname.insert(0, result[0])

            entry_lastname.delete(0, "end")
            entry_lastname.insert(0, result[1])

            entry_religion.delete(0, "end")
            entry_religion.insert(0, result[2])

            entry_nationality.delete(0, "end")
            entry_nationality.insert(0, result[3])

            dob_entry.delete(0, "end")
            dob_entry.insert(0, result[4])

            entry_tel.delete(0, "end")
            entry_tel.insert(0, result[5])

            entry_email.delete(0, "end")
            entry_email.insert(0, result[6])

            department_menu.set(result[7])
            position_menu.set(result[8])

            entry_salary.delete(0, "end")
            entry_salary.insert(0, result[9])

        else:
            messagebox.showinfo("No Results", "No employee found with that ID.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch employee details. Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
#ตอน2
def update_employee_details(edit_id_entry, entry_firstname, entry_lastname, entry_religion, entry_nationality, dob_entry, entry_tel, entry_email, department_menu, position_menu, entry_salary):
    employee_id = edit_id_entry.get().strip()
    firstname = entry_firstname.get().strip()
    lastname = entry_lastname.get().strip()
    religion = entry_religion.get().strip()
    nationality = entry_nationality.get().strip()
    dob = dob_entry.get().strip()
    tel = entry_tel.get().strip()
    email = entry_email.get().strip()
    department = department_menu.get().strip()
    position = position_menu.get().strip()
    salary = entry_salary.get().strip()

    if not employee_id or not firstname or not lastname or department == "Select Department" or position == "Select Position":
        messagebox.showwarning("Input Error", "Please fill in all the required fields.")
        return

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # อัปเดตข้อมูลพนักงานในฐานข้อมูล
        update_query = """
            UPDATE employees
            SET firstname = %s, lastname = %s, religion = %s, nationality = %s, dob = %s, tel = %s, email = %s, department = %s, position = %s, salary = %s
            WHERE employee_id = %s;
        """
        cursor.execute(update_query, (firstname, lastname, religion, nationality, dob, tel, email, department, position, salary, employee_id))

        connection.commit()

        messagebox.showinfo("Success", f"Employee ID {employee_id} has been updated successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update employee details. Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def delete_employee(employee_id):
    try:
        # เชื่อมต่อกับฐานข้อมูล PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"                        
        )
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error occurred:", e)
    finally:
        conn.close()


def save_comment(employee_id, comment):
    try:
        # เชื่อมต่อกับฐานข้อมูล PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AsPpeez1875",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (employee_id, comment) VALUES (%s, %s)", (employee_id, comment))
        conn.commit()
        cursor.close()

        # แสดงข้อความยืนยัน
        messagebox.showinfo("Success", "Comment saved successfully!")
    except Exception as e:
        print("Error occurred:", e)
        messagebox.showerror("Error", "Failed to save comment.")
    finally:
        conn.close()