from src.extractors.phone.phoneNumberExtractor import PhoneNumberExtractor, FilterEnum
import requests
from pathlib import Path
from src.extractors.logo.logoExtractor import LogoExtractor
import logging
import sys
from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': '*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://www.google.com/'}


# TODO - make checks if request passed, check if url is valid
def get_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Error reading html")


# TODO - makni
def readFromTheFile(name):
    return Path("resources/" + name).read_text()


def format_phone_numbers(phone_numbers: list[str]):
    phone_numbers_set = set()
    for number in phone_numbers:
        phone_numbers_set.add(re.sub("[^\d+\(\)]"," ", number.strip()))
    return phone_numbers_set


def configure_logs(LOG_LEVEL):
    logging.basicConfig(level=LOG_LEVEL,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        stream=sys.stderr)

def init_phone_number_extractor(beautiful_soup_wrapper):
    numberExtractor = PhoneNumberExtractor(beautiful_soup_wrapper)
    numberExtractor.add_filter(FilterEnum.MINIMUM_NUMBER_OF_DIGITS)
    numberExtractor.add_filter(FilterEnum.NUMBER_SHOULD_CONTAIN_ONLY_NUMBERS)
    numberExtractor.add_filter(FilterEnum.NUMER_IS_DATE)
    numberExtractor.add_filter(FilterEnum.MINUS_ONLY_BETWEEN_TWO_NUMBERS)
    numberExtractor.add_filter(FilterEnum.SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS)
    numberExtractor.add_filter(FilterEnum.NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR)
    return numberExtractor


if __name__ == '__main__':
    LOG_LEVEL = logging.INFO
    configure_logs(LOG_LEVEL)

    # html = get_html("https://www.cmsenergy.com/contact-us/default.aspx")
    html = readFromTheFile("phosagro.txt")
    html = "aaaaa"
    beautiful_soup_wrapper = BeautifulSoupHtmlWrapper(html)

    numberExtractor = init_phone_number_extractor(beautiful_soup_wrapper)
    logoExtractor = LogoExtractor(beautiful_soup_wrapper)

    numbers = numberExtractor.extractNumbers()
    print(numbers)
    numbers = format_phone_numbers(numbers)
    print(numbers)

    logo = logoExtractor.extract()
    print(logo)
