import unittest
from src.extractors.phone.phoneNumberExtractor import NumberExtractor, filter_on_number_is_date, \
    filter_on_number_contains_only_one_parenthesis_pair, filter_on_minus_only_between_two_numbers, \
    filter_on_slashes_only_between_two_numbers, create_filter_on_minimum_number_of_digits
from random import shuffle


class Basefilter_on_number_prefix_and_sufix_test(unittest.TestCase):
    def setUp(self):
        self.numberExtractor = NumberExtractor()

    def test_numbers_at_beggining_and_end_of_line(self):
        candidate_list = [("", "+385123456", " "), ("", "+385123456", "  "), (" ", "+385123456", ""),
                          ("", "+385123456", "")]
        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)
        self.assertTrue(candidate_list[2][1] in filtered_list)

    def test_numbers_in_the_middle(self):
        candidate_list = [(" ", "+385123456", " "), (" ", "+385123456", "  "), ('', "+385123456", ' ')]
        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)

    def test_numbers_before_dot(self):
        candidate_list = [(" ", "+385123456", "."), (" ", "+385123456", ". ")]

        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)

    def test_numbers_before_coma(self):
        candidate_list = [(" ", "+385123456", ","), (" ", "+385123456", ", ")]

        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)

    def test_numbers_before_unvalid_char(self):
        candidate_list = [("a", "+385123456", " "), (".", "+385123456", " "), (",", "+385123456", " "),
                          ("!", "+385123456", " ")]

        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), 0)

    def test_numbers_after_unvalid_char(self):
        candidate_list = [(" ", "+385123456", "a"), (" ", "+385123456", "a "), (" ", "+385123456", "!"),
                          (" ", "+385123456", "! ")
            , (" ", "+385123456", ".."), (" ", "+385123456", ",,"), (" ", "+385123456", ".1")]

        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), 0)

    def test_numbers_after_valid_char(self):
        candidate_list = [(" ", "+385123456", " a"), (" ", "+385123456", " p"), (" ", "+385123456", " !")]

        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)
        self.assertTrue(candidate_list[2][1] in filtered_list)

    def test_couple_valind_and_couple_invalid(self):
        valid_candidates = [(" ", "+385123456", " "), (" ", "+385123456", ", "), ("", "+385123456", ""),
                            (" ", "+385123456", ". "), (" ", "+385123456", ""), (" ", "+385123456", ", ")]
        invalid_candidates = [(" ", "+385123456", ".."), (" ", "+385123456", ".2 "), ("", "+385123456", "! "),
                              (".", "+385123456", ""), (",", "+385123456", ""), ("a", "+385123456", ", "),
                              ("-", "+385123456", ", ")]

        joined_list = valid_candidates + invalid_candidates
        shuffle(joined_list)
        filtered_list = self.numberExtractor.basefilter_on_number_prefix_and_sufix(joined_list)
        self.assertEqual(len(filtered_list), len(valid_candidates))
        self.assertTrue(valid_candidates[0][1] in filtered_list)
        self.assertTrue(valid_candidates[1][1] in filtered_list)
        self.assertTrue(valid_candidates[2][1] in filtered_list)
        self.assertTrue(valid_candidates[3][1] in filtered_list)
        self.assertTrue(valid_candidates[4][1] in filtered_list)
        self.assertTrue(valid_candidates[5][1] in filtered_list)


