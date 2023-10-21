import unittest
from src.extractors.logo.logoExtractor import LogoExtractor
from src.extractors.beautifulSoupWrapper import BeautifulSoupHtmlWrapper




class Do_the_search_for_a_word_test(unittest.TestCase):

    def setUp(self):
        self.logo_extractor = LogoExtractor(BeautifulSoupHtmlWrapper(""))

    def test_logo_in_src(self):
        candidates = [DummyImageElementStringWrapper("random","random", "random"),
                      DummyImageElementStringWrapper("random","random", "random"),
                      DummyImageElementStringWrapper("src/logo_name.png","random", "random")]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/logo_name.png", logo_path.child)

    def test_logo_in_img(self):
        candidates = [DummyImageElementStringWrapper("random","random", "random"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "this is logo", "random"),
                      DummyImageElementStringWrapper("random","random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/no_mention_in_src.png", logo_path.child)

    def test_logo_in_parent(self):
        candidates = [DummyImageElementStringWrapper("random","random", "random"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", "this is logo"),
                      DummyImageElementStringWrapper("random","random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/no_mention_in_src.png", logo_path.child)

    def test_logo_in_src_but_footer(self):
        candidates = [DummyImageElementStringWrapper("random", "random", "random"),
                      DummyImageElementStringWrapper("random", "random", "random"),
                      DummyImageElementStringWrapper("src/logo_name.png", "random", "footer")]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/logo_name.png", logo_path.child)

    def test_logo_in_img_but_also_in_footer(self):
        candidates = [DummyImageElementStringWrapper("logo.png", "random", "footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "this is logo", ""),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/no_mention_in_src.png", logo_path.child)

    def test_logo_in_parent_but_also_in_footer(self):
        candidates = [DummyImageElementStringWrapper("logo.png", "random", "footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", "this is logo"),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/no_mention_in_src.png", logo_path.child)

    def test_logo_in_parent_but_also_in_footer_2(self):
        candidates = [DummyImageElementStringWrapper("", "logo.png", "footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", "this is logo"),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("src/no_mention_in_src.png", logo_path.child)

    def test_src_only_footer(self):
        candidates = [DummyImageElementStringWrapper("logo.png", "", "footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", ""),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("logo.png", logo_path.child)

    def test_img_only_footer(self):
        candidates = [DummyImageElementStringWrapper("a.png", "logo.png", "footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", ""),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual("a.png", logo_path.child)

    def test_parent_and_footer(self):
        candidates = [DummyImageElementStringWrapper("a.png", "", " "),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", ""),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual(None, logo_path)

        candidates = [DummyImageElementStringWrapper("a.png", "", " footer"),
                      DummyImageElementStringWrapper("src/no_mention_in_src.png", "", ""),
                      DummyImageElementStringWrapper("random", "random", "random")
                      ]

        logo_path = self.logo_extractor.do_the_search_for_a_word(candidates, key_word="logo")
        self.assertEqual(None, logo_path)


class DummyImageElementStringWrapper():
    def __init__(self, child, current, parent  ):
        self.child = child
        self.current = current
        self.parent = parent
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