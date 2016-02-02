import sys
import logging
from decimal import Decimal

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


class Processor(object):

    def __init__(self, *args, **kwargs):
        self.db = {}

    def parse_event(self, event):

        try:  # to parse event
            event_type, name, *args = event.split()
        except Exception as e:
            raise Exception('ParseError: {0}'.format(str(e)))

        method = getattr(self, event_type.lower())
        method(name, *args)

    @staticmethod
    def parse_dollars(amount):
        if '$' in amount:
            return Decimal(amount.strip('$'))

    @staticmethod
    def luhn_checksum(card_number):
        # Python implementation of Luhn algorithm
        # https://en.wikipedia.org/wiki/Luhn_algorithm
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
        return self.luhn_checksum(card_number) == 0

    def add(self, name, card_number, limit):
        log.info('Adding credit card {0} for {1} with {2} limit'.format(card_number, name, limit))

        if self.is_luhn_valid(card_number):
            balance = Decimal(0)
        else:
            balance = 'error'

        self.db[name] = {'card_number': card_number, 'limit': self.parse_dollars(limit), 'balance': balance}

    def charge(self, name, amount):
        log.info('Charging {0} {1}'.format(name, amount))
        account = self.db.get(name, None)
        balance = account.get('balance', None)
        card_number = account.get('card_number')
        limit = account.get('limit', None)

        if self.parse_dollars(amount) + balance > limit or not self.is_luhn_valid(card_number):
            return

        account['balance'] += self.parse_dollars(amount)

    def credit(self, name, amount):
        log.info('Crediting {0} {1}'.format(name, amount))
        account = self.db.get(name, None)
        card_number = account.get('card_number')

        if not self.is_luhn_valid(card_number):
            return

        account = self.db.get(name, None)
        account['balance'] -= self.parse_dollars(amount)

    def write_output(self):
        for key in sorted(self.db.keys()):
            balance = '${0}'.format(self.db[key].get('balance')) if not self.db[key].get('balance') == 'error' else self.db[key].get('balance')
            log.info('%s: %s' % (key, balance))
