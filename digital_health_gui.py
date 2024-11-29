import tkinter as tk
from tkinter import messagebox
from user_management import register_user, is_user_registered
from health_records import add_health_record, get_patient_records, get_all_patients

def register():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()
    if not username or not password or not role:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    register_user(username, password, role)
    messagebox.showinfo("Success", "User registered successfully!")

def login():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()
    if not username or not password or not role:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    if is_user_registered(username, password, role):
        messagebox.showinfo("Success", f"Welcome {username}!")
        if role == "Patient":
            open_patient_dashboard(username)
        elif role == "Doctor":
            open_doctor_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username, password, or role!")

def open_patient_dashboard(patient_name):
    dashboard = tk.Toplevel(root)
    dashboard.title(f"{patient_name}'s Dashboard")

    tk.Label(dashboard, text="Add New Record:").pack()
    record_entry = tk.Entry(dashboard, width=50)
    record_entry.pack()

    def add_record():
        record = record_entry.get()
        if not record:
            messagebox.showwarning("Input Error", "Record cannot be empty!")
            return
        response = add_health_record(patient_name, record)
        messagebox.showinfo("Success", response)
        record_entry.delete(0, tk.END)

    tk.Button(dashboard, text="Add Record", command=add_record).pack()
    tk.Button(dashboard, text="View Records", command=lambda: view_patient_records(patient_name)).pack()

def open_doctor_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Doctor's Dashboard")

    tk.Label(dashboard, text="Select a Patient:").pack()
    patients = get_all_patients()

    if not patients:
        messagebox.showinfo("No Patients", "No patients have any records yet.")
        return

    patient_var = tk.StringVar(value=patients[0])
    patient_dropdown = tk.OptionMenu(dashboard, patient_var, *patients)
    patient_dropdown.pack()

    def view_selected_patient_records():
        selected_patient = patient_var.get()
        view_patient_records(selected_patient)

    tk.Button(dashboard, text="View Patient Records", command=view_selected_patient_records).pack()

def view_patient_records(patient_name):
    records = get_patient_records(patient_name)
    if not records:
        messagebox.showinfo("No Records", f"No records found for patient: {patient_name}")
    else:
        formatted_records = "\n\n".join(records)
        messagebox.showinfo(f"{patient_name}'s Records", formatted_records)

# GUI Setup
root = tk.Tk()
root.title("Digital Health Records")

# Role selection
role_var = tk.StringVar(value="Patient")
tk.Label(root, text="Role:").pack()
tk.Radiobutton(root, text="Patient", variable=role_var, value="Patient").pack()
tk.Radiobutton(root, text="Doctor", variable=role_var, value="Doctor").pack()

# Username and Password
tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Buttons
tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()

root.mainloop()
