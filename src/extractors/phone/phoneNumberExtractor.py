import re
from enum import Enum
from typing import List, Tuple
import logging

from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper

# Regexs representing possible date formats that could occur
# This are used in filter_on_number_is_date to filter out dates from possible phone numbers
POSSIBLE_DATE_FORMAT_REGEXS = [r'^\d\d\d\d(-\d\d){1,2}$',
                               r'^\d\d\d\d( \d\d){1,2}$',
                               r'^\d\d\d\d(\\\d\d){1,2}$',
                               r'^\d\d\d\d(/\d\d){1,2}$',

                               r'^(\d\d-){1,2}\d\d\d\d$',
                               r'^(\d\d ){1,2}\d\d\d\d$',
                               r'^(\d\d\\){1,2}\d\d\d\d$',
                               r'^(\d\d/){1,2}\d\d\d\d$']


def filter_on_number_is_date(phone_number_candidates: List[str]) -> List[str]:
    """
    Function filters out dates from the possible phone numbers.

    :param phone_number_candidates: list of phone number candidates
    :return: list containing phone number candidates that passed the test
    """
    passed_candidates = []
    for candidate in phone_number_candidates:
        valid = True
        for regex in POSSIBLE_DATE_FORMAT_REGEXS:
            # if date is found
            if re.search(regex, candidate):
                valid = False
                break
        if valid:
            passed_candidates.append(candidate)

    return passed_candidates


def filter_on_number_contains_maximum_one_parenthesis_pair(phone_number_candidates: List[str]) -> List[str]:
    """
    Function checks for valid usage of the parenthesis. Number should have only one open ( and one closed ) parenthesis.
    Also if ( is present ) should come after it in a number

    :param phone_number_candidates: list of phone number candidates
    :return: list containing phone number candidates that passed the test
    """
    passed_candidates = []
    for candidate in phone_number_candidates:
        open_parenthesis_positions = find_occurrences(candidate, '(')
        close_parenthesis_positions = find_occurrences(candidate, ')')

        # if there is no parenthesis then candidate passes filter
        if len(open_parenthesis_positions) == 0 and len(close_parenthesis_positions) == 0:
            passed_candidates.append(candidate)
        # if number has one open and one closed parenthesis and position of open one is before closed one then
        # candidate passes filter
        elif len(open_parenthesis_positions) == 1 and len(close_parenthesis_positions) == 1 and \
                open_parenthesis_positions[0] < close_parenthesis_positions[0]:
            passed_candidates.append(candidate)

    return passed_candidates


def filter_on_minus_only_between_two_numbers(phone_number_candidates: List[str]) -> List[str]:
    """
    Function checks for valid usage of - sign. - is used as the separator of numbers and should be used unly
    between two numbers ex. 01-322-332.
    We don't allow spaces or other signs around - ex.  01 - 322 - 332 or 01-322--332 are not valid.

     :param phone_number_candidates: list of phone number candidates
     :return: list containing phone number candidates that passed the test
     """
    return filter_on_char_only_between_two_numbers(phone_number_candidates, "-")


def filter_on_slashes_only_between_two_numbers(phone_number_candidates: List[str]) -> List[str]:
    """
    Function checks for valid usage of \ or / signs. Signs are used as the separator of numbers and should be used unly
    between two numbers ex. 01\322\332 or 01/322/332 .
    We don't allow spaces or other signs around \ and / ex.  01 \ 322 \ 332 or 01/322//332 are not valid.

     :param phone_number_candidates: list of phone number candidates
     :return: list containing phone number candidates that passed the test
     """
    passed = filter_on_char_only_between_two_numbers(phone_number_candidates, "\\")
    return filter_on_char_only_between_two_numbers(passed, "/")


def filter_on_char_only_between_two_numbers(phone_number_candidates: List[str], char: str) -> List[str]:
    """
    Function checks if position of provided char is between positions of two numbers.

    :param phone_number_candidates: list of phone number candidates
    :param char: letter for which we are testing
    :return: list containing phone number candidates that passed the test
    """
    passed_candidates = []
    for candidate in phone_number_candidates:
        char_positions = find_occurrences(candidate, char)
        if len(char_positions) == 0:
            passed_candidates.append(candidate)

        else:
            check_if_all_ok = [candidate[pos - 1].isnumeric() and candidate[pos + 1].isnumeric() for pos in
                               char_positions]
            if not False in check_if_all_ok:
                passed_candidates.append(candidate)

    return passed_candidates


