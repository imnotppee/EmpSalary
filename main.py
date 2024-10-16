import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from datetime import datetime
from database import *

create_comments_table()
create_table()
# Initialize the main application window
app = ctk.CTk()
center_window(app, 1000, 600)
app.title("Employee Salary Management")

# Can't resize window
app.resizable(False, False)

# Dictionary to hold department and their corresponding positions
department_positions = {
    "Kitchen staff": ["Head Chef", "Chef", "Chef's Assistant"],
    "Managerial staff": ["Restaurant Manager", "Kitchen Manager", "Floor Manager"],
    "Floor staff": ["Cashier", "Cleaning staff", "Security guard"],
    "Bar staff": ["Bartender", "Barista"],
    "Delivery staff": ["Delivery staff", "Delivery Assistant"]
}

# Create frames for layout
frame_left = ctk.CTkFrame(app, width=600, height=500)
frame_left.grid(row=0, column=0, sticky="nsew")

frame_right = ctk.CTkFrame(app, width=400, height=500)
frame_right.grid(row=0, column=1, sticky="nsew")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Add logo and title to the header frame
#logo_image = ctk.CTkImage(Image.open("icon1.png"), size=(80, 80))

header_frame = ctk.CTkFrame(frame_left)
header_frame.pack(pady=20, padx=20, anchor="nw", fill="x")

#logo_label = ctk.CTkLabel(header_frame, image=logo_image, text="")
#logo_label.pack(side="left", padx=10)

label_title = ctk.CTkLabel(header_frame, text="Employee Salary Management", font=("Arial", 24))
label_title.pack(side="left", padx=50)

# Create input fields for employee details
label_name_frame = ctk.CTkFrame(frame_left)
label_name_frame.pack(pady=5)

label_first_name = ctk.CTkLabel(label_name_frame, text="First Name")
label_first_name.grid(row=0, column=0, padx=10)
entry_first_name = ctk.CTkEntry(label_name_frame, width=150)
entry_first_name.grid(row=0, column=1, padx=10)

label_last_name = ctk.CTkLabel(label_name_frame, text="Last Name")
label_last_name.grid(row=0, column=2, padx=10)
entry_last_name = ctk.CTkEntry(label_name_frame, width=150)
entry_last_name.grid(row=0, column=3, padx=10)

# Create frame for Date of Birth, Age, Department, and Position
info_frame = ctk.CTkFrame(frame_left)
info_frame.pack(pady=5)

label_dob = ctk.CTkLabel(info_frame, text="Date of Birth")
label_dob.grid(row=0, column=0, padx=10)
dob_entry = ctk.CTkEntry(info_frame, width=150)
dob_entry.grid(row=0, column=1, padx=10)

label_age = ctk.CTkLabel(info_frame, text="Age")
label_age.grid(row=0, column=2, padx=10)
entry_age = ctk.CTkEntry(info_frame, width=150, state='readonly')
entry_age.grid(row=0, column=3, padx=10)

dob_entry.bind("<FocusOut>", lambda event: calculate_age(dob_entry, entry_age))

# Create frame for Religion and Nationality
religion_nationality_frame = ctk.CTkFrame(frame_left)
religion_nationality_frame.pack(pady=5)

# Religion input field
label_religion = ctk.CTkLabel(religion_nationality_frame, text="Religion")
label_religion.grid(row=0, column=0, padx=10)
entry_religion = ctk.CTkEntry(religion_nationality_frame, width=150)
entry_religion.grid(row=0, column=1, padx=10)

# Nationality input field
label_nationality = ctk.CTkLabel(religion_nationality_frame, text="Nationality")
label_nationality.grid(row=0, column=2, padx=10)
entry_nationality = ctk.CTkEntry(religion_nationality_frame, width=150)
entry_nationality.grid(row=0, column=3, padx=10)

# Create frame for Department and Position
department_position_frame = ctk.CTkFrame(frame_left)
department_position_frame.pack(pady=5)

# Department selection
label_department = ctk.CTkLabel(department_position_frame, text="Department")
label_department.grid(row=1, column=0, padx=10)
department_menu = ctk.CTkComboBox(department_position_frame, values=list(department_positions.keys()), width=200)
department_menu.set("Select Department")
department_menu.grid(row=1, column=1, padx=10)

# Position selection
label_position = ctk.CTkLabel(department_position_frame, text="Position")
label_position.grid(row=1, column=2, padx=10)
position_menu = ctk.CTkComboBox(department_position_frame, values=["Select Position"]+ [pos for sublist in department_positions.values() for pos in sublist], width=200)
position_menu.set("Select Position")
position_menu.grid(row=1, column=3, padx=10)

# Create frame for Salary
salary_frame = ctk.CTkFrame(frame_left)
salary_frame.pack(pady=5)

label_salary = ctk.CTkLabel(salary_frame, text="Salary")
label_salary.grid(row=0, column=0, padx=10)
entry_salary = ctk.CTkEntry(salary_frame, width=150)  # Define entry_salary here
entry_salary.grid(row=0, column=1, padx=10)

