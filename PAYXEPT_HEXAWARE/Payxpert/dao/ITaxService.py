from abc import ABC, abstractmethod


class ITaxService(ABC):

    @abstractmethod
    def calculate_tax(self, employee_id, tax_year):
        pass

    @abstractmethod
    def get_tax_by_id(self, tax_id):
        pass

    @abstractmethod
    def get_taxes_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_taxes_for_year(self, tax_year):
        pass
