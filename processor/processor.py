import re
import sys
from decimal import Decimal

from processor.exceptions import ParseError
from processor.utils import setup_logger

log = setup_logger('logger')


class Processor(object):

    def __init__(self, *args, **kwargs):
        """
        Initialize the Processor instance with a structure to contain data.
        A preexisting database can be passed in the kwargs opening up the possibility
        for Processors to be instantiated as workers.

        Accounts are stores in a hash in the format: db = {
            'Tom': {'card_number': '4111111111111111', 'balance': 1000, 'limit': 2000}
            'Lisa': {'card_number': '4111111111111111', 'balance': 1000, 'limit': 2000}
        }
        """
        self.db = kwargs.get('db', {})
        if not isinstance(self.db, dict):
            raise TypeError('Database must be dictionary')

    def parse_event(self, event):
        """
        Parse event string into event components and passes them as parameters
        to the methods that perform Processor actions.

        :param event - string
        """

        if not isinstance(event, str):
            raise ValueError('Event type must be string')

        event_type, name, *numbers = event.split()

        if not numbers:
            raise ParseError((
                'Processor requires event_type, name,'
                'and additional method args: {0}'.format(numbers)
            ))

        # strip $ signs from amounts
        args = map(self.parse_dollars, numbers)

        # call processor method via the event type
        method = getattr(self, event_type.lower())
        method(name, *args)

    @staticmethod
    def parse_dollars(number):
        """
        Parse dollar value from string.

        :param number - must be numeric string, but can contain $ sign.

        If number is dollar amount, strip $ sign and cast to Decimal
        so balance can be mutated via mathmatical operations.

        If number is not dollar amount it should be a credit card number and should be left as string.
        Raises ValueError if number contains non-numeric characters besides the $ sign.
        """
        if not re.match(r'[$+-]?(\d+(\.\d*)?|\.\d+)', number):
            raise ValueError('Number must be numeric')
        if '$' in number:
            return Decimal(number.strip('$'))
        else:
            return number

    @staticmethod
    def check_amount(amount):
        """
        Helper method to validate amount is of type Decimal

        :param amount - Decimal
        """
        if not isinstance(amount, Decimal):
            raise TypeError((
                'Invalid parameter type(s) - '
                'amount={0} must be Decimal'.format(type(amount))
            ))

    @staticmethod
    def luhn_checksum(card_number):
        """
        Python implementation of Luhn algorithm.
        https://en.wikipedia.org/wiki/Luhn_algorithm

        :param card_number - string
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def is_luhn_valid(self, card_number):
        """
        Test card number with Luhn algorithm.

        :param card_number - string
        """
        return self.luhn_checksum(card_number) == 0

    def add(self, name, card_number, limit):
        """
        Add a new credit card to the database.
        Checks is card number is valid with Luhn check

        :param name - string
        :param card_number - string
        :param limit - Decimal
        """
        log.info('Adding credit card {0} for {1} with {2} limit'.format(card_number, name, limit))

        if self.is_luhn_valid(card_number):
            balance = Decimal(0)
        else:
            log.warning('Card number {0} is not Luhn valid'.format(card_number))
            balance = 'error'

        self.db[name] = {'card_number': card_number, 'limit': limit, 'balance': balance}

    def get_account_details(self, name):
        """
        Abstracts logic for retrieving an account and it's data from the db.
        Exception handling is built in for missing accounts or data required
        to perform processor actions such as charging and crediting.
        """

        try:  # to get account
            account = self.db[name]
        except KeyError as e:
            log.error('Account doesn\'t exist')
            raise

        if not isinstance(name, str):
            raise TypeError((
                'Invalid parameter type(s) - '
                'name={0} must be str and'.format(type(name), type(amount))
            ))

        balance = account.get('balance', None)
        card_number = account.get('card_number', None)
        limit = account.get('limit', None)

        # check for missing params
        if any(param is None for param in [balance, card_number, limit]):
            raise KeyError((
                'Missing parameter(s) required for processing charge - '
                'balance={0} card_number={1} limit={2}'.format(balance, card_number, limit)
            ))

        return account, balance, card_number, limit

    def charge(self, name, amount):
        """
        Charge account associated with the name a certain amount.
        Checks is card number is valid with Luhn check

        :param name - string
        :param amount - Decimal
        """
        log.info('Charging {0} {1}'.format(name, amount))
        self.check_amount(amount)
        account, balance, card_number, limit = self.get_account_details(name)

        # fast fails if card is not valid so we don't end up
        # comparing decimal amounts with str for error balances
        if not self.is_luhn_valid(card_number) or amount + balance > limit:
            return balance

        account['balance'] += amount

    def credit(self, name, amount):
        """
        Credit account associated with the name a certain amount.
        Checks is card number is valid with Luhn check

        :param name - string
        :param amount - Decimal
        """
        log.info('Crediting {0} {1}'.format(name, amount))
        self.check_amount(amount)

        account, balance, card_number, limit = self.get_account_details(name)

        if not self.is_luhn_valid(card_number):
            return balance

        account = self.db.get(name, None)
        account['balance'] -= amount

    def generate_summary(self):
        """
        Generates the summary string in preparation for output.
        Formats the summary in alphabetical order by name.
        Appends a $ to dollar values and not to accounts in error.
        Each summary line ends with a \n
        """
        summary = ''
        for key in sorted(self.db.keys()):
            balance = '${0}'.format(self.db[key].get('balance'))

            if 'error' in balance:
                balance = balance.strip('$')

            summary += '{0}: {1}\n'.format(key, balance)
        return summary

    @staticmethod
    def write_output(summary):
        """
        Simple wrapper method for writing output to stout.
        It can be easily extended to write to file.

        :param summary - string
        """
        sys.stdout.write(summary)
