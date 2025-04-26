from django.test import TestCase
from .requests import Request  # Make sure we're importing from local requests.py
from .mocks.data import MOCK_DATA

class TestRequest(TestCase):
    def setUp(self):
        self.request = Request()

    def test_get_physician(self):
        physician, error = self.request.request_physicians(1)
        self.assertFalse(error)
        self.assertEqual(physician["name"], "Dr. House")

    def test_physician_not_found(self):
        physician, error = self.request.request_physicians(999)
        self.assertTrue(error)
        self.assertEqual(physician["error"]["code"], "02")
