from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Test that 1 + 1 always equal 2.
        """
        self.assertEqual(1 + 1, 2)
