import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ZelleService:
    """
    A service class for interacting with the Zelle API.

    This class provides methods for sending payments, retrieving payment details,
    requesting money, and updating credentials. Credentials are initially loaded
    from environment variables but can be updated via a class method.
    """

    def __init__(self):
        """
        Initializes the ZelleService with credentials from environment variables.
        """
        self.zelle_email = os.getenv("ZELLE_EMAIL")
        self.zelle_password = os.getenv("ZELLE_PASSWORD")
        self.zelle_phone_number = os.getenv("ZELLE_PHONE_NUMBER")
        self.zelle_note = os.getenv("ZELLE_NOTE")
        self.zelle_receiver = os.getenv("ZELLE_RECEIVER")
        self.zelle_amount = os.getenv("ZELLE_AMOUNT")
        # Base URL for the Zelle API
        self.base_url = "https://api.zellepay.com"
        # Default headers for all requests
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def update_credentials(self, email=None, password=None, phone_number=None, note=None, receiver=None, amount=None):
        """
        Updates the Zelle credentials for the service.

        Parameters:
            email (str): New email to use.
            password (str): New password.
            phone_number (str): New phone number.
            note (str): New payment note.
            receiver (str): New receiver information.
            amount (str or float): New amount.
        """
        if email:
            self.zelle_email = email
        if password:
            self.zelle_password = password
        if phone_number:
            self.zelle_phone_number = phone_number
        if note:
            self.zelle_note = note
        if receiver:
            self.zelle_receiver = receiver
        if amount:
            self.zelle_amount = amount

    def send_payment(self):
        """
        Sends a payment using the Zelle API based on the stored credentials.

        Returns:
            dict: API response if successful.

        Raises:
            Exception: If the API call fails.
        """
        payload = {
            "email": self.zelle_email,
            "password": self.zelle_password,
            "phone_number": self.zelle_phone_number,
            "amount": self.zelle_amount,
            "note": self.zelle_note,
            "receiver": self.zelle_receiver,
        }
        url = f"{self.base_url}/payment"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Payment sent successfully!")
            result = response.json()
            print("Response:", result)
            return result
        else:
            error = response.json()
            print("Error sending payment:", error)
            raise Exception(f"Payment error: {error}")

    def get_payment_details(self, transaction_id):
        """
        Retrieves detailed information about a specific payment.

        Parameters:
            transaction_id (str): The ID of the transaction.

        Returns:
            dict: Detailed information about the payment.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{self.base_url}/payment/{transaction_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            details = response.json()
            print("Payment Details:")
            for key, value in details.items():
                print(f"{key}: {value}")
            return details
        else:
            error = response.json()
            print("Error retrieving payment details:", error)
            raise Exception(f"Payment details error: {error}")

    def request_money(self):
        """
        Requests money using the Zelle API. This method assumes that there is
        a separate endpoint for requesting money.

        Returns:
            dict: API response if successful.

        Raises:
            Exception: If the API call fails.
        """
        payload = {
            "email": self.zelle_email,
            "password": self.zelle_password,
            "phone_number": self.zelle_phone_number,
            "amount": self.zelle_amount,
            "note": self.zelle_note,
            "receiver": self.zelle_receiver,
        }
        url = f"{self.base_url}/request"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Money request sent successfully!")
            result = response.json()
            print("Response:", result)
            return result
        else:
            error = response.json()
            print("Error requesting money:", error)
            raise Exception(f"Money request error: {error}")

    def simulate_login(self):
        """
        Simulates a login process for Zelle by checking if credentials are set.
        Actual authentication is handled in the send_payment/request_money methods.

        Returns:
            bool: True if credentials are present, otherwise raises an Exception.
        """
        if self.zelle_email and self.zelle_password:
            print("Credentials are set. Ready to proceed.")
            return True
        else:
            raise Exception("Missing Zelle credentials. Please update the credentials using update_credentials().")

    def logout(self):
        """
        Simulates logging out by clearing stored credentials.
        """
        self.zelle_email = None
        self.zelle_password = None
        self.zelle_phone_number = None
        self.zelle_note = None
        self.zelle_receiver = None
        self.zelle_amount = None
        print("Logged out successfully. Credentials cleared.")
