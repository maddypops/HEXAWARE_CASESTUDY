class FinancialRecord:
    def __init__(self, record_id, employee_id, record_date, description, amount, record_type):
        self.record_id = record_id
        self.employee_id = employee_id
        self.record_date = record_date
        self.description = description
        self.amount = amount
        self.record_type = record_type

    def display_financial_info(self):
        return {
            'Record ID': self.record_id,
            'Employee ID': self.employee_id,
            'Date': self.record_date,
            'Description': self.description,
            'Amount': self.amount,
            'Type': self.record_type
        }

    def __str__(self):
        return (f"Record ID: {self.record_id}, Employee ID: {self.employee_id}, "
                f"Date: {self.record_date}, Description: {self.description}, "
                f"Amount: {self.amount}, Type: {self.record_type}")