label_start_day = ctk.CTkLabel(salary_frame, text="Starting Day")
label_start_day.grid(row=0, column=2, padx=10)
start_day_entry = ctk.CTkEntry(salary_frame, width=150)
start_day_entry.grid(row=0, column=3, padx=10)

# Create frame for Telephone, Email, and Starting Day
contact_frame = ctk.CTkFrame(frame_left)
contact_frame.pack(pady=5)

label_tel = ctk.CTkLabel(contact_frame, text="Telephone")
label_tel.grid(row=0, column=0, padx=10)
entry_tel = ctk.CTkEntry(contact_frame, width=150)
entry_tel.grid(row=0, column=1, padx=10)

label_email = ctk.CTkLabel(contact_frame, text="Email")
label_email.grid(row=0, column=2, padx=10)
entry_email = ctk.CTkEntry(contact_frame, width=150)
entry_email.grid(row=0, column=3, padx=10)

# Add button to submit employee data
btn_add = ctk.CTkButton(frame_left, text="Add Employee", command=lambda: add_employees(
    entry_first_name, entry_last_name, entry_religion, entry_nationality,
    dob_entry, entry_tel, entry_email, department_menu, position_menu, entry_salary,
))
btn_add.pack(pady=10)


# ฟังก์ชันสำหรับซ่อนปุ่ม Save
def hide_save_button():
    btn_save.grid_remove()

# ฟังก์ชันสำหรับแสดงปุ่ม Save
def show_save_button():
    btn_save.pack(padx=10)

# ปุ่ม Save Changes (บันทึกการแก้ไข)
btn_save = ctk.CTkButton(frame_left, text="Save Changes", command=lambda: [
    update_employee_details(
        edit_id_entry, entry_first_name, entry_last_name, entry_religion, entry_nationality, 
        dob_entry, entry_tel, entry_email, department_menu, position_menu, entry_salary
    ),
    hide_save_button()  # ซ่อนปุ่ม Save หลังจากบันทึกสำเร็จ
])
btn_save.pack(pady=10)
hide_save_button()  # ซ่อนปุ่ม Save ไว้ก่อนจนกว่าจะกด Edit

# Create frame for Search
search_frame = ctk.CTkFrame(frame_left)
search_frame.pack(pady=10)

# Search input field
label_search = ctk.CTkLabel(search_frame, text="Search by Name")
label_search.grid(row=0, column=0, padx=10)
search_entry = ctk.CTkEntry(search_frame, width=150)
search_entry.grid(row=0, column=1, padx=10)

# Search button
btn_search = ctk.CTkButton(search_frame, text="Search", command=lambda: search_employee(search_entry))
btn_search.grid(row=0, column=2, padx=10)

# Add the View Comments button
btn_view_comments = ctk.CTkButton(frame_left, text="View Comments")
btn_view_comments.pack(pady=10)

# Edit input field for Employee ID
label_edit_id = ctk.CTkLabel(search_frame, text="Edit Employee ID")
label_edit_id.grid(row=1, column=0, padx=10)
edit_id_entry = ctk.CTkEntry(search_frame, width=150)
edit_id_entry.grid(row=1, column=1, padx=10)

# ปุ่ม Edit สำหรับดึงข้อมูลพนักงานเพื่อแก้ไข
btn_edit = ctk.CTkButton(search_frame, text="Edit", command=lambda: [
    fetch_employee_details(
        edit_id_entry, entry_first_name, entry_last_name, entry_religion, entry_nationality, 
        dob_entry, entry_tel, entry_email, department_menu, position_menu, entry_salary
    ),
    show_save_button()  # แสดงปุ่ม Save หลังจากที่ดึงข้อมูลสำเร็จ
])
btn_edit.grid(row=1, column=2, padx=10)



# Delete input field for Employee ID
label_delete_id = ctk.CTkLabel(search_frame, text="Delete Employee ID")
label_delete_id.grid(row=2, column=0, padx=10)
delete_id_entry = ctk.CTkEntry(search_frame, width=150)
delete_id_entry.grid(row=2, column=1, padx=10)

# Delete button
btn_delete = ctk.CTkButton(search_frame, text="Delete", command=lambda: delete_employee_data(delete_id_entry))
btn_delete.grid(row=2, column=2, padx=10)

# ฟังก์ชันสำหรับลบข้อมูลพนักงาน
def delete_employee_data(entry):
    employee_id = entry.get()
    if employee_id:
        # เรียกใช้ฟังก์ชัน delete_employee จาก database.py
        delete_employee(employee_id)
        messagebox.showinfo("Success", "Employee deleted successfully!")
        entry.delete(0, ctk.END)  # ล้างช่องกรอก ID
    else:
        messagebox.showwarning("Input Error", "Please enter an Employee ID to delete.")

