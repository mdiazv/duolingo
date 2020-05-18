import random


class Challenge:
    @staticmethod
    def parse(wd, div):
        cls = div.get_attribute('class').split()
        if 'multiple-choice-challenge' in cls:
            return MultipleChoiceChallenge(wd, div)
        if 'select-phrase-challenge' in cls:
            return SelectPhraseChallenge(wd, div)
        if 'match-challenge' in cls:
            return MatchChallenge(wd, div)
        if 'challenge' in cls:
            div = div.find_element_by_xpath('./div')
            return Challenge.parse(wd, div)
        if 'challenge-question' in cls:
            return QuestionChallenge(wd, div.parent)
        print ("Can't handle challenge: {}".format(cls))
    def solve(self, responses):
        print ('Solving {}'.format(self.question))
        resp = next(responses)
        print ('Response', resp)
        self.respond(resp)
    def respond(self, r):
        for a in self.answers:
            if a.text == r:
                a.select()
                break


class MultipleChoiceChallenge(Challenge):
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.question = div.find_element_by_css_selector('.challenge-question').text
        self.answers = [Answer(wd, d, '.phrases-with-hints') for d in div.find_elements_by_css_selector('.click-to-select')]
    def __repr__(self):
        return 'MultipleChoiceChallenge ({s.question}. {s.answers}'.format(s=self)


class SelectPhraseChallenge(Challenge):
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.question = ''
        self.answers = [Answer(wd, d, '.selectable-token') for d in div.find_elements_by_css_selector('.challenge-answer')]
    def __repr__(self):
        return 'SelectPhraseChallenge ({s.answers}'.format(s=self)


class QuestionChallenge(Challenge):
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.question = div.find_element_by_css_selector('.challenge-question').text
        self.answers = [TapAnswer(wd, d) for d in div.find_elements_by_css_selector('.tappable-phrase')]
    def __repr__(self):
        return 'QuestionChallenge ({s.question}, {s.answers}'.format(s=self)


class MatchChallenge(Challenge):
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.question = div.find_element_by_css_selector('.challenge-question').text
        self.tokens = self.get_tokens()
    def __repr__(self):
        return 'MatchChallenge ({s.question}, {s.tokens}'.format(s=self)
    def get_tokens(self):
        return [TapAnswer(self.wd, d) for d in self.div.find_elements_by_css_selector('.selectable-token')
                if 'match-grade-correct' not in d.get_attribute('class').split()]
    def solve(self, responses):
        print ('Solving {}'.format(self.question))
        matches = next(responses)
        print ('Matches', matches)
        for k, v in matches.items():
            if self.respond(k):
                self.respond(v)
        self.random_guess()
    def random_guess(self):
        tokens = self.get_tokens()
        while tokens:
            a, b = random.sample(tokens, 2)
            print ('Random guess', a.text, b.text)
            a.select()
            b.select()
            tokens = self.get_tokens()
    def respond(self, r):
        for t in self.tokens:
            if t.text.lower() == r.lower() and t.select():
                return True


class Answer:
    def __init__(self, wd, div, cls):
        self.wd = wd
        self.div = div
        self.text = div.find_element_by_css_selector(cls).text
    def __repr__(self):
        return 'Answer ({s.text})'.format(s=self)
    def select(self):
        print ('About to hit {}'.format(self))
        button = self.div.find_element_by_tag_name('button')
        button.click()


class TapAnswer:
    def __init__(self, wd, div):
        self.wd = wd
        self.div = div
        self.text = div.text
    def __repr__(self):
        return 'TapAnswer ({s.text})'.format(s=self)
    def select(self):
        print ('About to hit {}'.format(self))
        cls = self.div.get_attribute('class').split()
        if 'match-selected' not in cls:
            self.div.click()
            return True
