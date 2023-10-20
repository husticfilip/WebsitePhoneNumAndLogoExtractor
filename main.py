import requests
from pathlib import Path
from bs4 import BeautifulSoup
from try1 import replaceAllNonDigitsPlusesAndParenthesis, getPhoneNumers, cleanText
from logo_try1 import extractLogo



def extractPlainText(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Finding the text:
    scripts = soup.find_all("script")
    print(scripts)
    return ""

def adhoctest():
    text = ("        +1 408 235 7700    \n"
            ""
            ""
            "   +1 408 235 7737      ")
    cleaned = replaceAllNonDigitsPlusesAndParenthesis(text)
    res = getPhoneNumers(cleaned)

def writeToTheFile(url, name):
    response = requests.get(url)

    with open("resources/"+name, "w") as text_file:
        text_file.write(response.text)

def readFromTheFile(name):
    return Path("resources/"+name).read_text()


if __name__ == '__main__':
    #writeToTheFile("https://www.zaba.hr/home/en", "zaba.txt")
    input_html = readFromTheFile("phosagro.txt")
    extractPlainText(input_html)
    #getPhoneNumers(input_html)
    # TODO - ako se ispostavi da se do nekih stranica ne moze doci baci exception
   #input_html = requests.get('https://www.phosagro.com/contacts/').content.decode('UTF-8')
   #cleaned = replaceAllNonDigitsPlusesAndParenthesis(input_html)
   #res = getPhoneNumers(cleaned)

