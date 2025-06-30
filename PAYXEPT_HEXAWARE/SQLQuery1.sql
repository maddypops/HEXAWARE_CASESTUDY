-- Create the database if not exists

CREATE DATABASE EmployeeManagementDB;

USE EmployeeManagementDB;

-- Employee Table
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    DateOfBirth DATE,
    Gender NVARCHAR(10),
    Email NVARCHAR(100),
    PhoneNumber NVARCHAR(15),
    Address NVARCHAR(255),
    Position NVARCHAR(100),
    Salary DECIMAL(10, 2),  -- Added Salary column
    JoiningDate DATE,
    TerminationDate DATE NULL
);


DROP TABLE Employee;
DROP TABLE Payroll;
DROP TABLE Tax;
DROP TABLE FinancialRecord;




CREATE TABLE Payroll (
    PayrollID INT PRIMARY KEY IDENTITY(1,1),
    EmployeeID INT FOREIGN KEY REFERENCES Employee(EmployeeID),
    PayPeriodStartDate DATE,
    PayPeriodEndDate DATE,
    BasicSalary DECIMAL(10, 2),
    OvertimePay DECIMAL(10, 2),
    Deductions DECIMAL(10, 2),
    NetSalary DECIMAL(10, 2)
);

CREATE TABLE Tax (
    TaxID INT PRIMARY KEY IDENTITY(1,1),
    EmployeeID INT FOREIGN KEY REFERENCES Employee(EmployeeID),
    TaxYear INT,
    TaxableIncome DECIMAL(10, 2),
    TaxAmount DECIMAL(10, 2)
);

CREATE TABLE FinancialRecord (
    RecordID INT PRIMARY KEY IDENTITY(1,1),
    EmployeeID INT FOREIGN KEY REFERENCES Employee(EmployeeID),
    RecordDate DATE,
    Description NVARCHAR(255),
    Amount DECIMAL(10, 2),
    RecordType NVARCHAR(50)
);

SELECT * FROM Employee;
SELECT * FROM Payroll;
SELECT * FROM Tax;
SELECT * FROM FinancialRecord;