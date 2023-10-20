from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Comment
import re

def readFromTheFile(name):
    return Path("resources/"+name).read_text()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def getPhoneNumers(text):
    #cleaned_list = re.findall(r'[\+0-9].+?(?=(?:\s\s|\s$|$))', text)
    # nalazi sve brojeve koji imaju i ( ) - \s i cijeli string je dugacak od 5-17 TODO razmisli o vrijednostima
    #cleaned_list = re.findall(r'[+\d][\d\(\)\-\s]{5,17}(?=[^\d])', text)
    cleaned_list = re.findall(r'((tel)?.?[+\d][\d\(\)\-\s]{5,17}\d(?=[^\d]).?)', text)
    cleaned_list = [t[0] for t in cleaned_list  ]

    passed_candidates = filterWrongCharacterAtBegginigOrEnd(cleaned_list)
    print(cleaned_list)

def filterWrongCharacterAtBegginigOrEnd(candidates):
    passed_candidates = []

    for candidate in candidates:
        # pocetak treba biti pored praznog polja ili pocetka > html zagrade ili pak ako je broj na samom pocetku reda onda pocetak moze biti i + ili broj
        if candidate[0] == " " or candidate[0] == "+" or candidate[0].isnumeric():
            # kraj treba biti pored praznog polja ili kraja < html zagrade ili ako je na samom kraju reda moze biti i broj
            if candidate[-1] == " " or candidate[-1].isnumeric():
                passed_candidates.append(candidate)

    return passed_candidates


def extractPlainText(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Finding the text:
    scripts = soup.find_all("script")
    text = soup.findAll(text=True)

    connectText = u" ".join(t.strip() for t in text)

    getPhoneNumers(connectText)

    return ""


if __name__ == '__main__':
    #writeToTheFile("https://www.zaba.hr/home/en", "zaba.txt")
    input_html = readFromTheFile("phosagro.txt")
    extractPlainText(input_html)
