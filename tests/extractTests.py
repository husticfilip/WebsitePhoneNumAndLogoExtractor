import unittest

#TODO makni iz src foldera import
from src.extract import format_logo_path, format_phone_numbers


class Format_phone_number_and_logo_path_tests(unittest.TestCase):

    def test_format_phone_numbers_no_numbers(self):
        phone_numbers = []
        formated = format_phone_numbers(phone_numbers)
        self.assertEqual(None, formated)

    def test_format_phone_numbers_test_normal_num(self):
        phone_numbers = ["13 23 33", "13-23-33", "13\\23\\33", "13/23/33"]
        formated = format_phone_numbers(phone_numbers)

        self.assertEqual(len(formated), 1)
        self.assertTrue("13 23 33" in formated)

    def test_format_phone_numbers_test_normal_num_plus(self):
        phone_numbers = ["+13 23 33", "+13-23-33", "+13\\23\\33", "+13/23/33"]
        formated = format_phone_numbers(phone_numbers)

        self.assertEqual(len(formated), 1)
        self.assertTrue("+13 23 33" in formated)

    def test_format_phone_numbers_test_paranthesis(self):
        phone_numbers = [ "(13) 23 33",  "(13)-23-33", "(13)\\23\\33", "(13)/23/33"]
        formated = format_phone_numbers(phone_numbers)

        self.assertEqual(len(formated), 1)
        self.assertTrue("(13) 23 33" in formated)

    def test_format_phone_numbers_test_paranthesis_plus(self):
        phone_numbers = [ "+(13) 23 33",  "+(13)-23-33", "+(13)\\23\\33", "+(13)/23/33"]
        formated = format_phone_numbers(phone_numbers)

        self.assertEqual(len(formated), 1)
        self.assertTrue("+(13) 23 33" in formated)

    def test_format_logo_path_empty_path(self):
        url ="www.hr.com"
        logo_path = ""
        formated = format_logo_path(logo_path, url)
        self.assertEqual("", formated)

    def test_format_logo_path_both_having_slashes(self):
        url ="www.hr.com/"
        logo_path = "/logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

        url = "www.hr.com\\"
        logo_path = "\\logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

    def test_format_logo_path_only_logo_having_slashes(self):
        url ="www.hr.com"
        logo_path = "/logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

        url = "www.hr.com"
        logo_path = "\\logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

    def test_format_logo_path_only_url_having_slashes(self):
        url ="www.hr.com/"
        logo_path = "logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

        url = "www.hr.com\\"
        logo_path = "logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)

    def test_format_logo_path_none_having_slashes(self):
        url ="www.hr.com"
        logo_path = "logo.png"
        formated = format_logo_path(logo_path, url)
        self.assertEqual("www.hr.com/logo.png", formated)