import getpass
import logging
from venmo_api import Client

# Configure logging to output messages with time stamps.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class VenmoService:
    """
    A service class that wraps common Venmo API operations including login,
    sending money, requesting money, checking balance, viewing transaction history,
    retrieving payment details, viewing/updating profile, and logging out.
    """

    def __init__(self):
        """
        Initializes the VenmoService without a logged-in client.
        """
        self.client = None

    def login(self):
        """
        Prompts the user for Venmo credentials and logs in to create an authenticated client.

        Uses the getpass module to securely prompt for the password and validates that the email
        contains an '@'. It retrieves an access token using the Venmo API and initializes the client.

        Raises:
            Exception: If login fails or if invalid credentials are provided.
        """
        print("Login using your Venmo account to get an access token for the API.")
        email = input("Venmo Email: ").strip()
        if '@' not in email:
            raise ValueError("Invalid email provided. Please enter a valid email address.")
        password = getpass.getpass("Venmo Password: ")

        try:
            token = Client.get_access_token(username=email, password=password)
            self.client = Client(access_token=token)
            logging.info("Successfully logged in!")
        except Exception as e:
            logging.error("Login failed: %s", e)
            raise Exception("Login failed: " + str(e))

    def send_money(self):
        """
        Prompts for recipient details, amount, and a note, then sends money using the Venmo API.

        If an email is provided as the recipient, it searches for the corresponding user.
        If multiple users are found, the first match is used.

        Raises:
            Exception: If the payment fails or if any input is invalid.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        receiver = input("Enter receiver's Venmo email or user id: ").strip()
        if '@' in receiver:
            try:
                results = self.client.user.search(receiver)
                if not results:
                    print("No user found with that email.")
                    return
                elif len(results) > 1:
                    print("Multiple users found. Using the first match.")
                receiver_id = results[0].id
            except Exception as e:
                logging.error("Error searching for user: %s", e)
                return
        else:
            receiver_id = receiver

        try:
            amount_input = input("Enter amount to send (e.g., 10.50): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
        except ValueError:
            print("Invalid amount entered.")
            return

        note = input("Enter a note for the payment: ").strip()

        try:
            response = self.client.payment.send_money(receiver_id, amount, note, audience='private')
            logging.info("Payment sent successfully!")
            print("Payment sent successfully!")
            print("Response:", response)
        except Exception as e:
            logging.error("Error sending payment: %s", e)
            print("Error sending payment:", e)

    def request_money(self):
        """
        Prompts for recipient details, amount, and a note, then requests money using the Venmo API.

        Similar to send_money, but this method requests money instead of sending it.

        Raises:
            Exception: If the money request fails or if any input is invalid.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        requester = input("Enter requester's Venmo email or user id: ").strip()
        if '@' in requester:
            try:
                results = self.client.user.search(requester)
                if not results:
                    print("No user found with that email.")
                    return
                elif len(results) > 1:
                    print("Multiple users found. Using the first match.")
                requester_id = results[0].id
            except Exception as e:
                logging.error("Error searching for user: %s", e)
                return
        else:
            requester_id = requester

        try:
            amount_input = input("Enter amount to request (e.g., 10.50): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
        except ValueError:
            print("Invalid amount entered.")
            return

        note = input("Enter a note for the request: ").strip()

        try:
            # Assuming the API provides a method for requesting money.
            response = self.client.payment.request_money(requester_id, amount, note, audience='private')
            logging.info("Money request sent successfully!")
            print("Money request sent successfully!")
            print("Response:", response)
        except Exception as e:
            logging.error("Error requesting money: %s", e)
            print("Error requesting money:", e)

    def view_balance(self):
        """
        Retrieves and displays the user's Venmo balance.

        Raises:
            Exception: If unable to retrieve the balance.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        try:
            balance = self.client.user.get_balance()
            print("Your current balance is: ${:.2f}".format(balance))
        except Exception as e:
            logging.error("Error retrieving balance: %s", e)
            print("Error retrieving balance:", e)

    def view_transaction_history(self):
        """
        Retrieves and displays a simplified transaction history.

        Prints a list of recent transactions including transaction ID, amount, note, and date.

        Raises:
            Exception: If unable to retrieve the transaction history.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        try:
            transactions = self.client.user.get_transactions()
            if not transactions:
                print("No transactions found.")
                return

            print("Recent Transactions:")
            for tx in transactions:
                print("ID: {}, Amount: ${:.2f}, Note: {}, Date: {}".format(
                    tx.id, tx.amount, tx.note, tx.date))
        except Exception as e:
            logging.error("Error retrieving transaction history: %s", e)
            print("Error retrieving transaction history:", e)

    def get_payment_details(self):
        """
        Retrieves detailed information for a specific payment by transaction ID.

        Prompts the user to input a transaction ID and then fetches details using the API.

        Raises:
            Exception: If the transaction details cannot be retrieved.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        transaction_id = input("Enter the transaction ID: ").strip()
        try:
            payment_details = self.client.payment.get_details(transaction_id)
            print("Payment Details:")
            for key, value in payment_details.items():
                print(f"{key}: {value}")
        except Exception as e:
            logging.error("Error retrieving payment details: %s", e)
            print("Error retrieving payment details:", e)

    def view_profile(self):
        """
        Retrieves and displays the user's profile information.

        Displays information such as user id, username, and other available details.

        Raises:
            Exception: If unable to retrieve profile information.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        try:
            profile = self.client.user.get_profile()
            print("Your Profile Information:")
            for key, value in profile.items():
                print(f"{key}: {value}")
        except Exception as e:
            logging.error("Error retrieving profile: %s", e)
            print("Error retrieving profile:", e)

    def update_profile(self):
        """
        Updates the user's profile information.

        Prompts the user for new profile details (for example, a new display name)
        and updates the profile via the API. This is a placeholder function and assumes
        the API supports such an update.

        Raises:
            Exception: If the profile update fails.
        """
        if not self.client:
            raise Exception("Not authenticated. Please log in first.")

        # Example: updating the display name.
        new_display_name = input("Enter your new display name: ").strip()
        try:
            # Assuming the API has a method to update profile info.
            response = self.client.user.update_profile(display_name=new_display_name)
            logging.info("Profile updated successfully!")
            print("Profile updated successfully!")
            print("Response:", response)
        except Exception as e:
            logging.error("Error updating profile: %s", e)
            print("Error updating profile:", e)

    def logout(self):
        """
        Logs out by deleting the client instance.

        Note:
            The Venmo API does not have an explicit logout endpoint.
            Deleting the client instance simulates logging out.
        """
        if self.client:
            print("Logging out...")
            del self.client
            self.client = None
            logging.info("Logged out successfully.")
            print("Logged out successfully.")
        else:
            print("No active session to log out from.")