def open_comment_window():
    comment_window = ctk.CTkToplevel(app)  # สร้างหน้าต่างใหม่
    comment_window.title("Comment on Employee")
    comment_window.geometry("400x400")

    # ฟิลด์สำหรับกรอก Employee ID
    label_id = ctk.CTkLabel(comment_window, text="Employee ID")
    label_id.pack(pady=10)
    entry_id = ctk.CTkEntry(comment_window, width=150)
    entry_id.pack(pady=5)

    # ฟิลด์สำหรับกรอก Comment
    label_comment = ctk.CTkLabel(comment_window, text="Comment")
    label_comment.pack(pady=10)
    entry_comment = ctk.CTkEntry(comment_window, width=150)
    entry_comment.pack(pady=5)

    # ปุ่มสำหรับบันทึก Comment
    btn_save_comment = ctk.CTkButton(
        comment_window,
        text="Save Comment",
        command=lambda: save_comment(entry_id.get(), entry_comment.get())
    )
    btn_save_comment.pack(pady=20)

# Add the Comment button
btn_comment = ctk.CTkButton(frame_left, text="Comment on Employee", command=open_comment_window)
btn_comment.pack(pady=10)

def view_comments_window():
    comment_window = ctk.CTkToplevel(app)  # สร้างหน้าต่างใหม่
    comment_window.title("View Comments")
    comment_window.geometry("400x500")

    # ฟิลด์สำหรับกรอก Employee ID
    label_id = ctk.CTkLabel(comment_window, text="Employee ID")
    label_id.pack(pady=10)
    entry_id = ctk.CTkEntry(comment_window, width=150)
    entry_id.pack(pady=5)

    # Text widget สำหรับแสดงความคิดเห็น
    comments_display = ctk.CTkTextbox(comment_window, width=350, height=200)
    comments_display.pack(pady=10)

    def fetch_comments():
        employee_id = entry_id.get()
        if not employee_id:
            messagebox.showwarning("Input Error", "Please enter an Employee ID.")
            return

        try:
            connection = psycopg2.connect(
                dbname="postgres",  
                user="postgres",
                password="1234",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            # ดึงความคิดเห็นจากตาราง comments
            fetch_query = """
                SELECT comment FROM comments WHERE employee_id = %s;
            """
            cursor.execute(fetch_query, (employee_id,))
            results = cursor.fetchall()

            comments_display.delete(1.0, ctk.END)  # ล้าง Text Widget ก่อน
            if results:
                for row in results:
                    comments_display.insert(ctk.END, f"{row[0]}\n")  # แสดงความคิดเห็นแต่ละอัน
            else:
                comments_display.insert(ctk.END, "No comments found for this Employee ID.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch comments. Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

 # ปุ่มเพื่อดึงความคิดเห็น
    btn_fetch_comments = ctk.CTkButton(comment_window, text="Fetch Comments", command=fetch_comments)
    btn_fetch_comments.pack(pady=10)

# เชื่อมโยงปุ่ม View Comments
btn_view_comments.configure(command=view_comments_window)



# color's programs
new_palette = {
    "background": "#2C3639",  # Dark greenish-gray for background
    "frame_bg": "#3F4E4F",    # Muted teal for frame backgrounds
    "button_bg": "#A27B5C",   # Soft brown for buttons
    "button_fg": "#DCD7C9",   # Light beige for button text
    "label_text": "#DCD7C9",  # Light beige for label text
    "entry_bg": "#DCD7C9",    # Light beige for input fields
    "entry_fg": "#2C3639",    # Dark greenish-gray for input text
    "highlight": "#A27B5C",   # Soft brown for button hover
    "warning": "#DCD7C9"      # Light beige for warning text
}

# Apply new colors to the app and frames
app.configure(fg_color=new_palette["background"])
header_frame.configure(fg_color=new_palette["frame_bg"])
frame_left.configure(fg_color=new_palette["frame_bg"])
frame_right.configure(fg_color=new_palette["frame_bg"])
label_name_frame.configure(fg_color=new_palette["frame_bg"])
info_frame.configure(fg_color=new_palette["frame_bg"])
religion_nationality_frame.configure(fg_color=new_palette["frame_bg"])
department_position_frame.configure(fg_color=new_palette["frame_bg"])
salary_frame.configure(fg_color=new_palette["frame_bg"])
contact_frame.configure(fg_color=new_palette["frame_bg"])
search_frame.configure(fg_color=new_palette["frame_bg"])

# Apply color to the labels
label_title.configure(text_color=new_palette["label_text"])
label_first_name.configure(text_color=new_palette["label_text"])
label_last_name.configure(text_color=new_palette["label_text"])
label_dob.configure(text_color=new_palette["label_text"])
label_age.configure(text_color=new_palette["label_text"])
label_religion.configure(text_color=new_palette["label_text"])
label_nationality.configure(text_color=new_palette["label_text"])
label_department.configure(text_color=new_palette["label_text"])
label_salary.configure(text_color=new_palette["label_text"])
label_tel.configure(text_color=new_palette["label_text"])
label_email.configure(text_color=new_palette["label_text"])
label_start_day.configure(text_color=new_palette["label_text"])
label_search.configure(text_color=new_palette["label_text"])

# Apply colors to buttons
btn_add.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)
btn_search.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)

btn_comment.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)

btn_delete.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)

btn_edit.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)

btn_view_comments.configure(
    fg_color=new_palette["button_bg"], 
    hover_color=new_palette["highlight"], 
    text_color=new_palette["button_fg"]
)

# Start the application
app.mainloop()