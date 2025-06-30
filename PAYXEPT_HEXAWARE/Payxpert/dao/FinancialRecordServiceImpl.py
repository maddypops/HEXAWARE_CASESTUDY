from Payxpert.dao.IFinancialRecordService import IFinancialRecordService
from Payxpert.entity.FinancialRecord import FinancialRecord
from Payxpert.exception.FinancialRecordException import FinancialRecordException
import pyodbc
class FinancialRecordServiceImpl(IFinancialRecordService):

    def __init__(self, conn):
        self.conn = conn

    def add_financial_record(self, employee_id, description, amount, record_type, record_date):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO FinancialRecord (EmployeeID, Description, Amount, RecordType, RecordDate) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (employee_id, description, amount, record_type, record_date))
        self.conn.commit()

    def get_financial_record_by_id(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM FinancialRecord WHERE RecordID = ?", (record_id,))
        row = cursor.fetchone()
        if row:
            return FinancialRecord(*row)
        else:
            raise FinancialRecordException(f"Financial record with ID {record_id} not found.")

    def get_financial_records_for_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM FinancialRecord WHERE EmployeeID = ?", (employee_id,))
        records = []
        for row in cursor.fetchall():
            records.append(FinancialRecord(*row))
        return records

    def get_financial_records_for_date(self, record_date):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM FinancialRecord WHERE RecordDate = ?", (record_date,))
        records = []
        for row in cursor.fetchall():
            records.append(FinancialRecord(*row))
        return records

    def delete_financial_records_by_employee_id(self, emp_id):
        cursor = self.conn.cursor()
        try:
            # Check if financial records exist for the employee
            cursor.execute("SELECT * FROM FinancialRecord WHERE EmployeeID = ?", (emp_id,))
            records = cursor.fetchall()

            if not records:
                raise FinancialRecordException(f"No financial records found for Employee ID: {emp_id}")

            # Delete financial records for the employee
            cursor.execute("DELETE FROM FinancialRecord WHERE EmployeeID = ?", (emp_id,))
            self.conn.commit()
            print(f"Financial records for Employee ID {emp_id} have been successfully deleted.")

        except pyodbc.DatabaseError as e:
            self.conn.rollback()
            raise FinancialRecordException(f"Error deleting financial records for Employee ID {emp_id}: {e}")
        finally:
            cursor.close()
