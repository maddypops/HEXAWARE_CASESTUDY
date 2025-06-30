class Employee:
    def __init__(self, first_name, last_name, dob, gender, email, phone, address, position, salary, joining_date, termination_date=None, employee_id=None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.position = position
        self.salary = salary
        self.joining_date = joining_date
        self.termination_date = termination_date

    def calculate_age(self):
        from datetime import date
        birth_date = self.dob
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def display_employee_info(self):
        return {
            'Employee ID': self.employee_id,
            'Name': f"{self.first_name} {self.last_name}",
            'Age': self.calculate_age(),
            'Gender': self.gender,
            'Position': self.position,
            'Salary': self.salary,
            'Joining Date': self.joining_date,
            'Termination Date': self.termination_date if self.termination_date else 'N/A'
        }

    def __str__(self):
        return (f"EmployeeID: {self.employee_id}, FirstName: {self.first_name}, LastName: {self.last_name}, "
                f"DateOfBirth: {self.dob}, Gender: {self.gender}, Email: {self.email}, Phone: {self.phone}, "
                f"Address: {self.address}, Position: {self.position}, Salary: {self.salary}, "
                f"JoiningDate: {self.joining_date}, TerminationDate: {self.termination_date}")
