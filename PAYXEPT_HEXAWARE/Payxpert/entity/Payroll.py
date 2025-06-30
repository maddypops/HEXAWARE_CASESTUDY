class Payroll:
    def __init__(self, payroll_id, employee_id, pay_period_start_date, pay_period_end_date,
                 basic_salary, overtime_pay, deductions, net_salary):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.pay_period_start_date = pay_period_start_date
        self.pay_period_end_date = pay_period_end_date
        self.basic_salary = basic_salary
        self.overtime_pay = overtime_pay
        self.deductions = deductions
        self.net_salary = net_salary

    def calculate_gross_salary(self):
        return self.basic_salary + self.overtime_pay

    def display_payroll_info(self):
        return {
            'Payroll ID': self.payroll_id,
            'Employee ID': self.employee_id,
            'Pay Period Start Date': self.pay_period_start_date,
            'Pay Period End Date': self.pay_period_end_date,
            'Basic Salary': self.basic_salary,
            'Overtime Pay': self.overtime_pay,
            'Deductions': self.deductions,
            'Net Salary': self.net_salary,
            'Gross Salary': self.calculate_gross_salary()
        }

    def __str__(self):
        return (f"Payroll(Payroll ID: {self.payroll_id}, Employee ID: {self.employee_id}, "
                f"Pay Period: {self.pay_period_start_date} to {self.pay_period_end_date}, "
                f"Basic Salary: {self.basic_salary}, Overtime Pay: {self.overtime_pay}, "
                f"Deductions: {self.deductions}, Net Salary: {self.net_salary})")