class filter_on_number_is_date_test(unittest.TestCase):

    def test_possible_date_formats_1(self):
        candidates = ["2023-10-10", "2023 10 10", "2023 14", "2023-14", "14"]
        filtered_candidates = filter_on_number_is_date(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    # def test_possible_date_formats_but_not_date(self):
    #    candidates = ["2023-32-10", "14-10-2023", "2023 10", "10 2023"]
    #    filtered_candidates = filter_on_number_is_date(candidates)

    #    self.assertEqual(len(filtered_candidates), 0)


class filter_on_number_contains_only_one_parenthesis_pair_test(unittest.TestCase):

    def test_no_brackets(self):
        candidates = ["+385 101 101", "385 101 101", "+385-101-101"]
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

    def test_valid_brackets(self):
        candidates = ["(+385) 101 101", "(385) 101 101", "+385(101)101", "+385 (101) 101"]
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])
        self.assertEqual(candidates[3], filtered_candidates[3])

    def test_invalid_multiple_brackets(self):
        candidates = ["(+385) (101) 101", "(385)() 101 101", "+385(101)(1)01", "+3(85) (101) 101"]
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_invalid_only_opening_bracket(self):
        candidates = ["(+385 101 101", "(385 ( 101 101", "+385 (101 1 01", "+3 85 101 10(1"]
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_invalid_only_closing_bracket(self):
        candidates = [")+385 101 101", ")385 ) 101 101", "+385 )101 1 01", "+3 85 101 10(1"]
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_valid_invalid_mix(self):
        valid_candidates = ["(+385) 101 101", "(385) 101 101", "+385(101)101", "+385 (101) 101"]
        invalid_candidates = [")+385 101 101", ")385 ) 101 101", "+385 )101 1 01", "+3 85 101 10(1"]

        joined = valid_candidates + invalid_candidates
        shuffle(joined)
        filtered_candidates = filter_on_number_contains_only_one_parenthesis_pair(joined)

        self.assertEqual(len(filtered_candidates), 4)
        self.assertTrue(valid_candidates[0] in filtered_candidates)
        self.assertTrue(valid_candidates[1] in filtered_candidates)
        self.assertTrue(valid_candidates[2] in filtered_candidates)
        self.assertTrue(valid_candidates[3] in filtered_candidates)


