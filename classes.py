from string import ascii_lowercase
import os
import io


def read_verb(path):
    assert os.path.exists(path)
    verb_dict = dict()
    with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
        while True:
            line = src.readline().strip()
            if line == '':
                break
            origin, words = line.split('->')
            origin = origin.strip()
            words = [word.strip() for word in words.split(',')]
            for word in words:
                verb_dict[word] = origin
    return verb_dict


class char_counter(object):

    def __init__(self):
        def get_cnt_dict():
            a = dict()
            for char in ascii_lowercase:
                a[char] = 0
            return a

        self.char2cnt = get_cnt_dict()
        assert len(self.char2cnt) == 26
        self.total_cnt = 0

    def update(self, char):
        self.char2cnt[char] += 1

    def cnt2freq(self):
        char = [k for k in self.char2cnt.keys()]
        cnt = [v for v in self.char2cnt.values()]
        # self.total_cnt = sum(cnt)
        index = sorted(range(len(cnt)), key=cnt.__getitem__, reverse=True)
        char = [char[i] for i in index]
        cnt = [cnt[i]  for i in index]
        return (char, cnt)


class word_counter(object):

    def __init__(self):
        self.word2cnt = dict()
        self.total_cnt = 0
        self.stop_words = None

    def update(self, word):
        if (self.stop_words and word not in self.stop_words) or not self.stop_words:
            if word in self.word2cnt:
                self.word2cnt[word] += 1
            else:
                self.word2cnt[word] = 1

    def cnt2freq(self):
        words = [k for k in self.word2cnt.keys()]
        cnt = [v for v in self.word2cnt.values()]
        # self.total_cnt = sum(cnt)
        # index = sorted(range(len(cnt)),key=cnt.__getitem__, reverse=True)
        index = sorted(range(len(cnt)), key=lambda i: (-cnt[i], words[i]))
        words = [words[i] for i in index]
        cnt = [cnt[i]  for i in index]
        return (words, cnt)

    def stop_word_table(self, params):
        if params.x:
            path = params.x
            assert os.path.exists(path)
            stop_words = set()
            with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
                words = src.readlines()
            self.stop_words = set([x.strip() for x in words])


class phrase_counter(object):

    def __init__(self):
        self.phrase2cnt = dict()
        self.total_cnt = 0
        self.stop_words = None

    def update(self, phrase):
        if phrase in self.phrase2cnt:
            self.phrase2cnt[phrase] += 1
        else:
            self.phrase2cnt[phrase] = 1

    def cnt2frq(self):
        phrases = [k for k in self.phrase2cnt.keys()]
        cnts = [v for v in self.phrase2cnt.values()]
        # self.total_cnt = sum(cnts)
        index = sorted(range(len(cnts)), key=lambda i: (-cnts[i], phrases[i]))
        phrases = [phrases[i] for i in index]
        cnts = [cnts[i]  for i in index]
        return phrases, cnts

    def stop_word_table(self, params):
        if params.x:
            path = params.x
            assert os.path.exists(path)
            stop_words = set()
            with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
                words = src.readlines()
            self.stop_words = set([x.strip() for x in words])

    def remove_stop_words(self, words):
        if self.stop_words:
            return [x for x in words if x not in self.stop_words]
        else:
            return words


class normalizer(object):

    def __init__(self, params):
        self.params = params
        self.verbfile = params.v
        self.verb_dict = read_verb(self.verbfile)

    def __getitem__(self, item):
        if item in self.verb_dict:
            return self.verb_dict[item]
        else:
            return item
