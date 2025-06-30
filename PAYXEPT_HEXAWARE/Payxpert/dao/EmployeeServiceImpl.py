import pyodbc
from Payxpert.dao.IEmployeeService import IEmployeeService
from Payxpert.entity.Employee import Employee
from Payxpert.exception.EmployeeNotFoundException import EmployeeNotFoundException
from Payxpert.exception.InvalidInputException import InvalidInputException
from Payxpert.util.ValidationService import ValidationService

class EmployeeServiceImpl(IEmployeeService):

    def __init__(self, conn):
        self.conn = conn

    def get_employee_by_id(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT EmployeeID, FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, Salary, JoiningDate, TerminationDate FROM Employee WHERE EmployeeID = ?",
            (employee_id,))
        row = cursor.fetchone()

        if row:
            employee = Employee(
                employee_id=row[0],
                first_name=row[1],
                last_name=row[2],
                dob=row[3],
                gender=row[4],
                email=row[5],
                phone=row[6],
                address=row[7],
                position=row[8],
                salary=row[9],
                joining_date=row[10],
                termination_date=row[11]
            )
            return employee
        else:
            raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")

    def get_all_employees(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT EmployeeID, FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, Salary, JoiningDate, TerminationDate FROM Employee")
        employees = []
        for row in cursor.fetchall():
            employee = Employee(
                employee_id=row[0],
                first_name=row[1],
                last_name=row[2],
                dob=row[3],
                gender=row[4],
                email=row[5],
                phone=row[6],
                address=row[7],
                position=row[8],
                salary=row[9],
                joining_date=row[10],
                termination_date=row[11]
            )
            employees.append(employee)
        return employees

    def add_employee(self, employee):
        try:
            # Validate employee attributes using ValidationService
            ValidationService.validate_non_empty(employee.first_name, "First name")
            ValidationService.validate_non_empty(employee.last_name, "Last name")
            ValidationService.validate_positive_number(employee.salary, "Salary")
            ValidationService.validate_email(employee.email)
            ValidationService.validate_phone_number(employee.phone)
            ValidationService.validate_date(employee.dob)  # Assuming dob is in YYYY-MM-DD format
            ValidationService.validate_non_empty(employee.position, "Position")
            ValidationService.validate_non_empty(employee.address, "Address")

            cursor = self.conn.cursor()
            query = """
                INSERT INTO Employee 
                (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address, Position, Salary, JoiningDate, TerminationDate) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                employee.first_name,
                employee.last_name,
                employee.dob,
                employee.gender,
                employee.email,
                employee.phone,
                employee.address,
                employee.position,
                employee.salary,
                employee.joining_date,
                employee.termination_date
            ))
            self.conn.commit()  # Commit the changes after the insert
            print("Employee added successfully.")

        except InvalidInputException as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"An error occurred while adding the employee: {e}")

    def update_employee(self, employee):
        try:
            # Proceed with the update without validation
            cursor = self.conn.cursor()
            query = """
                UPDATE Employee 
                SET FirstName = ?, LastName = ?, DateOfBirth = ?, Gender = ?, Email = ?, PhoneNumber = ?, Address = ?, Position = ?, Salary = ?, JoiningDate = ?, TerminationDate = ? 
                WHERE EmployeeID = ?
            """
            cursor.execute(query, (
                employee.first_name,
                employee.last_name,
                employee.dob,
                employee.gender,
                employee.email,
                employee.phone,
                employee.address,
                employee.position,
                employee.salary,
                employee.joining_date,
                employee.termination_date,
                employee.employee_id
            ))
            if cursor.rowcount == 0:
                raise EmployeeNotFoundException(f"Employee with ID {employee.employee_id} not found.")
            self.conn.commit()  # Commit the changes after the update
            print("Employee updated successfully.")

        except EmployeeNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred while updating the employee: {e}")

    def remove_employee(self, employee_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Employee WHERE EmployeeID = ?", (employee_id,))
            if cursor.rowcount == 0:
                raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found.")
            self.conn.commit()  # Commit the changes after the delete
            print(f"Employee with ID {employee_id} removed successfully.")
        except EmployeeNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred while removing the employee: {e}")
