from bs4 import BeautifulSoup, Tag
import logging


class BeautifulSoupHtmlWrapper():
    """
    Class represents BeautifulSoup wrapper where BeautifulSoup is used
    to parse input html text with its html.parser. Latter parsed html
    can be used to access various elements in it.
    """

    def __init__(self, html: str):
        logging.info("Initializing BeautifulSoupHtmlWrapper and parsing html with BeautifulSoup html.parser")
        try:
            self.soup_html_parsed: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        except Exception as ex:
            logging.error("Provided html can not be parsed")
            logging.error(ex, exc_info=True)
            raise ValueError("Provided html can not be parsed")

    def get_text_no_html_tags(self):
        """
        :return: Function returns text of parsed html without its html tags
        """
        text = self.soup_html_parsed.find_all(string=True)
        return " ".join(t.strip() for t in text)

    def get_all_img_elements(self):
        """
        :return: Function returns all img taged elements from parsed html
        """
        return self.soup_html_parsed.find_all('img')

    def init_image_wrappers(self, beautiful_soup_image_elements):
        """
        Function Initilizes List of ImageElementStringWrapper construced of provided beautiful_soup_image_elements
        :param beautiful_soup_image_elements: list of BeautifulSoup image elements.
        :return: list of ImageElementStringWrappers
        """
        return [ImageElementStringWrapper(image) for image in beautiful_soup_image_elements]


class ImageElementStringWrapper():
    """
    Class represents wrapper for BeautifulSoup image element where
    text of image <src> is extracted, text of <img> tag is extracted
    and text of imgage parent <div> is extracted.
    """

    def __init__(self, image: Tag):
        self.image = image
        """
        Child text is text inside <src> tag
        """
        self.child = str(image['src']).lower() if image.has_attr('src') else ""
        """
        Current text is text inside  <img> tag
        """
        self.current = str(image).lower()
        """
        Parent text is text inside image parent <div> tag
        """
        self.parent = str(image.parent).lower()
        """
        Is image in the footer
        """
        self.is_footer = self.check_if_in_footer(self.parent)

    def check_if_in_footer(self, parent: str):
        """
        Function checks if image is in a footer by checking for 'foot' substring
        in image's parent <div> tag
        """
        if 'foot' in parent.lower():
            return True
        else:
            return False
