import streamlit as st
from datetime import datetime
from dao.EmployeeServiceImpl import EmployeeServiceImpl
from dao import PayrollServiceImpl
from dao import TaxServiceImpl
from dao.DatabaseContext import DatabaseContext

conn_string = ("DRIVER={ODBC Driver 17 for SQL Server};"
               "SERVER=MADDYPOPS;"
               "DATABASE=payroll;"
               "Trusted_Connection=yes;")
db_context = DatabaseContext(conn_string)
conn = db_context.get_connection()

# Initialize services
employee_service = EmployeeServiceImpl
payroll_service = PayrollServiceImpl
tax_service = TaxServiceImpl


st.set_page_config(page_title="Payroll Management System", layout="wide")

def add_employee_from_ui(self, first_name, last_name, dob, gender, email, phone, address, position, salary, joining_date, termination_date=None):
    conn = self.db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Employee (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, Salary, JoiningDate, TerminationDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, dob, gender, email, phone, address, position, salary, joining_date, termination_date))
        conn.commit()
    except Exception as e:
        raise Exception(f"Database error: {e}")
    finally:
        conn.close()


# Sidebar Menu
menu = ["Home", "Add Employee", "View Employees", "Generate Payroll", "View Payrolls", "Calculate Tax", "View Taxes", "Search Employee"]
choice = st.sidebar.selectbox("Menu", menu)

# Home Page
if choice == "Home":
    st.title("Payroll Management System")

# Add Employee Page
elif choice == "Add Employee":
    st.subheader("Add New Employee")
    with st.form("add_employee_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female"])
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        position = st.text_input("Position")
        salary = st.number_input("Salary", min_value=0)
        joining_date = st.date_input("Joining Date")
        termination_date = st.text_input("Termination Date (optional)")

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            try:
                employee_service.add_employee_from_ui(first_name, last_name, dob, gender, email, phone, address, position, salary, joining_date, termination_date)
                st.success(f"Employee {first_name} {last_name} added successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# View Employees Page
elif choice == "View Employees":
    st.subheader("All Employees")
    employees = employee_service.get_all_employees()
    if employees:
        for emp in employees:
            st.write(f"ID: {emp.employee_id}, Name: {emp.first_name} {emp.last_name}, Position: {emp.position}")
    else:
        st.warning("No employees found.")

# Generate Payroll Page
elif choice == "Generate Payroll":
    st.subheader("Generate Payroll")
    employee_id = st.number_input("Enter Employee ID", min_value=1)
    start_date = st.date_input("Pay Period Start Date")
    end_date = st.date_input("Pay Period End Date")
    overtime_pay = st.number_input("Enter Overtime Pay", min_value=0)
    deductions = st.number_input("Enter Deductions", min_value=0)
    submitted = st.button("Generate Payroll")

    if submitted:
        try:
            payroll_service.generate_payroll_from_ui(employee_id, start_date, end_date, overtime_pay, deductions)
            st.success("Payroll generated successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# View Payrolls Page
elif choice == "View Payrolls":
    st.subheader("All Payroll Records")
    payrolls = payroll_service.get_all_payrolls()
    if payrolls:
        for p in payrolls:
            st.write(f"PayrollID: {p.payroll_id}, EmployeeID: {p.employee_id}, Net Salary: {p.net_salary}, Period: {p.start_date} to {p.end_date}")
    else:
        st.warning("No payroll records found.")

# Calculate Tax Page
elif choice == "Calculate Tax":
    st.subheader("Calculate Tax")
    employee_id = st.number_input("Enter Employee ID for Tax Calculation", min_value=1)
    tax_year = st.number_input("Enter Tax Year", min_value=2000, max_value=2100, value=2024)
    submitted = st.button("Calculate Tax")

    if submitted:
        try:
            tax_service.calculate_tax(employee_id, tax_year)
            st.success(f"Tax calculated successfully for employee {employee_id} for the year {tax_year}!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# View Taxes Page
elif choice == "View Taxes":
    st.subheader("All Tax Records")
    taxes = tax_service.get_all_taxes()
    if taxes:
        for t in taxes:
            st.write(f"TaxID: {t.tax_id}, EmployeeID: {t.employee_id}, Year: {t.tax_year}, Tax Amount: {t.tax_amount}")
    else:
        st.warning("No tax records found.")

# Search Employee by ID
elif choice == "Search Employee":
    st.subheader("Search Employee by ID")
    emp_id = st.number_input("Enter Employee ID to Search", min_value=1)
    submitted = st.button("Search")

    if submitted:
        try:
            emp = employee_service.get_employee_by_id(emp_id)
            if emp:
                st.write(f"ID: {emp.employee_id}")
                st.write(f"Name: {emp.first_name} {emp.last_name}")
                st.write(f"Email: {emp.email}")
                st.write(f"Position: {emp.position}")
                st.write(f"Joining Date: {emp.joining_date}")
            else:
                st.warning("Employee not found.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
