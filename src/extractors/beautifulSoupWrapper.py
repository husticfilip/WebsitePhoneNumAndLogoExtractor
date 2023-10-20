from bs4 import BeautifulSoup, Tag
from typing import List


class BeautifulSoupHtmlWrapper():

    def __init__(self, html: str):
        self.soup_html_parsed: BeautifulSoup = BeautifulSoup(html, 'html.parser')

    def get_text_no_html_tags(self):
        text = self.soup_html_parsed.find_all(string=True)
        return " ".join(t.strip() for t in text)

    def get_all_img_elements(self):
        return self.soup_html_parsed.find_all('img')

    def init_image_wrappers(self, images):
        return [ImageElementStringWrapper(image) for image in images]


class ImageElementStringWrapper():

    def __init__(self, image: Tag):

        self.image = image
        self.child = str(image['src']).lower() if image.has_attr('src') else ""
        self.current = str(image).lower()
        self.parent = str(image.parent).lower()
        self.is_footer = self.check_if_in_footer(self.parent)

    def check_if_in_footer(self, parent: str):
        if 'foot' in parent.lower():
            return True
        else:
            return False
