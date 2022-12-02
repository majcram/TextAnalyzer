import requests, re
from bs4 import BeautifulSoup
from collections import Counter
import statistics as stats
import string


import operator
import matplotlib.pyplot as plt; plt.rcdefaults()
class TextAnalyzer:
    def __init__(self, src, src_type='discover'):
        """Keyword arguments:
        src (str) -- text, path to file, or url
        src_type (str) -- The type of input (text, path, url, discover)"""
        if isinstance(src, str) == False or len(src) <= 0:
            raise Exception("Source must be a valid string, filepath or a valid URL")
        self._src = src
        self._src_type = src_type
        self._content = None
        self._orig_content = self.read_file(self._src)
        self.set_values()

    def read_file(fname, mode='r'):
        with open (fname, mode) as f:
            return f.read()

    def set_values(self):
        if self._src.endswith('.txt'):
            self._src_type = 'path'
            #self._content = self._orig_content=self.read_file(self._src)
            self._content = self._orig_content()

        elif self._src.startswith('http'):
            self._src_type = 'url'
            r = requests.get(self._src)
            res = r.content
            self._orig_content = r.text
            self._content = res
        else:
            self._src_type = 'text'
            self._orig_content = self._src
            self._content = self._src

    def set_content_to_tag(self, tag, tag_id=None):
        """Changes _content to the text within a specific element of an HTML document
        Keyword arguments:
            tag (str) Tag to read
            tag_id (str) ID of tag to read
        It’s possible the HTML does not contain the tag being searched. You should use exception handling to catch any errors."""
        soup = BeautifulSoup(self._orig_content, "html.parser")
        content = soup.find('{}'.format(tag),{'id':'{}'.format(tag_id)})
        if content == None:
            raise Exception ("Tag or attribute not exist")
            self._content = content.getText()
            #print(content)

    def reset_content(self):
        """Resets _content to full text. Useful after a call to set_content_to_tag() """
        self._content = self._orig_content

    def _words(self, casesensitive=False):
        """Returns words in _content as list.
        Keyword arguments:
        casesensitive (bool)  If True makes all words uppercase"""
        words = (self._content).strip(string.whitespace + string.punctuation)
        if casesensitive == False:
            words= words.upper()
        return words.split()

    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        w_list= self._words()
        min_max_words = [item for item in w_list if len(item) >= minlen and len(item) <= maxlen]
        com_words= Counter(min_max_words)
        list_com_words= sorted(com_words.items(), key=operator.itemgetter(1), reverse=True)
        return list_com_words[:count]

    def char_distribution(self, casesensitive=False, letters_only=False):
        str_words = ''.join(self._words(casesensitive))
        if letters_only == True:
            str_words = (re.sub('[_\W\d]+', '', str_words))
            char_list = Counter(str_words)
            chars_list= sorted(char_list.items(), key=operator.itemgetter(1), reverse=True)
        return chars_list

    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        w_list= self._words()
        w_list = [word.strip(string.punctuation + string.whitespace) for word in w_list]
        min_max_words = [item for item in w_list if len(item) >= minlen and len(item) <= maxlen]
        com_words= Counter(min_max_words)
        list_com_words= sorted(com_words.items(), key=operator.itemgetter(1),
        reverse=True)
        most_com_words= list_com_words[:count]
        keys1 = []
        values1 = []
        for item in most_com_words:
            keys1.append(item[0])
            values1.append(item[1])
        plt.bar(range(len(keys1)), values1, tick_label=keys1)
        # plt.savefig('bar.png')
        plt.title("Common Words")
        plt.show()

    def plot_char_distribution(self, casesensitive=False, letters_only=False):
        char_dist=self.char_distribution(casesensitive, letters_only)
        keys1 = []
        values1 = []
        for item in char_dist:
            keys1.append(item[0])
            values1.append(item[1])
        plt.bar(range(len(keys1)), values1, tick_label=keys1)
        plt.title("Character Distribution")
        plt.show()

    @property
    def avg_word_length(self):
        "Average word length"
        #words_list = self._words()
        words_list= self._content.split()
        word_len_list=[len(word) for word in words_list]
        length = sum(word_len_list) / len(word_len_list)
        return float('%.2f'%length)

    @property
    def distinct_word_count(self):
        """Number of distinct words in content"""
        dis_words = Counter(self._words())
        return len(dis_words)

    @property
    def positivity(self):
        tally = 0
        words= self._words()
        neg_word_list= self.read_file('negative.txt', 'rb').split()
        neg_word_list = [item.decode('UTF-8') for item in neg_word_list]
        pos_word_list = self.read_file('positive.txt', 'r').split()
        for item in words:
            if item in pos_word_list:
                tally = tally + 1
            return (round(tally / self.word_count * 1000))

            if item in neg_word_list:
                tally = tally - 1
            return (round(tally / self.word_count * 1000))

    @property
    def word_count(self):
        """Number of words in content"""
        return len(self._words())

    @property
    def words(self):
        return self._words()

text = '''The outlook wasn't brilliant for the Mudville Nine that day;
the score stood four to two, with but one inning more to play.
And then when Cooney died at first, and Barrows did the same,
a sickly silence fell upon the patrons of the game.'''
url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
path = "pride-and-prejudice.txt"
fname = "pride-and-prejudice.txt"
ta = TextAnalyzer(fname)











   