class Filter_on_minus_only_between_two_numbers_test(unittest.TestCase):

    def test_no_minuses(self):
        candidates = ["+385 101 101", "385 101 101", "+(385) 101 101"]
        filtered_candidates = filter_on_minus_only_between_two_numbers(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

    def test_minuses_between_numbers(self):
        candidates = ["+385-101-101", "385-101 101", "13-13-13"]
        filtered_candidates = filter_on_minus_only_between_two_numbers(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

    def test_minuses_not_between_two_number(self):
        candidates = ["1 -101101", "385 (-101 101", "13 13-)13", "1313 - 13", "13-13 - 13", "13--13  13"]
        filtered_candidates = filter_on_minus_only_between_two_numbers(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_valind_and_invalid_mix(self):
        valid_candidates = ["+385 101 101", "385-101 101", "13-13-13"]
        invalid_candidates = ["1 -101101", "385 (-101 101", "13 13-)13", "1313 - 13", "13-13 - 13", "13--13  13"]

        joined = valid_candidates + invalid_candidates
        shuffle(joined)
        filtered_candidates = filter_on_minus_only_between_two_numbers(joined)

        self.assertEqual(len(filtered_candidates), len(valid_candidates))
        self.assertTrue(valid_candidates[0] in filtered_candidates)
        self.assertTrue(valid_candidates[1] in filtered_candidates)
        self.assertTrue(valid_candidates[2] in filtered_candidates)


class Filter_on_minus_only_slashes_two_numbers_test(unittest.TestCase):

    def test_no_slashes(self):
        candidates = ["+385 101 101", "385 101 101", "+(385) 101 101"]
        filtered_candidates = filter_on_slashes_only_between_two_numbers(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

    def test_slashes_between_numbers(self):
        candidates = ["+385\\801\\101", "385\\101\\101", "13\\13\\13"]
        filtered_candidates = filter_on_slashes_only_between_two_numbers(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

        candidates = ["+385/101/101", "385/101/101", "13/13/13"]
        filtered_candidates = filter_on_slashes_only_between_two_numbers(candidates)

        self.assertEqual(candidates[0], filtered_candidates[0])
        self.assertEqual(candidates[1], filtered_candidates[1])
        self.assertEqual(candidates[2], filtered_candidates[2])

    def test_slashes_not_between_two_number(self):
        candidates = ["1 \\101101", "385 (\\101 101", "13 13\\)13", "1313 \\ 13", "13\\13 \\ 13", "13\\\\13  13"]
        filtered_candidates = filter_on_slashes_only_between_two_numbers(candidates)

        self.assertEqual(len(filtered_candidates), 0)

        candidates = ["1 /101101", "385 (/101 101", "13 13/)13", "1313 / 13", "13/13 / 13", "13//13  13"]
        filtered_candidates = filter_on_slashes_only_between_two_numbers(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_valind_and_invalid_mix(self):
        valid_candidates = ["+385 101 101", "(+385) 101 101", "(+385) 101-101", "385\\101 101", "13/13/13",
                            "099\\111\\111"]
        invalid_candidates = ["1 \\101101", "385 (/101 101", "13 13/)13", "1313 \\ 13", "13\\13 \\ 13", "13//13  13"]

        joined = valid_candidates + invalid_candidates
        shuffle(joined)
        filtered_candidates = filter_on_slashes_only_between_two_numbers(joined)

        self.assertEqual(len(filtered_candidates), len(valid_candidates))
        self.assertTrue(valid_candidates[0] in filtered_candidates)
        self.assertTrue(valid_candidates[1] in filtered_candidates)
        self.assertTrue(valid_candidates[2] in filtered_candidates)
        self.assertTrue(valid_candidates[3] in filtered_candidates)
        self.assertTrue(valid_candidates[4] in filtered_candidates)
        self.assertTrue(valid_candidates[5] in filtered_candidates)

class Filter_on_minimum_number_of_digits(unittest.TestCase):

    def test_numbers_are_valid(self):
        filter = create_filter_on_minimum_number_of_digits(minimum_number_of_digits=6)
        candidates = ["+385 101 101", "(+385) 101 101", "(+385) 101-101", "385\\101 101", "13/13/13", "099\\111\\111"]
        filtered_candidates = filter(candidates)

        self.assertEqual(len(filtered_candidates), len(candidates))
        self.assertTrue(candidates[0] in filtered_candidates)
        self.assertTrue(candidates[1] in filtered_candidates)
        self.assertTrue(candidates[2] in filtered_candidates)
        self.assertTrue(candidates[3] in filtered_candidates)
        self.assertTrue(candidates[4] in filtered_candidates)
        self.assertTrue(candidates[5] in filtered_candidates)

    def test_numbers_are_not_valid(self):
        filter = create_filter_on_minimum_number_of_digits(minimum_number_of_digits=6)
        candidates = ["+01 101", "101 10", "12345", "11 11 2", "(34)44", "2-3-4-1-3", "2/3/4/1/3", "2\\3\\4\\1\\3", "2\\3/4-1(3)"]
        filtered_candidates = filter(candidates)

        self.assertEqual(len(filtered_candidates), 0)

    def test_valind_and_invalid_mix(self):
        filter = create_filter_on_minimum_number_of_digits(minimum_number_of_digits=6)
        valid_candidates = ["+385 101 101", "(+385) 101 101", "(+385) 101-101", "385\\101 101", "13/13/13", "099\\111\\111"]
        invalid_candidates = ["+01 101", "101 10", "12345", "11 11 2", "(34)44", "2-3-4-1-3", "2/3/4/1/3", "2\\3\\4\\1\\3", "2\\3/4-1(3)"]

        joined = valid_candidates + invalid_candidates
        shuffle(joined)
        filtered_candidates = filter(joined)

        self.assertEqual(len(filtered_candidates), len(valid_candidates))
        self.assertTrue(valid_candidates[0] in filtered_candidates)
        self.assertTrue(valid_candidates[1] in filtered_candidates)
        self.assertTrue(valid_candidates[2] in filtered_candidates)
        self.assertTrue(valid_candidates[3] in filtered_candidates)
        self.assertTrue(valid_candidates[4] in filtered_candidates)
        self.assertTrue(valid_candidates[5] in filtered_candidates)


if __name__ == '__main__':
    unittest.main()
