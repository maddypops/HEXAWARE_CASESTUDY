import unittest
from Payxpert.dao.PayrollServiceImpl import PayrollServiceImpl, calculate_gross_salary
from Payxpert.entity.Employee import Employee
from datetime import date


class TestCalculateGrossSalary(unittest.TestCase):

    def setUp(self):
        self.employee = Employee(
            first_name='John',
            last_name='Doe',
            dob=date(1990, 1, 1),  # Providing required dob
            gender='Male',
            email='john.doe@example.com',
            phone='1234567890',
            address='123 Main St',
            position='Developer',
            salary=5000.00,  # Basic salary
            joining_date=date(2020, 1, 1)
        )
        self.payroll_service = PayrollServiceImpl(None)  # Mocking database connection

    def test_calculate_gross_salary(self):
        # Calculate gross salary using the PayrollServiceImpl
        gross_salary = calculate_gross_salary(self.employee.salary)

        # Print the calculated gross salary
        print(f"Calculated Gross Salary: {gross_salary}")

        # Assuming an expected gross salary
        expected_gross_salary = 5000.00  # Modify based on your application's logic
        self.assertEqual(gross_salary, expected_gross_salary)


if __name__ == '__main__':
    unittest.main()