def create_filter_on_minimum_number_of_digits(minimum_number_of_digits):
    """
    Function creates filter_on_minimum_number_of_digits function are parameterized it with minimum
    number of digits a phone number needs to have.

    :param minimum_number_of_digits: minimum number of digits a phone number needs to have
    :return: function that is used to filter phone number candidates
    """

    def filter_on_minimum_number_of_digits(phone_number_candidates: List[str]) -> List[str]:
        """
        Function checks if phone number candidates has at least minimum allowed number of digits.

     :param phone_number_candidates: list of phone number candidates
     :return: list containing phone number candidates that passed the test
        """
        passed_candidates = []
        for candidate in phone_number_candidates:
            if sum(c.isdigit() for c in candidate) >= minimum_number_of_digits:
                passed_candidates.append(candidate)
        return passed_candidates

    return filter_on_minimum_number_of_digits


def filter_on_candidate_shouldnt_contain_only_numbers(phone_number_candidates: List[str]) -> List[str]:
    """
    Function checks if phone number candidates are not contained only of digits.
    ex. numbers 12345 or 4827328383 will not pass the test
    while +4827328383 or 482-732-8383 will pass the test.

     :param phone_number_candidates: list of phone number candidates
     :return: list containing phone number candidates that passed the test
     """
    passed_candidates = []
    for candidate in phone_number_candidates:
        if not candidate.isnumeric():
            passed_candidates.append(candidate)
    return passed_candidates


def find_occurrences(string:str, match_char:str):
    """
    :param string: string to find positions of letter in
    :param match_char: letter for which to find positions in string
    :return: list of positions on witch match_char is found in a string
    """
    return [index for index, char in enumerate(string) if char == match_char]


class FilterEnum(Enum):
    """
    Enum used to specify different types of filters that can
    be used on phone number candidates.
    """
    NUMER_IS_DATE = 1
    NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR = 2
    MINUS_ONLY_BETWEEN_TWO_NUMBERS = 3
    SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS = 4
    MINIMUM_NUMBER_OF_DIGITS = 5
    NUMBER_SHOULD_CONTAIN_ONLY_NUMBERS = 6


