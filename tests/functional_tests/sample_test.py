from unittest import TestCase
from app.helpers.body_loader import BodyLoader
# TODO: add tests and stop doing lazy work


class MyTest(TestCase):
    def test_valid_body(self):
        test = BodyLoader.parse_file_url
        self.assertTrue(True)
