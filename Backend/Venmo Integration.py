import getpass
from venmo_api import Client


def login():
    """
    Prompts the user for Venmo credentials and returns an access token.
    """
    print("Login using your Venmo account to get an access token for the API.")
    email = input("Venmo Email: ").strip()
    if '@' not in email:
        print("Invalid email provided.")
        raise SystemExit
    # Use getpass so the password isn't echoed to the screen.
    password = getpass.getpass("Venmo Password: ")

    try:
        # This will return an access token if the credentials are valid.
        token = Client.get_access_token(username=email, password=password)
        print("Successfully logged in!")
    except Exception as e:
        print("Login failed:", e)
        raise SystemExit

    return token


def send_money(client):
    """
    Prompts for recipient, amount, and a note, then sends money using the Venmo API.
    """
    # Ask for recipient info. If an email is provided, attempt to search for the user.
    receiver = input("Enter receiver's Venmo email or user id: ").strip()

    if '@' in receiver:
        try:
            results = client.user.search(receiver)
            if not results:
                print("No user found with that email.")
                return
            elif len(results) > 1:
                print("Multiple users found. Using the first match.")
            receiver_id = results[0].id
        except Exception as e:
            print("Error searching for user:", e)
            return
    else:
        # Assume the user entered a valid Venmo user id.
        receiver_id = receiver

    try:
        amount = float(input("Enter amount to send: ").strip())
    except ValueError:
        print("Invalid amount entered.")
        return

    note = input("Enter a note for the payment: ").strip()

    try:
        # The payment method used here is 'send_money'.
        # 'audience' can be set to 'private' (default) or 'friends' depending on your needs.
        response = client.payment.send_money(receiver_id, amount, note, audience='private')
        print("Payment sent successfully!")
        print("Response:", response)
    except Exception as e:
        print("Error sending payment:", e)


def logout(client):
    """
    Logs out by deleting the client instance.
    (There is no explicit logout endpoint in the Venmo API.)
    """
    print("Logging out...")
    del client
    print("Logged out successfully.")


def main():
    # Login and get the access token.
    token = login()

    # Create a Venmo API client using the access token.
    client = Client(access_token=token)

    while True:
        print("\nOptions:")
        print("1. Send money")
        print("2. Logout and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            send_money(client)
        elif choice == "2":
            logout(client)
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()
