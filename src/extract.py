from src.extractors.phone.phoneNumberExtractor import NumberExtractor, FilterEnum
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from src.extractors.logo.logoExtractor import LogoExtractor

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
 'Accept-Language': '*',
 'Accept-Encoding': 'gzip, deflate, br',
 'Referer': 'https://www.google.com/'}

# TODO - make checks if request passed
def get_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Error reading html")

def remove_html_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Finding the text:
    text = soup.findAll(string=True)
    return " ".join(t.strip() for t in text)


def readFromTheFile(name):
    return Path("resources/" + name).read_text()

if __name__ == '__main__':
    url = "https://www.fer.unizg.hr/"

    numberExtractor = NumberExtractor()
    numberExtractor.add_filter(FilterEnum.MINIMUM_NUMBER_OF_DIGITS)
    numberExtractor.add_filter(FilterEnum.NUMER_IS_DATE)
    numberExtractor.add_filter(FilterEnum.MINUS_ONLY_BETWEEN_TWO_NUMBERS)
    numberExtractor.add_filter(FilterEnum.SLASHES_AND_BACKSLASHES_ONLY_BETWEEN_TWO_NUMBERS)
    numberExtractor.add_filter(FilterEnum.NUMBER_CONTAINS_ONLY_ONE_PARANTHASIS_PAIR)

    logoExtractor = LogoExtractor()

    #html = get_html("https://www.cmsenergy.com/contact-us/default.aspx")
    html = readFromTheFile("phosagro.txt")
    cleaned_text = remove_html_tags(html)
    numbers = numberExtractor.extractNumbers(cleaned_text)
    print(numbers)

    logo = logoExtractor.extract(html, url)
    print(logo)

