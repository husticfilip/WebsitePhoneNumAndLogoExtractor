from typing import List, Tuple
import re
from enum import Enum

POSSIBLE_DATE_FORMAT_REGEXS = [r'^\d\d\d\d(-\d\d){1,2}$',
                               r'^\d\d\d\d( \d\d){1,2}$',
                               r'^\d\d\d\d(\\\d\d){1,2}$',
                               r'^\d\d\d\d(/\d\d){1,2}$',

                               r'^(\d\d-){1,2}\d\d\d\d$',
                               r'^(\d\d ){1,2}\d\d\d\d$',
                               r'^(\d\d\\){1,2}\d\d\d\d$',
                               r'^(\d\d/){1,2}\d\d\d\d$']


# TODO -testiaj  jos
# u illionu imaju datovi tipa 10/24/2022 2023 27'
def filter_on_number_is_date(phone_number_candidates: List[str]) -> List[str]:
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


def filter_on_number_contains_only_one_parenthesis_pair(phone_number_candidates: List[str]) -> List[str]:
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
    return filter_on_char_only_between_two_numbers(phone_number_candidates, "-")


# Pripazi na "\\" i '\'
def filter_on_slashes_only_between_two_numbers(phone_number_candidates: List[str]) -> List[str]:
    passed = filter_on_char_only_between_two_numbers(phone_number_candidates, "\\")
    return filter_on_char_only_between_two_numbers(passed, "/")


def filter_on_char_only_between_two_numbers(phone_number_candidates: List[str], char: str) -> List[str]:
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
    def filter_on_minimum_number_of_digits(phone_number_candidates: List[str]) -> List[str]:
        passed_candidates = []
        for candidate in phone_number_candidates:
            if sum(c.isdigit() for c in candidate) >= minimum_number_of_digits:
                passed_candidates.append(candidate)
        return passed_candidates

    return filter_on_minimum_number_of_digits


def filter_on_candidate_shouldnt_contain_only_numbers(phone_number_candidates: List[str]) -> List[str]:
    passed_candidates = []
    for candidate in phone_number_candidates:
        if not candidate.isnumeric():
            passed_candidates.append(candidate)
    return passed_candidates


def find_occurrences(string, match_char):
    return [index for index, char in enumerate(string) if char == match_char]



class FilterEnum(Enum):
    NUMER_IS_DATE = 1
    NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR = 2
    MINUS_ONLY_BETWEEN_TWO_NUMBERS = 3
    SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS = 4
    MINIMUM_NUMBER_OF_DIGITS = 5
    NUMBER_SHOULD_CONTAIN_ONLY_NUMBERS = 6



class NumberExtractor():
    # NUMBER_MATCHING_REGEX_WITH_TEL = r'((tel:)\s?[+(\d][\d\(\)\-\s]{5,17}\d)'
    # pokupi sve sto je u " "
    # NUMBER_MATCHING_REGEX_WITH_PREFIX = r'.{4,20}["\']\s?[+(\d][\d\(\)\-\s]{5,17}\d\s?["\']'

    PHONE_NUMBER_KEY_WORDS = ["PHONE", "TEL", "NUMBER", "FAX", "MOBILE"]

    # NUMBER_MATCHING_REGEX = r'([^\d+(]{0,20})([+(\d]([\d\(\)\-\s\\/](?!\s\s)){5,17}\d)(?=[^\d]|\n|$)(.?.?)'
    PREFIX_LENGTH = '{0,20}'
    NUMBER_LENGTH = '{4,17}'
    NUMBER_MATCHING_REGEX = fr'([^+(\d]{PREFIX_LENGTH}(\+\+)?)([+(\d]([\d\(\)\-\s\\/](?!\s\s)){NUMBER_LENGTH}\d)(?=[^\d]|$)(.?.?)'

    MINIMUM_NUMBER_OF_DIGITS = 6
    def __init__(self):
        self.filters = []

    # TODO-provijeri jos jednom je li dobto pridruzeno sve u filters
    def add_filter(self, filter_enum: FilterEnum):
        if filter_enum == FilterEnum.NUMER_IS_DATE:
            self.filters.append(filter_on_number_is_date)
        if filter_enum == FilterEnum.NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR:
            self.filters.append(filter_on_number_contains_only_one_parenthesis_pair)
        if filter_enum == FilterEnum.MINUS_ONLY_BETWEEN_TWO_NUMBERS:
            self.filters.append(filter_on_minus_only_between_two_numbers)
        if filter_enum == FilterEnum.SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS:
            self.filters.append(filter_on_slashes_only_between_two_numbers)
        if filter_enum == FilterEnum.MINIMUM_NUMBER_OF_DIGITS:
            self.filters.append(create_filter_on_minimum_number_of_digits(minimum_number_of_digits=self.MINIMUM_NUMBER_OF_DIGITS))
        if filter_enum == FilterEnum.NUMBER_SHOULD_CONTAIN_ONLY_NUMBERS:
            self.filters.append(filter_on_candidate_shouldnt_contain_only_numbers)

    def reset_filters(self):
        self.filters = []

    def extractNumbers(self, text) -> List[str]:
        candidates_tuple_groups = self.extract_candidate_list(text)
        certain = self.get_certain_phone_numbers(candidates_tuple_groups)
        candidates_list = self.basefilter_on_number_prefix_and_sufix(candidates_tuple_groups)

        # TODO - log filters being used
        for filter_apply in self.filters:
            candidates_list = filter_apply(candidates_list)

        return certain + candidates_list

    def extract_candidate_list(self, text: str) -> List[Tuple[str, str, str]]:
        intermediate_result_set = re.findall(self.NUMBER_MATCHING_REGEX, text)
        # get only prefix, number and sufix groups. Eliminate (\+\+) group at index 1 and lookahead group which is at index 3
        result_set = [(t[0], t[2], t[4]) for t in intermediate_result_set]
        return result_set

    def get_certain_phone_numbers(self, candidates: List[Tuple[str, str, str]]) -> List[str]:
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
        passed_candidates = []

        for candidate in phone_number_candidates:
            prefix, number, sufix = candidate[0], candidate[1], candidate[2]
            if prefix == "" or prefix.endswith(" "):
                if sufix == "" or sufix.startswith(
                        " ") or sufix == " \n" or sufix == ". " or sufix == "." or sufix == ", " or sufix == ",":
                    passed_candidates.append(number)
        return passed_candidates
