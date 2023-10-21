from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper, ImageElementStringWrapper
import logging


class LogoExtractor():
    # TODO - explain how it works
    """
    Class extracts phone numbers
    """

    """
    Key words with which we can recognize logo in html.
    """
    LOGO_KEY_WORDS = ['logo', 'icon']

    def __init__(self, soup_wrapper: BeautifulSoupHtmlWrapper):
        if not isinstance(soup_wrapper, BeautifulSoupHtmlWrapper):
            raise ValueError("Argument is not instance of BeautifulSoupHtmlWrapper")
        self.soup_wrapper = soup_wrapper

    # TODO - stavi exception handler
    def extract(self):
        """
        Entry point to logo extract

        :return: path to logo image or empty string if logo is not found
        """
        logging.info("Starting logo extractor")
        # get all <img> elements from BeautifulSoup and extract text in <src>, <img> and <div> tags
        # (<div... <img... <src... src> img> div>) wraped in images_wrappers
        images = self.soup_wrapper.get_all_img_elements()
        images_wrappers = self.soup_wrapper.init_image_wrappers(images)

        # do search for key words in priority order
        for key_word in self.LOGO_KEY_WORDS:
            solution = self.do_the_search_for_a_word(images_wrappers, key_word)
            if solution is not None:
                logging.info("Returning found logo path" + solution.child)
                return solution.child

        logging.info("Logo path not found")
        return ""

    def do_the_search_for_a_word(self, images_wrappers: list[ImageElementStringWrapper],
                                 key_word: str) -> ImageElementStringWrapper:
        """
        Function loop through images_wrappers three times.

        First time it looks at images_wrappers child element which is text inside <src> element.
        If it finds key_word is part of text and images_wrapper doesn't represent footer element
        it returns it as a solution. If it is footer it saves it as best found solution so far.

        Next with same process it looks at the images_wrappers current element which is a text inside of <img> element.
        And lastly it looks at the images_wrappers parent element which is a text inside of <div> element.

        If there is no logo found outside of footer, footer logo is returned.
        If there is no logo at all None is retunred


        :param images_wrappers: list of images wrappers
        :param key_word: key word which indicates element is the logo
        :return: path to logo or None if logo is not found
        """
        best_found = None
        for candidate in images_wrappers:
            if key_word in candidate.child:
                if candidate.is_footer and best_found is None:
                    best_found = candidate
                else:
                    return candidate

        for candidate in images_wrappers:
            if key_word in candidate.current:
                if candidate.is_footer and best_found is None:
                    best_found = candidate
                else:
                    return candidate

        for candidate in images_wrappers:
            if key_word in candidate.parent:
                if candidate.is_footer and best_found is None:
                    best_found = candidate
                else:
                    return candidate

        return best_found
