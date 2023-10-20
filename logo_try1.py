from bs4 import BeautifulSoup


def extractLogo(htmlText):
    soup = BeautifulSoup(htmlText, 'html.parser')
    images = soup.find_all('img')
    for item in images:
        str_item = str(item)
        if 'logo' in str_item and item['src'].startswith('https'):
            print(item['src'])
            return

        #img = 'https:' + item['src']
        #if 'logo' in img:
        #    print(img)
