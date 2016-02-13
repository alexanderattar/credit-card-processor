import sys
import unittest
from os import path
from decimal import Decimal

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from processor.processor import Processor
from processor.exceptions import ParseError


class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = Processor()

    # event parsing
    def test_event_is_string(self):
        self.assertRaises(ValueError, self.processor.parse_event, 0)

    def test_parse_event_can_upack_string(self):
        self.assertRaises(ValueError, self.processor.parse_event, 'Add')

    def test_parse_event_has_valid_args(self):
        self.assertRaises(ParseError, self.processor.parse_event, 'Add Tom')

    def test_parse_dollars_has_valid_number(self):
        self.assertRaises(ValueError, self.processor.parse_dollars, '$fail')

    def test_parse_dollars_returns_valid_card_number(self):
        self.assertTrue(self.processor.parse_dollars('4111111111111111').isdigit())

    # luhn
    def test_card_number_is_numberic_in_luhn_checksum(self):
        self.assertRaises(ValueError, self.processor.luhn_checksum, 'fail')

    def test_card_number_is_numberic_in_is_luhn_valid(self):
        self.assertRaises(ValueError, self.processor.is_luhn_valid, 'fail')

    def test_luhn_catches_invalid_invalid_numbers(self):
        self.assertFalse(self.processor.is_luhn_valid('1234567890123456'))

    # add
    def test_invalid_card_balance_equals_error(self):
        self.processor.add('User', '1234567890123456', '$4000')
        self.assertEqual(self.processor.db['User']['balance'], 'error')

    def test_balance_type_is_decimal(self):
        self.processor.add('User', '4111111111111111', '$4000')
        self.assertIsInstance(self.processor.db['User']['balance'], Decimal)

    # get account
    def test_nonexistant_account_name_raises_key_error(self):
        self.assertRaises(KeyError, self.processor.get_account_details, 'Non-Existent account')

    def test_missing_param_raises_key_error(self):
        self.processor.db['User'] = {'card_number': '4111111111111111', 'limit': '$5000', 'balance': None}
        self.assertRaises(KeyError, self.processor.get_account_details, 'User')

    # charge
    def test_charge_with_bad_params_raises_type_error(self):
        self.processor.db['User'] = {
            'card_number': '4111111111111111', 'limit': Decimal('9000'), 'balance': Decimal('9000')
        }
        self.assertRaises(TypeError, self.processor.charge, 'User', '$1000')

    def test_amount_over_limit_doesnt_charge(self):
        self.processor.db['User'] = {
            'card_number': '4111111111111111', 'limit': Decimal('9000'), 'balance': Decimal('9000')
        }
        self.assertEqual(self.processor.charge('User', Decimal('1')), Decimal('9000'))  # over 9000 ;)

    def test_invalid_card_is_not_charged(self):
        self.processor.add('User', '1234567890123456', Decimal('9000'))
        self.assertEqual(self.processor.charge('User', Decimal('1')), 'error')

    def test_credit_correctly_decreases_balance(self):
        self.processor.add('User', '4111111111111111', Decimal('9000'))
        self.processor.credit('User', Decimal())

    # credit
    def test_credit_with_bad_params_raises_type_error(self):
        self.processor.db['User'] = {
            'card_number': '4111111111111111', 'limit': Decimal('9000'), 'balance': Decimal('9000')
        }
        self.assertRaises(TypeError, self.processor.credit, 'User', '$1000')

    def test_invalid_card_is_not_credited(self):
        self.processor.add('User', '1234567890123456', Decimal('9000'))
        self.assertEqual(self.processor.credit('User', Decimal('1')), 'error')


if __name__ == '__main__':
    unittest.main()
