import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dao.loan_repository_impl import LoanRepositoryImpl
from entity.home_loan import HomeLoan
from entity.car_loan import CarLoan
from entity.customer import Customer
from dao.customer_dao_impl import CustomerDAOImpl
from dao.loan_dao_impl import LoanDAOImpl

def main():
    repo = LoanRepositoryImpl()

    while True:
        print("\n--- Loan Management System ---")
        print("1. Apply for Loan")
        print("2. Calculate Interest by Loan ID")
        print("3. Calculate EMI by Loan ID")
        print("4. Check Loan Status")
        print("5. Repay Loan")
        print("6. View Loan by ID")
        print("7. View All Loans")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cust_id = input("Enter Customer ID: ")
            cust_name = input("Enter Customer Name: ")
            credit_score = int(input("Enter Credit Score: "))

            cust = Customer(cust_id, cust_name, credit_score)
            cust_dao = CustomerDAOImpl()
            if not cust_dao.customer_exists(cust_id):
                cust_dao.add_customer(cust)
            else:
                    print(f"ℹ️ Customer with ID {cust_id} already exists. Skipping insertion.")

            loan_id = input("Enter Loan ID: ")
            principal = float(input("Enter Principal Amount: "))
            interest = float(input("Enter Interest Rate (%): "))
            term = int(input("Enter Loan Term (months): "))
            loan_type = input("Enter Loan Type (Home/Car): ").strip().lower()

            loan_repo = LoanDAOImpl()

            if loan_type == "home":
                address = input("Enter Property Address: ")
                value = float(input("Enter Property Value: "))
                loan = HomeLoan(loan_id, cust, principal, interest, term, "Pending", address, value)
                loan_repo.apply_loan(loan)

            elif loan_type == "car":
                model = input("Enter Car Model: ")
                car_price = float(input("Enter Car Price: "))
                loan = CarLoan(loan_id, cust, principal, interest, term, model, car_price)
                loan_repo.apply_loan(loan)

            else:
                print("❌ Invalid loan type. Please enter either Home or Car.")

        elif choice == "2":
            loan_id = input("Enter Loan ID: ")
            repo.calculate_interest(loan_id)

        elif choice == "3":
            loan_id = input("Enter Loan ID: ")
            repo.calculate_emi(loan_id)

        elif choice == "4":
            loan_id = input("Enter Loan ID: ")
            repo.loan_status(loan_id)

        elif choice == "5":
            loan_id = input("Enter Loan ID: ")
            amount = float(input("Enter repayment amount: "))
            repo.loan_repayment(loan_id, amount)

        elif choice == "6":
            loan_id = input("Enter Loan ID: ")
            repo.get_loan_by_id(loan_id)

        elif choice == "7":
            repo.get_all_loans()

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
