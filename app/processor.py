from decimal import Decimal


class Processor(object):

    def __init__(self, db):
        self.db = db

    def parse_event(self, event):
        event_type, name, *args = event.split()
        method = getattr(self, event_type.lower())
        method(name, *args)

    def parse_dollars(self, amount):
        return Decimal(amount.strip('$'))

    def luhn_checksum(self, card_number):
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
        print('Adding credit card {0} for {1} with {2} limit'.format(card_number, name, limit))
        if self.is_luhn_valid(card_number):
            balance = Decimal(0)
        else:
            balance = 'error'

        self.db[name] = {'card_number': card_number, 'limit': self.parse_dollars(limit), 'balance': balance}

    def charge(self, name, amount):
        print('Charging {0} {1}'.format(name, amount))
        account = self.db.get(name, None)
        balance = account.get('balance', None)
        card_number = account.get('card_number')
        limit = account.get('limit', None)

        if self.parse_dollars(amount) + balance > limit or not self.is_luhn_valid(card_number):
            return

        account['balance'] += self.parse_dollars(amount)

    def credit(self, name, amount):
        print('Crediting {0} {1}'.format(name, amount))
        account = self.db.get(name, None)
        card_number = account.get('card_number')

        if not self.is_luhn_valid(card_number):
            return

        account = self.db.get(name, None)
        account['balance'] -= self.parse_dollars(amount)

    def write_output(self):
        for key in sorted(self.db.keys()):
            print('%s: %s' % (key, self.db[key].get('balance')))
