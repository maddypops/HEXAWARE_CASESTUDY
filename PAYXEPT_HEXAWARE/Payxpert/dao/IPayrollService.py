from abc import ABC, abstractmethod

class IPayrollService:
    def generate_payroll(self, employee_id, start_date, end_date, basic_salary, overtime_pay, deductions):
        """
        Generates payroll for an employee for a given pay period.

        Parameters:
        - employee_id: The ID of the employee for whom payroll is being generated.
        - start_date: The start date of the pay period.
        - end_date: The end date of the pay period.
        - basic_salary: The basic salary of the employee.
        - overtime_pay: The overtime pay of the employee.
        - deductions: The deductions applicable to the employee.
        """
        pass

    def get_payroll_by_id(self, payroll_id):
        """
        Retrieves payroll details by payroll ID.

        Parameters:
        - payroll_id: The ID of the payroll to retrieve.
        """
        pass

    def get_payrolls_for_employee(self, employee_id):
        """
        Retrieves all payroll records for a specific employee.

        Parameters:
        - employee_id: The ID of the employee for whom to retrieve payroll records.
        """
        pass

    def get_payrolls_for_period(self, start_date, end_date):
        """
        Retrieves all payroll records within a specific pay period.

        Parameters:
        - start_date: The start date of the pay period.
        - end_date: The end date of the pay period.
        """
        pass

    def calculate_gross_salary(self, base_salary):
        """
        Method to calculate the gross salary of an employee.
        :param base_salary: The base salary of the employee
        :return: The gross salary after applying necessary components like bonuses or allowances.
        """
        pass