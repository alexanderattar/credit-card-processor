import re
from decimal import Decimal

from processor.exceptions import ParseError
from processor.utils import setup_logger

log = setup_logger()


class Processor(object):

    def __init__(self, *args, **kwargs):
        self.db = {}

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
    def luhn_checksum(card_number):
        """
        Python implementation of Luhn algorithm.

        https://en.wikipedia.org/wiki/Luhn_algorithm
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
        """Test card number with Luhn algorithm."""
        return self.luhn_checksum(card_number) == 0

    def add(self, name, card_number, limit):
        log.info('Adding credit card {0} for {1} with {2} limit'.format(card_number, name, limit))

        if self.is_luhn_valid(card_number):
            balance = Decimal(0)
        else:
            log.warning('Card number {0} is not Luhn valid'.format(card_number))
            balance = 'error'

        self.db[name] = {'card_number': card_number, 'limit': limit, 'balance': balance}

    def charge(self, name, amount):
        log.info('Charging {0} {1}'.format(name, amount))

        try:
            account = self.db[name]
        except KeyError as e:
            log.error('Account doesn\'t exist')
            raise

        balance = account.get('balance', None)
        card_number = account.get('card_number', None)
        limit = account.get('limit', None)

        # check for missing params
        if any(v is None for v in [balance, card_number, limit]):
            raise KeyError((
                'Missing parameter(s) required for processing charge - '
                'balance={0} card_number={1} limit={2}'.format(balance, card_number, limit)
            ))

        if amount + balance > limit or not self.is_luhn_valid(card_number):
            return

        account['balance'] += amount

    def credit(self, name, amount):
        log.info('Crediting {0} {1}'.format(name, amount))
        account = self.db.get(name, None)
        card_number = account.get('card_number')

        if not self.is_luhn_valid(card_number):
            return

        account = self.db.get(name, None)
        account['balance'] -= amount

    def write_output(self):
        log.info('\n\n=============== [SUMMARY] ===============')
        for key in sorted(self.db.keys()):
            balance = '${0}'.format(self.db[key].get('balance')) if not self.db[key].get('balance') == 'error' else self.db[key].get('balance')
            log.info('%s: %s' % (key, balance))
