from bs4 import BeautifulSoup, Tag


#TODO -<img _ngcontent-sc193="" alt="Where can I purchase a particular product?" src="/files/pepsi/documents/1533918762/pepsi-featured-pepsi-0.jpg"/>
#     u https://contact.pepsico.com/files/brands/1531511621/pepsi@2x.png -- dodati https://contact.pepsico.com/ na pocetak


class ImageElementStringWrapper():

    def __init__(self, image: Tag):

        self.image = image
        self.child = str(image['src']).lower() if image.has_attr('src') else ""
        self.current = str(image).lower()
        self.parent = str(image.parent).lower()
        self.is_footer = self.check_if_in_footer(self.parent)

    def check_if_in_footer(self, parent:str):
        if 'foot' in parent.lower():
            return True
        else:
            return False

    # TODO - koristi image da dobis konacni url jer je ostatak u to lower formi
    def format_logo_path(self, url):
        return self.child


def extract_elements_strings(images):
    return [ImageElementStringWrapper(image) for image in images]


class LogoExtractor():

    LOGO_KEY_WORDS = ['logo', 'icon']
    # TODO - stavi exception handler
    def extract(self, html_text, url):
        soup = BeautifulSoup(html_text, 'html.parser')
        images = soup.find_all('img')
        images_wrappers = extract_elements_strings(images)

        for key_word in self.LOGO_KEY_WORDS:
            solution = self.do_the_search_for_a_word(images_wrappers, key_word)
            if solution is not None:
               return solution.format_logo_path(url)

        return ""

    def do_the_search_for_a_word(self, images_wrappers:list[ImageElementStringWrapper], word:str) -> ImageElementStringWrapper:
        best_found = None
        for candidate in images_wrappers:
            if word in candidate.child:
                if candidate.is_footer and best_found is None:
                    best_found = candidate
                else:
                    return candidate

        for candidate in images_wrappers:
            if word in candidate.current:
                if not candidate.is_footer:
                    return candidate

        for candidate in images_wrappers:
            if word in candidate.parent:
                if not candidate.is_footer:
                    return candidate

        return best_found



    def search_for_word_in_elements(self, elements, word):
        candidates = []
        for candidate in elements:
            if word in candidate:
                candidates.append(candidate)
        return candidates






