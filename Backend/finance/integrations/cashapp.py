import requests
import json
from datetime import datetime
import hmac
import hashlib
import base64
import time
import uuid
import os
import logging
from pathlib import Path

# Set up logging configuration
log_dir = Path("log")
log_dir.mkdir(exist_ok=True)  # Create log directory if it doesn't exist
log_file = log_dir / "cashapp_scrapper.log"

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("CashAppScraper")


class CashAppClient:
    def __init__(self, client_id, client_secret, api_key, sandbox=True):
        """
        Initialize the Cash App API client

        Args:
            client_id (str): Your Cash App client ID
            client_secret (str): Your Cash App client secret
            api_key (str): Your Cash App API key
            sandbox (bool): Whether to use sandbox environment (default: True)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key

        if sandbox:
            self.base_url = "https://sandbox.api.cash.app/v1"
        else:
            self.base_url = "https://api.cash.app/v1"

        self.access_token = None
        self.token_expiry = 0

        logger.info(f"CashAppClient initialized. Sandbox mode: {sandbox}")

    def _generate_signature(self, endpoint, method, payload=None):
        """Generate HMAC signature for API requests"""
        timestamp = str(int(time.time()))
        nonce = str(uuid.uuid4())

        string_to_sign = f"{timestamp}.{nonce}.{method}.{endpoint}"
        if payload:
            string_to_sign += f".{json.dumps(payload)}"

        signature = hmac.new(
            self.client_secret.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).digest()

        logger.debug(f"Generated signature for {method} {endpoint}")

        return {
            "X-Cash-App-Timestamp": timestamp,
            "X-Cash-App-Nonce": nonce,
            "X-Cash-App-Signature": base64.b64encode(signature).decode()
        }

    def _refresh_token_if_needed(self):
        """Check if access token is expired and refresh if needed"""
        current_time = time.time()

        if not self.access_token or current_time >= self.token_expiry:
            logger.info("Access token expired or not present. Refreshing token.")
            self._get_access_token()

    def _get_access_token(self):
        """Get a new access token from Cash App API"""
        endpoint = "/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "payments.read payments.write"
        }

        logger.info("Requesting new access token")

        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                data=data
            )

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.token_expiry = time.time() + token_data["expires_in"] - 60  # Buffer of 60 seconds
                logger.info("Successfully obtained new access token")
            else:
                error_msg = f"Failed to obtain access token: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Exception while getting access token: {str(e)}")
            raise

    def _make_request(self, method, endpoint, params=None, data=None):
        """Make an authenticated request to Cash App API"""
        self._refresh_token_if_needed()

        url = f"{self.base_url}{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cash-App-API-Key": self.api_key
        }

        # Add signature headers
        signature_headers = self._generate_signature(endpoint, method, data)
        headers.update(signature_headers)

        logger.info(f"Making {method} request to {endpoint}")
        if params:
            logger.debug(f"Request params: {params}")
        if data:
            logger.debug(f"Request data: {data}")

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                error_msg = f"Unsupported HTTP method: {method}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            if response.status_code in (200, 201, 202):
                result = response.json() if response.text else {}
                logger.info(f"Request successful. Status code: {response.status_code}")
                logger.debug(f"Response data: {result}")

                # Log to the file for specific endpoints that contain transaction data
                if endpoint.startswith("/transactions") or endpoint.startswith("/payments"):
                    with open(log_file, "a") as f:
                        f.write(f"\n--- {datetime.now().isoformat()} - {method} {endpoint} ---\n")
                        f.write(json.dumps(result, indent=2))
                        f.write("\n")

                return result
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Exception during API request: {str(e)}")
            raise

    def get_balance(self):
        """Get current account balance"""
        logger.info("Getting account balance")
        result = self._make_request("GET", "/accounts/balance")
        logger.info(f"Balance retrieved: {result['available_amount']} {result['currency']}")
        return result

    def get_transaction_history(self, start_date=None, end_date=None, limit=50):
        """
        Get transaction history

        Args:
            start_date (str): ISO format date (YYYY-MM-DD)
            end_date (str): ISO format date (YYYY-MM-DD)
            limit (int): Maximum number of transactions to return
        """
        params = {"limit": limit}

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        date_range = f"from {start_date if start_date else 'beginning'} to {end_date if end_date else 'now'}"
        logger.info(f"Getting transaction history {date_range} (limit: {limit})")

        result = self._make_request("GET", "/transactions", params=params)

        # Log transaction data to the specific log file
        transactions = result.get('data', [])
        logger.info(f"Retrieved {len(transactions)} transactions")

        # Additional detailed logging to the cashapp_scrapper.log file
        with open(log_file, "a") as f:
            f.write(f"\n=== TRANSACTION HISTORY ({datetime.now().isoformat()}) ===\n")
            f.write(f"Date Range: {date_range}\n")
            f.write(f"Total Transactions: {len(transactions)}\n\n")

            for idx, tx in enumerate(transactions, 1):
                f.write(f"Transaction #{idx}:\n")
                f.write(json.dumps(tx, indent=2))
                f.write("\n\n")

        return result

    def send_payment(self, recipient, amount, currency="USD", note=None):
        """
        Send payment to a recipient

        Args:
            recipient (str): Recipient's $cashtag, email, or phone
            amount (float): Amount to send
            currency (str): Currency code (default: USD)
            note (str): Optional payment note
        """
        data = {
            "recipient": recipient,
            "amount": float(amount),
            "currency": currency
        }

        if note:
            data["note"] = note

        logger.info(f"Sending payment of {amount} {currency} to {recipient}")
        result = self._make_request("POST", "/payments", data=data)

        # Log payment details
        logger.info(f"Payment sent successfully. Payment ID: {result.get('id')}")

        # Additional detailed logging
        with open(log_file, "a") as f:
            f.write(f"\n=== PAYMENT SENT ({datetime.now().isoformat()}) ===\n")
            f.write(f"To: {recipient}\n")
            f.write(f"Amount: {amount} {currency}\n")
            if note:
                f.write(f"Note: {note}\n")
            f.write(f"Payment ID: {result.get('id')}\n")
            f.write(f"Status: {result.get('status')}\n")
            f.write("\n")

        return result

    def get_payment_status(self, payment_id):
        """
        Check status of a payment

        Args:
            payment_id (str): ID of the payment to check
        """
        logger.info(f"Checking status for payment ID: {payment_id}")
        result = self._make_request("GET", f"/payments/{payment_id}")

        # Log payment status
        logger.info(f"Payment status retrieved: {result.get('status')}")

        return result

    def request_payment(self, from_user, amount, currency="USD", note=None, expiration_days=14):
        """
        Request payment from a user

        Args:
            from_user (str): User's $cashtag, email, or phone
            amount (float): Amount to request
            currency (str): Currency code (default: USD)
            note (str): Optional request note
            expiration_days (int): Days until request expires
        """
        data = {
            "from_user": from_user,
            "amount": float(amount),
            "currency": currency,
            "expiration_days": expiration_days
        }

        if note:
            data["note"] = note

        logger.info(f"Requesting payment of {amount} {currency} from {from_user}")
        result = self._make_request("POST", "/payment_requests", data=data)

        # Log payment request details
        logger.info(f"Payment request sent. Request ID: {result.get('id')}")

        # Additional detailed logging
        with open(log_file, "a") as f:
            f.write(f"\n=== PAYMENT REQUESTED ({datetime.now().isoformat()}) ===\n")
            f.write(f"From: {from_user}\n")
            f.write(f"Amount: {amount} {currency}\n")
            if note:
                f.write(f"Note: {note}\n")
            f.write(f"Request ID: {result.get('id')}\n")
            f.write(f"Expires: {result.get('expiration_date')}\n")
            f.write("\n")

        return result

    def get_customer_profile(self, customer_id):
        """
        Get customer profile information

        Args:
            customer_id (str): ID of the customer
        """
        logger.info(f"Getting profile for customer ID: {customer_id}")
        return self._make_request("GET", f"/customers/{customer_id}")


# Example usage
if __name__ == "__main__":
    logger.info("Starting Cash App integration script")

    # Replace with your actual API credentials
    client = CashAppClient(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        api_key="YOUR_API_KEY",
        sandbox=True  # Use sandbox environment for testing
    )

    # Example: Get account balance
    try:
        balance = client.get_balance()
        print(f"Current balance: ${balance['available_amount']} {balance['currency']}")
        logger.info(f"Current balance: ${balance['available_amount']} {balance['currency']}")
    except Exception as e:
        error_msg = f"Error getting balance: {e}"
        print(error_msg)
        logger.error(error_msg)

    # Example: Send payment
    try:
        payment = client.send_payment(
            recipient="$johndoe",
            amount=10.00,
            note="Thanks for lunch!"
        )
        print(f"Payment sent! ID: {payment['id']}")
    except Exception as e:
        error_msg = f"Error sending payment: {e}"
        print(error_msg)
        logger.error(error_msg)

    # Example: Get transaction history for the last month
    try:
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        transactions = client.get_transaction_history(
            start_date=start_date,
            end_date=end_date,
            limit=10
        )

        print(f"Found {len(transactions['data'])} transactions:")
        for tx in transactions['data']:
            print(f"- {tx['created_at']}: ${tx['amount']} ({tx['description']})")
    except Exception as e:
        error_msg = f"Error getting transactions: {e}"
        print(error_msg)
        logger.error(error_msg)

    logger.info("Cash App integration script completed")