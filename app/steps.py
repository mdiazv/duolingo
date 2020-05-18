from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from challenges import *


class Step:
    WAIT = 5
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.text = div.text
    def __repr__(self):
        return 'Step ({s.text})'.format(s=self)
    def hit_continue(self, timeout=None):
        if timeout is None:
            timeout = self.WAIT
        wait = WebDriverWait(self.wd, timeout, poll_frequency=0.5)
        try:
            wait.until(lambda wd: 
                wd.find_element_by_css_selector('.continue').is_enabled())
        except TimeoutException:
            pass
        if self.wd.find_element_by_css_selector('.continue').is_enabled():
            self.wd.find_element_by_css_selector('.continue').click()
    @staticmethod
    def parse(wd, s, cls):
        if 'line' in cls:
            return LineStep(wd, s)
        if 'challenge-container' in cls:
            return ChallengeStep(wd, s)
        if 'challenge-question' in cls:
            return ChallengeQuestionStep(wd, s)
        print ("Can't handle step: {}".format(cls))


class LineStep(Step):
    WAIT = 2
    def __repr__(self):
        return 'LineStep ({s.text})'.format(s=self)
    def solve(self, _):
        print (self)
        spans = self.div.find_elements_by_css_selector('.phrase span')
        for span in spans:
            print ('waiting on:', span.text)
            wait = WebDriverWait(self.wd, self.WAIT, poll_frequency=0.1)
            wait.until(lambda wd: 'highlighted' in span.get_attribute('class').split())
        self.hit_continue(timeout=1)


class ChallengeQuestionStep(Step):
    def __repr__(self):
        return 'ChallengeQuestionStep ({s.text})'.format(s=self)
    def solve(self, _):
        print (self)


class ChallengeStep(Step):
    def __repr__(self):
        return 'ChallengeStep ({s.text})'.format(s=self)
    def solve(self, responses):
        print (self)
        print ('ChallengeStep', self.div.get_attribute('class'))
        divs = self.div.find_elements_by_xpath('./*')
        for d in divs:
            print (d.tag_name, d.text)
        div = self.div.find_element_by_xpath('./div')
        c = Challenge.parse(self.wd, div)
        print (c)
        c.solve(responses)
        self.hit_continue()
