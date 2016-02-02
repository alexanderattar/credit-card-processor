import unittest
from app.processor import Processor


class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = Processor()

    def test_calculator_add_method_returns_correct_result(self):
        result = self.calc.add(2, 2)
        self.assertEqual(4, result)

    def test_calculator_returns_error_message_if_both_args_not_numbers(self):
        self.assertRaises(ValueError, self.calc.add, 'two', 'three')

if __name__ == '__main__':
    unittest.main()
