CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    credit_score INT
);

CREATE TABLE Loan (
    loan_id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES Customer(customer_id),
    principal_amount FLOAT,
    interest_rate FLOAT,
    loan_term INT,
    loan_type VARCHAR(20),  
    loan_status VARCHAR(20) 
);

CREATE TABLE HomeLoan (
    loan_id INT PRIMARY KEY FOREIGN KEY REFERENCES Loan(loan_id),
    property_address VARCHAR(255),
    property_value INT
);

CREATE TABLE CarLoan (
    loan_id INT PRIMARY KEY FOREIGN KEY REFERENCES Loan(loan_id),
    car_model VARCHAR(100),
    car_price DECIMAL(15, 2)
);