from selenium import webdriver
from story import *
import os
import pickle
import random
import selenium
import time


class Duolingo:
    COOKIE_JAR = "cookies.txt"
    STORIES_URL = "https://stories.duolingo.com/"
    IMPLICIT_WAIT = 2
    def __init__(self):
        self.wd = webdriver.Chrome()
    def __enter__(self):
        self.wd.implicitly_wait(self.IMPLICIT_WAIT)
        self.wd.get(self.STORIES_URL)
        cookies = pickle.load(open(self.COOKIE_JAR, "rb"))
        for cookie in cookies:
            cookie['expiry'] = int(cookie['expiry'])
            print (cookie)
            self.wd.add_cookie(cookie)
        return self
    def __exit__(self, type, value, traceback):
        pickle.dump(self.wd.get_cookies(), open(self.COOKIE_JAR, "wb"))
        self.wd.close()
    def login(self, user, passwd):
        self.wd.get(self.STORIES_URL)
        try:
            login_button = self.wd.find_element_by_css_selector(".login-button")
            login_button.click()
        except selenium.common.exceptions.NoSuchElementException:
            return
        inputs = self.wd.find_elements_by_css_selector(".input-field")
        inputs[0].send_keys(user)
        inputs[1].send_keys(passwd)
        submit = self.wd.find_element_by_css_selector(".submit-button")
        submit.click()
    def get_stories(self):
        sets = self.wd.find_elements_by_css_selector(".set")
        self.story_sets = list(map(StorySet, sets))
        self.stories = sum([s.stories for s in self.story_sets], [])
        return self.stories
    def get_random_story(self):
        return self.stories[0]
        return random.choice([s for s in self.stories if s.is_enabled()])


user = os.getenv('DUOLINGO_USER')
password = os.getenv('DUOLINGO_PASSWORD')
with Duolingo() as D:
    D.login(user, passwd)
    ss = D.get_stories()
    print (ss)
    s = D.get_random_story()
    print (s)
    url = s.go()
    print (url)

    B = BonjourSolution(1,2,3)
    B.run(D.wd)

    time.sleep(5)
