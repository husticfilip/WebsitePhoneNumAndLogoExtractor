from src.extractors.phone.phoneNumberExtractor import PhoneNumberExtractor, FilterEnum
from pathlib import Path
from src.extractors.logo.logoExtractor import LogoExtractor
import logging
import sys
from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper
from utils import print_out_result, open_html
import traceback


# TODO - makni
def readFromTheFile(name):
    return Path("resources/" + name).read_text()


def configure_logs(LOG_LEVEL):
    logging.basicConfig(level=LOG_LEVEL,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        stream=sys.stderr)


def get_user_url_input():
    if len(sys.argv) == 1:
        print("Please provide url to the website as program argument.")
        exit()
    if len(sys.argv) > 2:
        print("Please provide only one program argument which is url to the website.")
        exit()
    else:
        return sys.argv[1]


def get_html():
    logging.info("Opening url " + url)
    try:
        html, status_code = open_html(url)
        if status_code != 200:
            print("Could not open website, got status code " + status_code + ".")
            exit()
        else:
            return html
    except Exception as ex:
        logging.error(ex, exc_info=True)
        print("Could not open website. Please check that url is correct.")
        exit()


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

    url = get_user_url_input()
    html = get_html()
    #html = readFromTheFile("cial.txt")

    try:
        logging.info("Initializing BeautifulSoupHtmlWrapper and parsing html with BeautifulSoup html.parser")
        beautiful_soup_wrapper = BeautifulSoupHtmlWrapper(html)

        numberExtractor = init_phone_number_extractor(beautiful_soup_wrapper)
        numbers = numberExtractor.extractNumbers()

        logoExtractor = LogoExtractor(beautiful_soup_wrapper)
        logo_path = logoExtractor.extract()
        print_out_result(numbers, logo_path, url)
    except Exception as ex:
        print("Problem while running number and logo extractors. Please check out the logs.")
        logging.error("Exception raised while running number and logo extractors")
        logging.error(ex, exc_info=True)
