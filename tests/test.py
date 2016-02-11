import sys
import unittest
from os import path
import decimal

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from processor.processor import Processor
from processor.exceptions import ParseError


class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = Processor()

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

    def test_card_number_is_numberic_in_luhn_checksum(self):
        self.assertRaises(ValueError, self.processor.luhn_checksum, 'fail')

    def test_card_number_is_numberic_in_is_luhn_valid(self):
        self.assertRaises(ValueError, self.processor.is_luhn_valid, 'fail')

    def test_luhn_catches_invalid_invalid_numbers(self):
        self.assertFalse(self.processor.is_luhn_valid('1234567890123456'))

    def test_invalid_card_balance_equals_error(self):
        self.processor.add('name', '1234567890123456', '$4000')
        self.assertEqual(self.processor.db['name']['balance'], 'error')

    def test_balance_type_is_decimal(self):
        self.processor.add('name', '4111111111111111', '$4000')
        self.assertIsInstance(self.processor.db['name']['balance'], decimal.Decimal)

    def test_nonexistant_account_name_raises_key_error(self):
        self.processor.db = {}  # empty the db so account definitely will not exist
        self.assertRaises(KeyError, self.processor.charge, 'Non-Existent account', '$1000')


if __name__ == '__main__':
    unittest.main()
