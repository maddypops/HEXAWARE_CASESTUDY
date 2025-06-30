from Payxpert.dao.IPayrollService import IPayrollService
from Payxpert.entity.Employee import Employee
from Payxpert.entity.Payroll import Payroll
from Payxpert.exception.PayrollGenerationException import PayrollGenerationException
import pyodbc


class PayrollServiceImpl(IPayrollService):

    def generate_payroll_from_ui(self, employee_id, start_date, end_date, overtime_pay, deductions):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Salary FROM Employee WHERE EmployeeID = ?", (employee_id,))
            result = cursor.fetchone()
            if not result:
                raise Exception("Employee not found.")
            basic_salary = result[0]
            net_salary = basic_salary + overtime_pay - deductions

            cursor.execute("""
                           INSERT INTO Payroll (EmployeeID, PayPeriodStartDate, PayPeriodEndDate, BasicSalary,
                                                OvertimePay, Deductions, NetSalary)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, (employee_id, start_date, end_date, basic_salary, overtime_pay, deductions, net_salary))
            conn.commit()
        except Exception as e:
            raise Exception(f"Payroll generation error: {e}")
        finally:
            conn.close()

    def get_all_payrolls(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT PayrollID, EmployeeID, PayPeriodStartDate, PayPeriodEndDate, NetSalary FROM Payroll")
            results = cursor.fetchall()
            payrolls = []
            for row in results:
                payroll = Payroll(
                    payroll_id=row[0],
                    employee_id=row[1],
                    start_date=row[2],
                    end_date=row[3],
                    net_salary=row[4]
                )
                payrolls.append(payroll)
            return payrolls
        except Exception as e:
            raise Exception(f"Error fetching payrolls: {e}")
        finally:
            conn.close()

    def calculate_gross_salary(base_salary):
        # Define logic for gross salary calculation.
        # This might include adding bonuses, allowances, etc.
        # For now, let's assume no extra allowances, so gross salary is equal to base salary.

        if base_salary < 0:
            raise ValueError("Salary cannot be negative")

        # You can add other components to the gross salary as needed.
        gross_salary = base_salary  # Simplified logic for now
        return gross_salary

    def __init__(self, conn):
        self.conn = conn

    def generate_payroll(self, employee_id, start_date, end_date, basic_salary, overtime_pay, deductions):
        cursor = self.conn.cursor()

        # Calculate net salary based on provided values
        net_salary = basic_salary + overtime_pay - deductions

        # Prepare the SQL query to insert the payroll record
        insert_query = """
            INSERT INTO Payroll (EmployeeID, PayPeriodStartDate, PayPeriodEndDate, 
                                 BasicSalary, OvertimePay, Deductions, NetSalary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        # Execute the insert query with the provided payroll details
        cursor.execute(insert_query,
                       (employee_id, start_date, end_date, basic_salary, overtime_pay, deductions, net_salary))

        # Commit the transaction to save changes
        self.conn.commit()

        # Optionally, you can return the generated Payroll ID or any other relevant info
        print("Payroll generated successfully for Employee ID:", employee_id)

    def get_payroll_by_id(self, payroll_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Payroll WHERE PayrollID = ?", (payroll_id,))
        row = cursor.fetchone()
        if row:
            return Payroll(*row)
        else:
            raise PayrollGenerationException(f"Payroll with ID {payroll_id} not found.")

    def get_payrolls_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Payroll WHERE EmployeeID = ?", (employee_id,))
        payrolls = []
        for row in cursor.fetchall():
            payrolls.append(Payroll(*row))
        return payrolls

    def get_payrolls_for_period(self, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Payroll WHERE PayPeriodStartDate >= ? AND PayPeriodEndDate <= ?",
                       (start_date, end_date))
        payrolls = []
        for row in cursor.fetchall():
            payrolls.append(Payroll(*row))
        return payrolls

    def calculate_net_salary(self, gross_salary, deductions):
        # Logic to calculate net salary by subtracting deductions from gross salary
        net_salary = gross_salary - deductions
        return net_salary

    def calculate_deductions(self, employee):
        # Example logic for calculating deductions (tax, insurance, etc.)
        # You can modify this to suit your actual deduction calculation needs
        return employee.salary * 0.1  # Assuming 10% deductions from salary

    def get_employee_by_id(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Employee WHERE EmployeeID = ?", (employee_id,))
        row = cursor.fetchone()
        if row:
            return Employee(*row)  # Assuming Employee class constructor matches database row
        else:
            raise PayrollGenerationException(f"Employee with ID {employee_id} not found.")

    def process_payroll(self, employee_ids):
        results = []
        for employee_id in employee_ids:
            try:
                # Retrieve employee object
                employee = self.get_employee_by_id(employee_id)

                # Ensure we are dealing with an Employee object and not a primitive type like float
                if not isinstance(employee, Employee):
                    raise ValueError(f"Employee {employee_id} is not a valid Employee object.")

                # Check if employee exists and salary is valid
                if not employee or not employee.salary:
                    raise ValueError(f"Employee {employee_id} not found or salary is missing.")

                # Convert employee's salary (which should be numeric) to float
                salary = float(employee.salary)

                # Deduction calculation logic
                deductions = self.calculate_deductions(employee.salary)
                net_salary = salary - deductions

                # Append successful result
                results.append({
                    'employee_id': employee_id,
                    'success': True,
                    'net_salary': net_salary
                })

            except Exception as e:
                # Append failure result with error message
                results.append({
                    'employee_id': employee_id,
                    'success': False,
                    'message': str(e)
                })
                print(f"Error processing payroll for Employee ID {employee_id}: {e}")

        return results

    def delete_payroll_by_employee_id(self, emp_id):
        cursor = self.conn.cursor()
        try:
            # Check if payroll records exist for the employee
            cursor.execute("SELECT * FROM Payroll WHERE EmployeeID = ?", (emp_id,))
            payrolls = cursor.fetchall()

            if not payrolls:
                raise PayrollGenerationException(f"No payroll records found for Employee ID: {emp_id}")

            # Delete payroll records for the employee
            cursor.execute("DELETE FROM Payroll WHERE EmployeeID = ?", (emp_id,))
            self.conn.commit()
            print(f"Payroll records for Employee ID {emp_id} have been successfully deleted.")

        except pyodbc.DatabaseError as e:
            self.conn.rollback()
            raise PayrollGenerationException(f"Error deleting payroll for Employee ID {emp_id}: {e}")
        finally:
            cursor.close()

    def update_payroll(self, payroll_id, new_basic_salary, new_overtime_pay, new_deductions):
        cursor = self.conn.cursor()

        # Check if the payroll exists before attempting to update
        cursor.execute("SELECT * FROM Payroll WHERE PayrollID = ?", (payroll_id,))
        payroll_record = cursor.fetchone()

        if payroll_record:
            # If the payroll exists, perform the update
            cursor.execute("""
                UPDATE Payroll
                SET BasicSalary = ?, OvertimePay = ?, Deductions = ?
                WHERE PayrollID = ?
            """, (new_basic_salary, new_overtime_pay, new_deductions, payroll_id))

            self.conn.commit()  # Commit the changes
        else:
            raise PayrollGenerationException(f"Payroll with ID {payroll_id} not found.")
