"""Sample tests"""

from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    "test the calc module"

    def test_add_numbers(self):
        res = calc.add(1,2)
        self.assertEqual(res, 3)