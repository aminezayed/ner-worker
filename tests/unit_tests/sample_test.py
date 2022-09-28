from unittest import TestCase
from app.helpers.body_loader import Body_Loader
# TODO: add tests and stop doing lazy work


class MyTest(TestCase):
    def test_valid_body(self):
        test = Body_Loader.parse_file_url
        self.assertTrue(True)
