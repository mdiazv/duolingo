from selenium.webdriver.support.wait import WebDriverWait
from steps import *
import time


class Story:
    """
    Story <class 'selenium.webdriver.remote.webelement.WebElement'> ['clear', 'click', 'find_element', 'find_element_by_class_name', 'find_element_by_css_selector', 'find_element_by_id', 'find_element_by_link_text', 'find_element_by_name', 'find_element_by_partial_link_text', 'find_element_by_tag_name', 'find_element_by_xpath', 'find_elements', 'find_elements_by_class_name', 'find_elements_by_css_selector', 'find_elements_by_id', 'find_elements_by_link_text', 'find_elements_by_name', 'find_elements_by_partial_link_text', 'find_elements_by_tag_name', 'find_elements_by_xpath', 'get_attribute', 'get_property', 'id', 'is_displayed', 'is_enabled', 'is_selected', 'location', 'location_once_scrolled_into_view', 'parent', 'rect', 'screenshot', 'screenshot_as_base64', 'screenshot_as_png', 'send_keys', 'size', 'submit', 'tag_name', 'text', 'value_of_css_property']
    """
    def __init__(self, div):
        self.div = div
        self.story = div
        self.url = self.story.get_property('href')
        self.title = div.find_element_by_css_selector('.title').text
        self.button = div.find_element_by_css_selector('.story-cover-illustration-button')
    def __repr__(self):
        return 'Story ({s.title}, {s.url})'.format(s=self)
    def is_enabled(self):
        return self.url is not None
    def go(self):
        self.button.click()
        return self.url


class StorySet:
    def __init__(self, div):
        self.div = div
        self.title = div.find_element_by_css_selector('.set-header').text
        stories = div.find_elements_by_css_selector('.story')
        self.stories = list(map(Story, stories))
    def __repr__(self):
        stories = '\n - '.join(map(str, self.stories))
        return 'StorySet ({s.title}, {stories})'.format(s=self, stories=stories)


class StorySolution:
    def __init__(self, url, keywords, tasks):
        self.url = url
        self.keywords = keywords
        self.tasks = tasks
    def run(self, wd):
        transcription = wd.find_element_by_css_selector('.transcription')
        steps = transcription.find_elements_by_xpath('./div')
        responses = iter(self.responses)
        for i, s in enumerate(steps):
            cls  = s.get_attribute('class').split()
            step = Step.parse(wd, s, cls)
            step.solve(responses)


class BonjourSolution(StorySolution):
    responses = [
        "My darling.",
        "examen d'anglais",
        "fatiguée",
        "She put sugar in her cup of coffee.",
        "What?",
        "… put salt in her coffee instead of sugar.",
        {'avec': 'with', 'es': 'are', 'salut': 'hi', 'de': 'of', 'est': 'is',
    #     'je': 'i', 'du sel': 'salt', 'fatiguée': 'tired', 'livre': 'book',
    #     'mon': 'my', 'la': 'the', 'son': 'her', 'voilà': 'here it is', 'suis': 'am',
    #     'très': 'very', 'veut': 'want', 'femme': 'wife', 'beaucoup': 'a lot',
    #     'beurk': 'yuck', "l'université": 'the university', 'table': 'table',
    #     "examen d'anglais": 'english test', 'tasse': 'cup', 'oui': 'yes',
    #     'café': 'coffee', "c'est": "it's", 'merci': 'thank you', 'boit': 'drinks',
    #     'elle': 'she', 'bonjour !': 'good morning', 'sur': 'on', 'travaille': 'work',
    #     'à la maison': 'at home', 'où': 'where', 'un': 'an', "j'ai": 'i have',
         'tu': 'you', 'dans': 'in', 'à': 'at', "livre d'anglais": 'english book',
         'quoi': 'what', 'chéri': 'darling', 'du sucre': 'some sugar', 'veux': 'want'},
    ]