class PhoneNumberExtractor():
    # TODO - za kraj komentiraj kako radi extractor
    """
    Class represents phone number extractor. It gets initialized with BeautifulSoupHtmlWrapper
    which contains html document parsed by BeautifulSoup.
    From BeautifulSoupHtmlWrapper it gets parsed text that doesn't contain any html tags.
    Then it uses NUMBER_MATCHING_REGEX to find all possible
    """

    """
    Maximum length of prefix group captured by NUMBER_MATCHING_REGEX
    """
    PREFIX_LENGTH = '{0,20}'

    """
    Possible lengts inner part of phone number(including non digit sparators).
    Since we are using one digit match before and one after the NUMBER_LENGTH = '{m,n}', 
    Real possible lengths of whole phone numbers are {m+2,n+2}
    """
    NUMBER_LENGTH = '{4,17}'

    """
    Regex used to match possible phone numbers. Regex extracts possible number, its prefix which length is specified
    by PREFIX_LENGTH and its sufix which length is between 0 and 2.
    """
    NUMBER_MATCHING_REGEX = fr'([^+(\d]{PREFIX_LENGTH}(\+\+)?)([+(\d]([\d\(\)\-\s\\/](?!\s\s)){NUMBER_LENGTH}\d)(?=[^\d]|$)(.?.?)'

    """
    Key words that could appear in phone number prefix
    """
    PHONE_NUMBER_KEY_WORDS = ["PHONE", "TEL", "NUMBER", "FAX", "MOBILE"]

    """
    Specifies minimum number of digits a phone number needs to have
    """
    MINIMUM_NUMBER_OF_DIGITS = 6

    def __init__(self, soup_wrapper: BeautifulSoupHtmlWrapper):
        if not isinstance(soup_wrapper, BeautifulSoupHtmlWrapper):
            raise ValueError("Argument is not instance of BeautifulSoupHtmlWrapper")

        self.filters = []
        self.soup_wrapper = soup_wrapper

    # TODO-provijeri jos jednom je li dobto pridruzeno sve u filters
    def add_filter(self, filter_enum: FilterEnum):
        """
        Function registers phone number filter that will be used to filter out
        non phone numbers.

        :param filter_enum: Enum representing the filter
        """
        if filter_enum == FilterEnum.NUMER_IS_DATE:
            self.filters.append(filter_on_number_is_date)
        if filter_enum == FilterEnum.NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR:
            self.filters.append(filter_on_number_contains_maximum_one_parenthesis_pair)
        if filter_enum == FilterEnum.MINUS_ONLY_BETWEEN_TWO_NUMBERS:
            self.filters.append(filter_on_minus_only_between_two_numbers)
        if filter_enum == FilterEnum.SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS:
            self.filters.append(filter_on_slashes_only_between_two_numbers)
        if filter_enum == FilterEnum.MINIMUM_NUMBER_OF_DIGITS:
            self.filters.append(
                create_filter_on_minimum_number_of_digits(minimum_number_of_digits=self.MINIMUM_NUMBER_OF_DIGITS))
        if filter_enum == FilterEnum.NUMBER_SHOULD_CONTAIN_ONLY_NUMBERS:
            self.filters.append(filter_on_candidate_shouldnt_contain_only_numbers)

    def reset_filters(self):
        self.filters = []

    def extractNumbers(self) -> List[str]:
        """
        Entry point of phone number extraction.
        :return: list of extracted phone numbers.
        """
        logging.info("Starting number extractor")
        # Get cleaned html text without html tags
        text = self.soup_wrapper.get_text_no_html_tags()
        candidates_tuple_groups = self.extract_candidate_list(text)

        logging.info("Getting certain phone numbers list")
        certain = self.get_certain_phone_numbers(candidates_tuple_groups)

        logging.info("Applying base filter:" + str(self.basefilter_on_number_prefix_and_sufix))
        candidates_list = self.basefilter_on_number_prefix_and_sufix(candidates_tuple_groups)

        # TODO - log filters being used
        for filter_apply in self.filters:
            logging.info("Applying filter: " + str(filter_apply))
            candidates_list = filter_apply(candidates_list)

        logging.info("Returning phone numbers")
        return certain + candidates_list

    def extract_candidate_list(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Function finds all groups in text that match NUMBER_MATCHING_REGEX.
        Its idea is to extract possible phone number, its prefix and its sufix and does
        three values are returned as tuple (number_prefix, number, number_sufix).

        :param text: string from which to extract vaules
        :return: List of extracted groups, each group represented by tuple (number_prefix, number, number_sufix)
        """
        intermediate_result_set = re.findall(self.NUMBER_MATCHING_REGEX, text)
        # get only prefix, number and sufix groups. Eliminate (\+\+) group at index 1 and lookahead group which is at index 3
        result_set = [(t[0], t[2], t[4]) for t in intermediate_result_set]
        return result_set

    def get_certain_phone_numbers(self, candidates: List[Tuple[str, str, str]]) -> List[str]:
        """
        Function checks prefix of each phone number candidate. If prefix contains one of the
        key words specified by PHONE_NUMBER_KEY_WORDS number is declared as phone number.

        :param candidates: List of phone number candidates. Each candidate represented by tuple (number_prefix, number, number_sufix)
        :return: list of numbers that are declared as phone number.
        """
        certain = []

        for candidate in candidates:
            prefix, number, sufix = candidate[0], candidate[1], candidate[2]
            prefix_to_upper = prefix.upper()
            for key_word in self.PHONE_NUMBER_KEY_WORDS:
                if key_word in prefix_to_upper:
                    certain.append(candidate[1])
                    break

        return certain

    def basefilter_on_number_prefix_and_sufix(self, phone_number_candidates: List[Tuple[str, str, str]]) -> List[str]:
        """
        Base filter applied on phone number candidates.
        Filter checks prefix to see if there is some char immediately before the number in which case number is not a phone numner.
        Filter checks sufix to see if there is nothing after the number, if it is at the end of the sentence ". ", or if it
        is in the sentence sparated by come ", " in which cases number could be a phone number.

        :param phone_number_candidates: List of phone number candidates. Each candidate represented by tuple (number_prefix, number, number_sufix)
        :return: list of candidates that passed the filter
        """
        passed_candidates = []

        for candidate in phone_number_candidates:
            prefix, number, sufix = candidate[0], candidate[1], candidate[2]
            if prefix == "" or prefix.endswith(" "):
                if sufix == "" or sufix.startswith(
                        " ") or sufix == " \n" or sufix == ". " or sufix == "." or sufix == ", " or sufix == ",":
                    passed_candidates.append(number)
        return passed_candidates
