class InvalidLoanException(Exception):
    def __init__(self, message="Loan not found or invalid loan ID provided."):
        super().__init__(message)