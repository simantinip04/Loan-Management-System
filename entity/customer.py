class Customer:
    def __init__(self, customer_id=0, name="", email="", phone_number="", address="", credit_score=0):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.credit_score = credit_score

    def __str__(self):
        return (f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone_number}, Address: {self.address}, Credit Score: {self.credit_score}")