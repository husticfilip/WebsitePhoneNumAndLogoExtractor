import unittest

from src.extractors.phone.phoneNumberExtractor import PhoneNumberExtractor


class Extract_candidate_list_test(unittest.TestCase):

    def setUp(self):
        self.numberExtractor = PhoneNumberExtractor()

    def compareTuples(self, tup1, tup2):
        for e1, e2 in zip(tup1, tup2):
            self.assertEqual(e1, e2)

    def test_normal_num(self):
        list = self.numberExtractor.extract_candidate_list(" 99 999 9993 ")
        self.compareTuples((" ", "99 999 9993", " "), list[0])
        list = self.numberExtractor.extract_candidate_list(" 99 999 9993  ")
        self.compareTuples((" ", "99 999 9993", "  "), list[0])

        list = self.numberExtractor.extract_candidate_list(" 999999993  ")
        self.compareTuples((" ", "999999993", "  "), list[0])
        list = self.numberExtractor.extract_candidate_list(" 999999993 ")
        self.compareTuples((" ", "999999993", " "), list[0])


    def test_normal_num_with_plus(self):
        list = self.numberExtractor.extract_candidate_list(" +99 999 9993 ")
        self.compareTuples((" ", "+99 999 9993", " "), list[0])

        list = self.numberExtractor.extract_candidate_list(" +999999993  ")
        self.compareTuples((" ", "+999999993", "  "), list[0])

    def test_number_at_beggining_of_line(self):
        list = self.numberExtractor.extract_candidate_list("99 999 9993 ")
        self.compareTuples(("", "99 999 9993", " "), list[0])

        list = self.numberExtractor.extract_candidate_list("+99 999 9993 ")
        self.compareTuples(("", "+99 999 9993", " "), list[0])

    def test_number_before_dot(self):
        list = self.numberExtractor.extract_candidate_list("99 999 9993.")
        self.compareTuples(("", "99 999 9993", "."), list[0])

        list = self.numberExtractor.extract_candidate_list("99 999 9993.  ")
        self.compareTuples(("", "99 999 9993", ". "), list[0])

    def test_number_before_coma(self):
        list = self.numberExtractor.extract_candidate_list("99 999 9993,")
        self.compareTuples(("", "99 999 9993", ","), list[0])

        list = self.numberExtractor.extract_candidate_list("99 999 9993, ")
        self.compareTuples(("", "99 999 9993", ", "), list[0])

    def test_number_beetween_characters(self):
        list = self.numberExtractor.extract_candidate_list(
            "a+1111 11aa\n:+1111 11::\n-+1111 11- \n\"+1111 11\"\"\n\'+1111 11\'")
        self.compareTuples(("a", "+1111 11", "aa"), list[0])
        self.compareTuples(("\n:", "+1111 11", "::"), list[1])
        self.compareTuples(("\n-", "+1111 11", "- "), list[2])
        self.compareTuples(("\n\"", "+1111 11", "\"\""), list[3])
        self.compareTuples(("\n'", "+1111 11", "'"), list[4])

        list = self.numberExtractor.extract_candidate_list(
            "a1111 11aa\n:1111 11::\n-1111 11- \n\"1111 11\"\"\n\'1111 11\'")
        self.compareTuples(("a", "1111 11", "aa"), list[0])
        self.compareTuples(("\n:", "1111 11", "::"), list[1])
        self.compareTuples(("\n-", "1111 11", "- "), list[2])
        self.compareTuples(("\n\"", "1111 11", "\"\""), list[3])
        self.compareTuples(("\n'", "1111 11", "'"), list[4])

    def test_number_with_brackets(self):
        list = self.numberExtractor.extract_candidate_list("99 (999) 9993")
        self.compareTuples(("", "99 (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+99 (999) 9993")
        self.compareTuples(("", "+99 (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+(99) (999) 9993")
        self.compareTuples(("", "+(99) (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+(99) (999) 9993")
        self.compareTuples(("", "+(99) (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("(99) (999) 9993")
        self.compareTuples(("", "(99) (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list(".(99) (999) 9993")
        self.compareTuples((".", "(99) (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("\"(99) (999) 9993")
        self.compareTuples(("\"", "(99) (999) 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+(1) 999 9993")
        self.compareTuples(("", "+(1) 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("(1) 999 9993")
        self.compareTuples(("", "(1) 999 9993", ""), list[0])

    def test_number_with_minuses(self):
        list = self.numberExtractor.extract_candidate_list("99-999-9993")
        self.compareTuples(("", "99-999-9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+99-999-9993")
        self.compareTuples(("", "+99-999-9993", ""), list[0])

    def test_minus_in_front(self):
        list = self.numberExtractor.extract_candidate_list("-1 99 999 9993")
        self.compareTuples(("-", "1 99 999 9993", ""), list[0])
        list = self.numberExtractor.extract_candidate_list("-+1 99 999 9993")
        self.compareTuples(("-", "+1 99 999 9993", ""), list[0])

    def test_minus_at_the_end(self):
        list = self.numberExtractor.extract_candidate_list("1 99 999 9993-")
        self.compareTuples(("", "1 99 999 9993", "-"), list[0])



    def test_numbers_with_slash(self):
        list = self.numberExtractor.extract_candidate_list("99\\999 9993")
        self.compareTuples(("", "99\\999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+99\\999\\9993")
        self.compareTuples(("", "+99\\999\\9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("\\+99\\999\\9993\\")
        self.compareTuples(("\\", "+99\\999\\9993", "\\"), list[0])

    def test_numbers_with_backslash(self):
        list = self.numberExtractor.extract_candidate_list("99/999 9993")
        self.compareTuples(("", "99/999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("+99/999/9993")
        self.compareTuples(("", "+99/999/9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("/+99/999/9993/")
        self.compareTuples(("/", "+99/999/9993", "/"), list[0])

    def test_one_number_at_beginning(self):
        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993")
        self.compareTuples(("", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list(".+1 99 999 9993")
        self.compareTuples((".", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("1 99 999 9993")
        self.compareTuples(("", "1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("-1 99 999 9993")
        self.compareTuples(("-", "1 99 999 9993", ""), list[0])

    def test_sufix_extraction_empty_end(self):
        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993 ")
        self.compareTuples(("", "+1 99 999 9993", " "), list[0])

        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993  ")
        self.compareTuples(("", "+1 99 999 9993", "  "), list[0])

        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993   ")
        self.compareTuples(("", "+1 99 999 9993", "  "), list[0])

    def test_sufix_extraction_random_chars(self):
        list = self.numberExtractor.extract_candidate_list("101101.")
        self.compareTuples(("", "101101", "."), list[0])

        list = self.numberExtractor.extract_candidate_list("101101.  ")
        self.compareTuples(("", "101101", ". "), list[0])

        list = self.numberExtractor.extract_candidate_list("101101a   ")
        self.compareTuples(("", "101101", "a "), list[0])

        list = self.numberExtractor.extract_candidate_list("101101px  ")
        self.compareTuples(("", "101101", "px"), list[0])

        list = self.numberExtractor.extract_candidate_list("101101 px  ")
        self.compareTuples(("", "101101", " p"), list[0])

    def test_sufix_extraction_char_used_in_phone_number(self):
        list = self.numberExtractor.extract_candidate_list("101101-")
        self.compareTuples(("", "101101", "-"), list[0])

        list = self.numberExtractor.extract_candidate_list("101101+  ")
        self.compareTuples(("", "101101", "+ "), list[0])

        list = self.numberExtractor.extract_candidate_list("101101(   ")
        self.compareTuples(("", "101101", "( "), list[0])

        list = self.numberExtractor.extract_candidate_list("101101)")
        self.compareTuples(("", "101101", ")"), list[0])

    def test_tel_prefix(self):
        list = self.numberExtractor.extract_candidate_list("tel:+1 99 999 9993")
        self.compareTuples(("tel:", "+1 99 999 9993", ""), list[0])
        list = self.numberExtractor.extract_candidate_list("tel:+99 999 9993")
        self.compareTuples(("tel:", "+99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("tel:1 99 999 9993")
        self.compareTuples(("tel:", "1 99 999 9993", ""), list[0])
        list = self.numberExtractor.extract_candidate_list("tel:99 999 9993")
        self.compareTuples(("tel:", "99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("tel:(1) 99 999 9993")
        self.compareTuples(("tel:", "(1) 99 999 9993", ""), list[0])
        list = self.numberExtractor.extract_candidate_list("tel:(99) 999 9993")
        self.compareTuples(("tel:", "(99) 999 9993", ""), list[0])

    def test_key_words_prefix(self):
        list = self.numberExtractor.extract_candidate_list("Phone   +1 99 999 9993")
        self.compareTuples(("Phone   ", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("phone   +1 99 999 9993")
        self.compareTuples(("phone   ", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("Mobile+1 99 999 9993")
        self.compareTuples(("Mobile", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("fax +1 99 999 9993")
        self.compareTuples(("fax ", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list(" number +1 99 999 9993")
        self.compareTuples((" number ", "+1 99 999 9993", ""), list[0])

    def test_key_words_with_trash_prefix(self):
        list = self.numberExtractor.extract_candidate_list("as Phone as  +1 99 999 9993")
        self.compareTuples(("as Phone as  ", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("this is Mobile or +1 99 999 9993")
        self.compareTuples(("this is Mobile or ", "+1 99 999 9993", ""), list[0])

        list = self.numberExtractor.extract_candidate_list("na koji fax ides +1 99 999 9993")
        self.compareTuples(("na koji fax ides ", "+1 99 999 9993", ""), list[0])

    def test_number_with_two_pluses_in_front(self):
        list = self.numberExtractor.extract_candidate_list("++99 999 9993")
        self.compareTuples(("++", "99 999 9993", ""), list[0])

    def test_two_pluses_at_the_end(self):
        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993++")
        self.compareTuples(("", "+1 99 999 9993", "++"), list[0])

    def test_multiple_numbers_in_line(self):
     list = self.numberExtractor.extract_candidate_list("+1 99 999 9993  tel:+1 99 999 9993  thiis1 99 999 9993aa  \n\"99 999 9993\"  ++99 999 9993.."
                                                        "fax:(99) 999 9993  +(99) 999 9993")
     self.compareTuples(("", "+1 99 999 9993", "  "), list[0])
     self.compareTuples(("tel:", "+1 99 999 9993", "  "), list[1])
     self.compareTuples(("thiis", "1 99 999 9993", "aa"), list[2])
     self.compareTuples(("  \n\"", "99 999 9993", "\" "), list[3])
     self.compareTuples((" ++", "99 999 9993", ".."), list[4])
     self.compareTuples(("fax:", "(99) 999 9993", "  "), list[5])
     self.compareTuples(("", "+(99) 999 9993", ""), list[6])


    def test_numbers_close_to_each_other(self):
        list = self.numberExtractor.extract_candidate_list("tel:+1 99 999 9993  +(99) 606 606  (99) 606 606  99 606 606")
        self.compareTuples(("tel:", "+1 99 999 9993", "  "), list[0])
        self.compareTuples(("", "+(99) 606 606", "  "), list[1])
        self.compareTuples(("", "(99) 606 606", "  "), list[2])
        self.compareTuples(("", "99 606 606", ""), list[3])

    # assumption is that there will be at lest two spaces between numbers
    def test_numbers_too_close_to_each_other(self):
        list = self.numberExtractor.extract_candidate_list("tel:+1 99 999 9993 +(99) 606 606")
        self.compareTuples(("tel:", "+1 99 999 9993", " +"), list[0])
        self.compareTuples(("", "(99) 606 606", ""), list[1])

    def test_numbers_separated_by_comma(self):
        list = self.numberExtractor.extract_candidate_list("tel:+1 99 999 9993, +(99) 606 606, 01 606 606")
        self.compareTuples(("tel:", "+1 99 999 9993", ", "), list[0])
        self.compareTuples(("", "+(99) 606 606", ", "), list[1])
        self.compareTuples(("", "01 606 606", ""), list[2])

    def test_numbers_between_other_words_by_comma(self):
        list = self.numberExtractor.extract_candidate_list("+1 99 999 9993  some paragraph +(99) 606 606  phone number is 01 606 606 end")
        self.compareTuples(("", "+1 99 999 9993", "  "), list[0])
        self.compareTuples(("some paragraph ", "+(99) 606 606", "  "), list[1])
        self.compareTuples(("phone number is ", "01 606 606", " e"), list[2])

    def test_no_numbers_in_text(self):
        list = self.numberExtractor.extract_candidate_list(
            " some paragraphphone number is  end")
        self.assertEqual(len(list), 0)

    def test_to_short_numbers_in_text(self):
        list = self.numberExtractor.extract_candidate_list("some 01 01 paragraphphone 51233 number +1234 is (01)1  end")
        self.assertEqual(len(list), 0)

    def test_decimal_numbers(self):
        list = self.numberExtractor.extract_candidate_list("11.12345")
        self.assertEqual(len(list), 0)

    # expected to find dates that are later filtered out of the solution list
    def test_date_numbers(self):
        list = self.numberExtractor.extract_candidate_list("10-11-2023  2023-10-11  2023-10  10-2023")
        self.compareTuples(("", "10-11-2023", "  "), list[0])
        self.compareTuples(("", "2023-10-11", "  "), list[1])
        self.compareTuples(("", "2023-10", "  "), list[2])
        self.compareTuples(("", "10-2023", ""), list[3])

        list = self.numberExtractor.extract_candidate_list("10 11 2023  2023 10 11  2023 10  10 2023")
        self.compareTuples(("", "10 11 2023", "  "), list[0])
        self.compareTuples(("", "2023 10 11", "  "), list[1])
        self.compareTuples(("", "2023 10", "  "), list[2])
        self.compareTuples(("", "10 2023", ""), list[3])

class Get_certain_phone_numbers_test(unittest.TestCase):

    def setUp(self):
        self.numberExtractor = PhoneNumberExtractor()

    def test_tel_tag(self):
        candidate_list = [("tel:", "+99 123 4565 ", ""), ("tel:", "+99 123 4565", ""), ("tel:", "99 123 4565", ""), ("tel: ","99 123 4565",""), ("tel: ","+99 123 4565","")]
        filtered_list = self.numberExtractor.get_certain_phone_numbers(candidate_list)

        self.assertEqual(len(filtered_list), len(candidate_list))
        self.assertTrue(candidate_list[0][1] in filtered_list)
        self.assertTrue(candidate_list[1][1] in filtered_list)
        self.assertTrue(candidate_list[2][1] in filtered_list)
        self.assertTrue(candidate_list[3][1] in filtered_list)
        self.assertTrue(candidate_list[4][1] in filtered_list)

        text = " \"tel:+99 123 4565  \n  tel: +99 123 4565   tel:99 123 4565  \n  \"tel: 99 123 4565, 'tel: 99 123 4565  'tel: +99 123 4565 "
        result_list = self.numberExtractor.get_certain_phone_numbers(text)

        self.assertEqual(result_list[0], "tel:+99 123 4565")
        self.assertEqual(result_list[1], "tel: +99 123 4565")
        self.assertEqual(result_list[2], "tel:99 123 4565")
        self.assertEqual(result_list[3], "tel: 99 123 4565")
        self.assertEqual(result_list[4], "tel: 99 123 4565")
        self.assertEqual(result_list[5], "tel: +99 123 4565")

    def test_false_tel_tag(self):
        text = " \"tel:a+99 123 4565  \n  \"tel:!+99 123 4565  tel:!+99 123 4565   \n "
        result_list = self.numberExtractor.get_certain_phone_numbers(text)

        self.assertEqual(len(result_list), 0)

    def test_phone_substring(self):
        text = "phone: \" +99 123 4565 \"    phone:\"+99 123 4565\"  phones:\"+99 123 4565\" mobile_phone: \"+99 123 4565\"   "
        result_list = self.numberExtractor.get_certain_phone_numbers(text)

        self.assertEqual(result_list[0], "phone: \" +99 123 4565 \"")
        self.assertEqual(result_list[1].strip(), "phone:\"+99 123 4565\"")
        self.assertEqual(result_list[2].strip(), "phones:\"+99 123 4565\"")
        self.assertEqual(result_list[3].strip(), "mobile_phone: \"+99 123 4565\"")

    def test_number_substring(self):
        text = "number: \" +99 123 4565 \"    number:\"+99 123 4565\"  numbers:\"+99 123 4565\" phone_number:\"+99 123 4565\"   "
        result_list = self.numberExtractor.get_certain_phone_numbers(text)

        self.assertEqual(result_list[0], "number: \" +99 123 4565 \"")
        self.assertEqual(result_list[1].strip(), "number:\"+99 123 4565\"")
        self.assertEqual(result_list[2].strip(), "numbers:\"+99 123 4565\"")
        self.assertEqual(result_list[3].strip(), "phone_number:\"+99 123 4565\"")

    def test_wrong_substrings(self):
        text = "id: \" 99 123 4565 \"    a:\"99 123 4565\"  something:\"99 123 4565\"   "
        result_list = self.numberExtractor.get_certain_phone_numbers(text)

        self.assertEqual(len(result_list), 0)




