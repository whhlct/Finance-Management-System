import sys
import logging
import argparse
from getpass import getpass
from time import sleep
from functools import wraps
from typing import Optional, Dict, Any, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
# Define log file location and formatting for console and file outputs
LOG_FILE = 'logs/venmo_scraper.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FILE)]
)
logger = logging.getLogger('VenmoScraper')  # Logger for all scraper operations

# ------------------------------------------------------------------------------
# Retry Decorator
# ------------------------------------------------------------------------------
def retry(attempts=3, delay=2):
    """
    Decorator to retry a function up to 'attempts' times with a sleep of 'delay' seconds between tries.
    Useful for flaky web operations that may fail intermittently.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    # Log a warning and retry after delay
                    logger.warning(f"{fn.__name__} failed on attempt {i+1}/{attempts}: {e}")
                    sleep(delay)
            # If all attempts fail, propagate the last exception
            raise last_exc
        return wrapper
    return decorator

# ------------------------------------------------------------------------------
# Page Object Base Class
# ------------------------------------------------------------------------------
class BasePage:
    """
    Base class for all page objects. Implements common Selenium operations with explicit waits.
    """
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by, locator):
        """Wait until a single element is present and return it."""
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def finds(self, by, locator):
        """Wait until multiple elements are present and return them."""
        return self.wait.until(EC.presence_of_all_elements_located((by, locator)))

    def click(self, by, locator):
        """Find an element and click it."""
        el = self.find(by, locator)
        el.click()

    def send_keys(self, by, locator, keys):
        """Find an input, clear it, and send keys."""
        el = self.find(by, locator)
        el.clear()
        el.send_keys(keys)

    def text(self, by, locator):
        """Return the text content of an element."""
        return self.find(by, locator).text

    def attr(self, by, locator, name):
        """Return the value of an attribute for an element."""
        return self.find(by, locator).get_attribute(name)

# ------------------------------------------------------------------------------
# Specific Page Objects
# ------------------------------------------------------------------------------
class LoginPage(BasePage):
    """Page object for Venmo login."""
    URL = 'https://account.venmo.com/sign-in/'

    @retry()
    def login(self, email: str, password: str):
        """
        Perform login: navigate to login URL, enter credentials, and submit.
        Wait for balance button to confirm success.
        """
        logger.info('Opening login page')
        self.driver.get(self.URL)
        self.send_keys(By.NAME, 'email', email)
        self.send_keys(By.NAME, 'password', password)
        self.click(By.XPATH, "//button[contains(text(),'Log In')]")
        # Wait for balance button as a success indicator
        self.find(By.CSS_SELECTOR, "[data-testid='balance-button']")
        logger.info('Login successful')

class BalancePage(BasePage):
    """Page object for retrieving account balance."""
    URL = 'https://venmo.com/account/transfers/'

    @retry()
    def get_balance(self) -> float:
        """Open the balance page and parse the displayed balance."""
        logger.info('Retrieving balance')
        self.driver.get(self.URL)
        text = self.text(By.CSS_SELECTOR, "[data-testid='balance-button']")
        # Convert string like '$1,234.56' to float
        return float(text.replace('$','').replace(',',''))

class HistoryPage(BasePage):
    """Page object for retrieving transaction history."""
    URL = 'https://venmo.com/account/transaction-history/'

    @retry()
    def get_transactions(self, limit=20) -> List[Dict[str, str]]:
        """Fetch recent transactions up to 'limit', returning list of dicts."""
        logger.info('Retrieving transactions')
        self.driver.get(self.URL)
        rows = self.finds(By.CSS_SELECTOR, '.transaction-history-list .transaction')
        txs = []
        for row in rows[:limit]:
            txs.append({
                'id': row.get_attribute('data-transaction-id'),
                'amount': row.find_element(By.CSS_SELECTOR,'.amount').text,
                'note': row.find_element(By.CSS_SELECTOR,'.note').text,
                'date': row.find_element(By.CSS_SELECTOR,'.datetime').get_attribute('datetime')
            })
        return txs

class ProfilePage(BasePage):
    """Page object for viewing and updating user profile settings."""
    URL = 'https://venmo.com/account/settings/profile/'

    @retry()
    def view(self) -> Dict[str, str]:
        """Return current profile fields as a dict."""
        logger.info('Viewing profile')
        self.driver.get(self.URL)
        fields = ['display_name','username','about']
        return {f: self.attr(By.NAME, f, 'value') for f in fields}

    @retry()
    def update(self, **fields) -> Dict[str, str]:
        """Update editable profile fields (display_name, about) and return the new settings."""
        logger.info('Updating profile')
        self.driver.get(self.URL)
        for key, val in fields.items():
            if key in ('display_name', 'about'):
                self.send_keys(By.NAME, key, val)
        self.click(By.XPATH, "//button[contains(text(),'Save')]")
        sleep(1)  # wait briefly for changes to persist
        return self.view()

class PaymentPage(BasePage):
    """Page object for sending and requesting payments."""
    URL = 'https://venmo.com/account/payment/'

    @retry()
    def send(self, user: str, amount: float, note: str):
        """Send a payment to a user with optional note."""
        logger.info(f'Sending ${amount} to {user}')
        self.driver.get(self.URL)
        # Select user
        self.send_keys(By.CSS_SELECTOR, 'input[placeholder="Search people"]', user)
        sleep(1)  # allow search suggestions to load
        self.click(By.CSS_SELECTOR, '.suggested-users li')
        # Enter amount and note
        self.send_keys(By.CSS_SELECTOR, 'input[placeholder="$0.00"]', str(amount))
        self.send_keys(By.CSS_SELECTOR, 'textarea[placeholder="Add a note"]', note)
        self.click(By.XPATH, "//button[contains(text(),'Pay')]")
        # Confirm success
        self.find(By.XPATH, "//div[contains(text(),'Payment sent')]")

    @retry()
    def request(self, user: str, amount: float, note: str):
        """Request a payment from a user with optional note."""
        logger.info(f'Requesting ${amount} from {user}')
        self.driver.get(self.URL)
        self.click(By.XPATH, "//button[contains(text(),'Request')]")
        self.send_keys(By.CSS_SELECTOR, 'input[placeholder="Search people"]', user)
        sleep(1)
        self.click(By.CSS_SELECTOR, '.suggested-users li')
        self.send_keys(By.CSS_SELECTOR, 'input[placeholder="$0.00"]', str(amount))
        self.send_keys(By.CSS_SELECTOR, 'textarea[placeholder="Add a note"]', note)
        self.click(By.XPATH, "//button[contains(text(),'Request')]")
        self.find(By.XPATH, "//div[contains(text(),'Request sent')]")

# ------------------------------------------------------------------------------
# Service Orchestrator
# ------------------------------------------------------------------------------
class VenmoService:
    """
    High-level service that ties together page objects and provides CLI-friendly methods.
    """
    def __init__(self, headless=True):
        # Configure Chrome driver options
        opts = Options()
        if headless:
            opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=opts)
        # Instantiate page objects
        self.login_page = LoginPage(self.driver)
        self.balance_page = BalancePage(self.driver)
        self.history_page = HistoryPage(self.driver)
        self.profile_page = ProfilePage(self.driver)
        self.payment_page = PaymentPage(self.driver)
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    def prompt_credentials(self):
        """Prompt user for email/password only if not already provided."""
        if not self.email:
            self.email = input('Venmo Email: ').strip()
        if not self.password:
            self.password = getpass('Venmo Password: ')

    def login(self):
        """Login flow: prompt for credentials, then perform login."""
        self.prompt_credentials()
        self.login_page.login(self.email, self.password)

    def logout(self):
        """Close browser to logout."""
        logger.info('Logging out (closing browser)')
        try:
            self.driver.quit()
        except Exception:
            pass

    def view_balance(self) -> float:
        """Return account balance."""
        return self.balance_page.get_balance()

    def view_transactions(self, limit=10) -> List[Dict[str, str]]:
        """Return recent transaction history."""
        return self.history_page.get_transactions(limit)

    def view_profile(self) -> Dict[str, str]:
        """Return current profile settings."""
        return self.profile_page.view()

    def update_profile(self, **fields) -> Dict[str, str]:
        """Update profile fields and return updated settings."""
        return self.profile_page.update(**fields)

    def send_money(self, user: str, amount: float, note: str):
        """Send money to user."""
        self.payment_page.send(user, amount, note)

    def request_money(self, user: str, amount: float, note: str):
        """Request money from user."""
        self.payment_page.request(user, amount, note)

# ------------------------------------------------------------------------------
# Command-Line Interface
# ------------------------------------------------------------------------------
def main():
    """Parse CLI args and execute corresponding VenmoService commands."""
    parser = argparse.ArgumentParser(description='Venmo Scraper CLI')
    parser.add_argument('--headless', action='store_true', help='Run browser headlessly')
    sub = parser.add_subparsers(dest='cmd', required=True)
    # Define subcommands
    sub.add_parser('login', help='Login to Venmo')
    sub.add_parser('logout', help='Logout (close browser)')
    sub.add_parser('balance', help='Show balance')
    p_hist = sub.add_parser('history', help='Show transaction history')
    p_hist.add_argument('--limit', type=int, default=10)
    sub.add_parser('profile', help='View profile')
    p_upd = sub.add_parser('update-profile', help='Update profile')
    p_upd.add_argument('--display', dest='display_name')
    p_upd.add_argument('--about')
    p_send = sub.add_parser('send', help='Send money')
    p_send.add_argument('user')
    p_send.add_argument('amount', type=float)
    p_send.add_argument('--note', default='')
    p_req = sub.add_parser('request', help='Request money')
    p_req.add_argument('user')
    p_req.add_argument('amount', type=float)
    p_req.add_argument('--note', default='')

    args = parser.parse_args()
    svc = VenmoService(headless=args.headless)

    try:
        # Execute based on chosen subcommand
        if args.cmd == 'login':
            svc.login()
            print('Logged in successfully.')
        elif args.cmd == 'logout':
            svc.logout()
            print('Logged out.')
        elif args.cmd == 'balance':
            svc.login()
            bal = svc.view_balance()
            print(f'Balance: ${bal:.2f}')
        elif args.cmd == 'history':
            svc.login()
            txs = svc.view_transactions(limit=args.limit)
            from tabulate import tabulate
            print(tabulate(txs, headers='keys', tablefmt='github'))
        elif args.cmd == 'profile':
            svc.login()
            prof = svc.view_profile()
            for k,v in prof.items(): print(f'{k}: {v}')
        elif args.cmd == 'update-profile':
            svc.login()
            # Filter only provided fields
            updates = {k:v for k,v in vars(args).items() if k in ('display_name','about') and v}
            prof = svc.update_profile(**updates)
            for k,v in prof.items(): print(f'{k}: {v}')
        elif args.cmd == 'send':
            svc.login()
            svc.send_money(args.user, args.amount, args.note)
            print(f'Sent ${args.amount} to {args.user}')
        elif args.cmd == 'request':
            svc.login()
            svc.request_money(args.user, args.amount, args.note)
            print(f'Requested ${args.amount} from {args.user}')
    except Exception as e:
        # Log errors and exit with failure
        logger.error('Operation failed: %s', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
