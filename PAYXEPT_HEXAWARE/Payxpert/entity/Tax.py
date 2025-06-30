class Tax:
    def __init__(self, tax_id, employee_id, tax_year, taxable_income, tax_amount):
        self.tax_id = tax_id
        self.employee_id = employee_id
        self.tax_year = tax_year
        self.taxable_income = taxable_income
        self.tax_amount = tax_amount

    def display_tax_info(self):
        return (f"TaxID: {self.tax_id}, EmployeeID: {self.employee_id}, "
                f"TaxYear: {self.tax_year}, TaxableIncome: {self.taxable_income}, "
                f"TaxAmount: {self.tax_amount}")

    def __str__(self):
        return (f"Tax ID: {self.tax_id}, Employee ID: {self.employee_id}, "
                f"Tax Year: {self.tax_year}, Taxable Income: {self.taxable_income:.2f}, "
                f"Tax Amount: {self.tax_amount:.2f}")
