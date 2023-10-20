from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper, ImageElementStringWrapper


class LogoExtractor():

    LOGO_KEY_WORDS = ['logo', 'icon']

    def __init__(self, soup_wrapper: BeautifulSoupHtmlWrapper):
        self.soup_wrapper = soup_wrapper

    # TODO - stavi exception handler
    def extract(self):
        images = self.soup_wrapper.get_all_img_elements()
        images_wrappers = self.soup_wrapper.init_image_wrappers(images)

        #self.soup_wrapper.find_all('img'))
        #images_wrappers = extract_elements_strings(images)

        for key_word in self.LOGO_KEY_WORDS:
            solution = self.do_the_search_for_a_word(images_wrappers, key_word)
            if solution is not None:
               return solution.child

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