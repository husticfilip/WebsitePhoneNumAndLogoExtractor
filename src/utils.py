import re
import copy
import requests
from urllib.parse import urlparse
import logging

"""
Header used to send http requests
"""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': 'https://www.google.com/'}


def add_host_to_headers(url: str):
    """
    Function ads 'Host' parameter to the headers. Assigned
    value to the 'Host'  parameter will be website domain.

    :param url: url to the website
    :return: headers expanded with 'Host' parameter
    """
    new_headers = copy.copy(headers)
    host = urlparse(url).netloc

    if not host.startswith("www."):
        host = "www." + host
    new_headers["Host"] = host
    return new_headers


def open_html(url: str):
    """
    Function tries to make GET request to the website specified by url.
    If url doens't point to valid website exception will be thrown.

    :param url: url to the website
    :return: text content of the response, status code of the response
    """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.info("Couldn't access website, adding 'Host' to the header")
        new_headers = add_host_to_headers(url)
        response = requests.get(url, headers=new_headers)

    return response.text, response.status_code


def format_logo_path(logo_path: str, url: str):
    """
    Function formats logo path for the output.
    If logo path is a link to some web location(it starts with http) it is not formated.
    If not it is concatenated with the website url.

    :param logo_path: extracted logo path
    :param url: url to the website
    :return: formated logo path
    """
    if logo_path == "":
        return logo_path
    if logo_path.startswith("http"):
        return logo_path
    else:
        url = re.sub(r'\\', '/', url)
        logo_path = re.sub(r'\\', '/', logo_path)

        if url.endswith("/") and logo_path.startswith("/"):
            return url + logo_path[1:]
        elif not url.endswith("/") and not logo_path.startswith("/"):
            return url + "/" + logo_path
        else:
            return url + logo_path


def format_phone_numbers(phone_numbers: list[str]):
    """
    Function formats numbers for the output. All chars except
    numbers, + and parenthesis are removed.
    Also, function eliminates duplicate phone numbers

    :param phone_numbers: list of phone numbers to format
    :return: set of unique and formated numbers
    """
    if len(phone_numbers) == 0:
        return None
    phone_numbers_set = set()
    for number in phone_numbers:
        phone_numbers_set.add(re.sub("[^\d+\(\)]", " ", number.strip()))
    return phone_numbers_set


def print_out_result(phone_numbers, logo_path, url):
    """
    Function formats and prints out found phone numbers and logo path.
    """
    formated_numbers = format_phone_numbers(phone_numbers)
    formated_logo_path = format_logo_path(logo_path, url)

    if formated_numbers is None:
        print("None")
    else:
        result_string = ""
        for number in formated_numbers:
            result_string += number + ", "
        result_string = result_string[0:-2]
        print(result_string)

    if formated_logo_path == "":
        print("None")
    else:
        print(formated_logo_path)
