class ReportGenerator:
    def __init__(self, payroll_service, tax_service, financial_service):
        self.payroll_service = payroll_service
        self.tax_service = tax_service
        self.financial_service = financial_service

    def generate_payroll_report(self, start_date, end_date):
        # Fetch payrolls for the given period
        payrolls = self.payroll_service.get_payrolls_for_period(start_date, end_date)
        if payrolls:
            print(f"\nPayroll Report from {start_date} to {end_date}:")
            for payroll in payrolls:
                print(payroll.display_payroll_info())
        else:
            print(f"No payroll records found for the given period: {start_date} to {end_date}")

    def generate_tax_report(self, tax_year):
        # Fetch taxes for the given year
        taxes = self.tax_service.get_taxes_for_year(tax_year)
        if taxes:
            print(f"\nTax Report for Year: {tax_year}")
            for tax in taxes:
                print(tax)
        else:
            print(f"No tax records found for the year: {tax_year}")

    def generate_financial_report(self, emp_id):
        # Fetch financial records for the employee
        financial_records = self.financial_service.get_financial_records_for_employee(emp_id)
        if financial_records:
            print(f"\nFinancial Records for Employee ID: {emp_id}")
            for record in financial_records:
                print(record)
        else:
            print(f"No financial records found for Employee ID: {emp_id}")
