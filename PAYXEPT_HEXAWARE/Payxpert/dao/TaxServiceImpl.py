from Payxpert.dao.ITaxService import ITaxService
from Payxpert.entity.Tax import Tax
from Payxpert.exception.TaxCalculationException import TaxCalculationException
from decimal import Decimal
import pyodbc

class TaxServiceImpl(ITaxService):

    def get_all_taxes(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT TaxID, EmployeeID, TaxYear, TaxAmount FROM Tax")
            results = cursor.fetchall()
            taxes = []
            for row in results:
                tax = Tax(
                    tax_id=row[0],
                    employee_id=row[1],
                    tax_year=row[2],
                    tax_amount=row[3]
                )
                taxes.append(tax)
            return taxes
        except Exception as e:
            raise Exception(f"Error fetching taxes: {e}")
        finally:
            conn.close()

    def __init__(self, conn):
        self.conn = conn

    def calculate_tax(self, employee_id, tax_year):
        cursor = self.conn.cursor()
        try:
            print(f"Fetching BasicSalary for Employee ID: {employee_id}")
            cursor.execute("SELECT BasicSalary FROM Payroll WHERE EmployeeID = ?", (employee_id,))
            row = cursor.fetchone()

            if row:
                basic_salary = Decimal(row[0])  # Ensure it's a Decimal
                tax_rate = Decimal('0.15')  # Example tax rate of 15%
                taxable_income = basic_salary * tax_rate
                tax_amount = taxable_income * tax_rate  # Tax amount based on taxable income and tax rate

                # Create a Tax object with calculated values, using None for tax_id if needed
                tax = Tax(None, employee_id, tax_year, taxable_income, tax_amount)

                # Insert into the database
                insert_query = "INSERT INTO Tax (EmployeeID, TaxYear, TaxableIncome, TaxAmount) VALUES (?, ?, ?, ?)"
                cursor.execute(insert_query, (tax.employee_id, tax.tax_year, tax.taxable_income, tax.tax_amount))
                self.conn.commit()
                print(f"Tax record inserted for Employee ID {employee_id}.")
                return tax  # Return the tax object if needed
            else:
                raise TaxCalculationException(
                    f"Failed to calculate tax for Employee ID {employee_id}. No salary found.")

        except pyodbc.DatabaseError as e:
            raise TaxCalculationException(f"Database error occurred: {e}")
        finally:
            cursor.close()

    def get_tax_by_id(self, tax_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Tax WHERE TaxID = ?", (tax_id,))
        row = cursor.fetchone()
        if row:
            return Tax(row[0], row[1], row[2], row[3], row[4])  # TaxID included
        else:
            raise TaxCalculationException(f"Tax with ID {tax_id} not found.")

    def get_taxes_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Tax WHERE EmployeeID = ?", (employee_id,))
        taxes = []
        for row in cursor.fetchall():
            taxes.append(Tax(row[0], row[1], row[2], row[3], row[4]))  # TaxID included
        return taxes

    def get_taxes_for_year(self, tax_year):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Tax WHERE TaxYear = ?", (tax_year,))
        taxes = []
        for row in cursor.fetchall():
            taxes.append(Tax(row[0], row[1], row[2], row[3], row[4]))  # TaxID included
        return taxes

    def calculate_tax_test(self, employee_id, income):
        try:
            cursor = self.conn.cursor()

            # Mock example query, adjust to your actual query
            query = f"SELECT tax_rate FROM TaxTable WHERE employee_id = ?"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()

            if result:
                tax_rate = result[0]  # Assuming tax_rate is fetched from the DB
                tax = income * tax_rate / 100  # Example tax calculation

                # Insert tax record
                insert_query = "INSERT INTO TaxRecords (employee_id, tax_amount) VALUES (?, ?)"
                cursor.execute(insert_query, (employee_id, tax))
                self.conn.commit()
                print(f"Tax record inserted for Employee ID {employee_id}.")
                return tax  # Ensure that the tax value is returned

            return None  # If no result is found

        except Exception as e:
            print(f"Error calculating tax for Employee ID {employee_id}: {e}")
            return None

    def delete_tax_by_employee_id(self, emp_id):
        cursor = self.conn.cursor()
        try:
            # Check if tax records exist for the employee
            cursor.execute("SELECT * FROM Tax WHERE EmployeeID = ?", (emp_id,))
            taxes = cursor.fetchall()

            if not taxes:
                raise TaxCalculationException(f"No tax records found for Employee ID: {emp_id}")

            # Delete tax records for the employee
            cursor.execute("DELETE FROM Tax WHERE EmployeeID = ?", (emp_id,))
            self.conn.commit()
            print(f"Tax records for Employee ID {emp_id} have been successfully deleted.")

        except pyodbc.DatabaseError as e:
            self.conn.rollback()
            raise TaxCalculationException(f"Error deleting tax for Employee ID {emp_id}: {e}")
        finally:
            cursor.close()
