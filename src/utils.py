import re
import copy
import requests
from urllib.parse import urlparse
import logging

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': 'https://www.google.com/'}


def add_host_to_headers(url: str):
    new_headers = copy.copy(headers)
    host = urlparse(url).netloc

    if not host.startswith("www."):
        host = "www." + host
    new_headers["Host"] = host
    return new_headers

def open_html(url: str):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.info("Couldn't access website, adding 'Host' to the header")
        new_headers = add_host_to_headers(url)
        response = requests.get(url, headers=new_headers)

    print(response.headers)
    return response.text, response.status_code

def format_logo_path(logo_path: str, url: str):
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
    if len(phone_numbers) == 0:
        return None
    phone_numbers_set = set()
    for number in phone_numbers:
        phone_numbers_set.add(re.sub("[^\d+\(\)]", " ", number.strip()))
    return phone_numbers_set


def print_out_result(phone_numbers, logo_path, url):
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
