from django.test import TestCase
from rango.models import Category


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Test that 1 + 1 always equal 2.
        """
        self.assertEqual(1 + 1, 2)


class CategoryMethodTest(TestCase):
    def test_ensure_views_are_positive(self):
        """
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)
