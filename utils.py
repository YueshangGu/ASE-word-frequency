import io
import os
from classes import char_counter
from string import ascii_lowercase
from string import ascii_letters
from classes import word_counter
from classes import phrase_counter
from classes import normalizer


def normanize(words, params):
    if isinstance(params.v, str):
        norm = normalizer(params)
        params.v = norm
    else:
        assert isinstance(params.v, normalizer)
    norm = params.v
    return [norm[v] for v in words]


def filter(s):
    legal_character = ascii_letters
    legal_character = legal_character + '0123456789'
    legal_character = legal_character + '\n\r\t '
    for i in range(len(s)):
        if s[i] not in legal_character:
            s = s.replace(s[i], ' ')

    return s


def custom_print(path, name_list, num_list, num=None):  # if len(name_list) < num will cause error
    assert len(name_list) == len(num_list)
    print("File: %s" % (path))
    for i in range(min(len(name_list), num)) if num else range(len(name_list)):
        print("%40s\t%d" % (name_list[i], num_list[i]))
    print('')


def read_preposition(path):
    assert os.path.exists(path)
    preposition_set = set()
    with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
        while True:
            prep = src.readline().strip()
            if prep == '':
                break
            preposition_set.add(prep)
    return preposition_set


def count_char_frequency(path, params):
    assert os.path.exists(path)
    ch_cnt = char_counter()
    all_char = ascii_lowercase

    with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
        lines = src.readlines()
    article = ''.join(lines).lower()
    for c in article:  # reduce some loop time( about 4 ms)
        if c in all_char:  # this will be call frequently, maybe we can count for all char but only summary for char we need
            ch_cnt.char2cnt[c] += 1
            # ch_cnt.update(c)
    # I change here because update() will be called frequently, it will save about 100ms for test_unit1-c
    char, cnt = ch_cnt.cnt2freq()
    if params.n >= 0:
        custom_print(path, char, cnt, params.n)
    else:
        custom_print(path, char, cnt)


def count_word_frequency(path, params):
    assert os.path.exists(path)
    # print(path)
    word_cnt = word_counter()

    word_cnt.stop_word_table(params)
    # print(path)

    with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
        lines = src.readlines()
    for line in lines:
        # words = line.strip().lower().split()
        words = filter(line.strip()).lower().split()
        for word in words:
            word_cnt.update(word)
    words, cnt = word_cnt.cnt2freq()
    if params.n >= 0:
        custom_print(path, words, cnt, params.n)
    else:
        custom_print(path, words, cnt)


def operate_in_dir(params, dir):
    # dir = params.d
    if params.s:
        recursive = True
    else:
        recursive = False
    list_dir = os.listdir(dir)
    for f in list_dir:
        f = os.path.join(dir, f)
        if os.path.isdir(f) and recursive:
            operate_in_dir(params, f)
        elif not os.path.isdir(f):
            if params.p > 0:
                count_phrase_frequency(f, params)
            elif params.c:
                count_char_frequency(f, params)
            elif params.p == -1 and (params.f or params.d or params.s):  # debug for regression test -d -s -n 5 data
                count_word_frequency(f, params)


def output_phrase_from_sentence(sen, params, phrase_cnt):
    phrase_len = params.p
    words = sen.strip().split()
    words = phrase_cnt.remove_stop_words(words)
    if params.v:
        words = normanize(words, params)
    if len(words) < phrase_len:
        return
    phrase_num = len(words) - phrase_len + 1
    for i in range(phrase_num):
        phrase_cnt.update(' '.join(words[i: i + phrase_len]))


def count_phrase_frequency(path, params):
    assert os.path.exists(path)
    phrase_cnt = phrase_counter()
    if params.x:
        phrase_cnt.stop_word_table(params)
    with io.open(path, 'r', newline='\n', errors='ignore', encoding='utf8') as src:
        lines = src.readlines()
    article = ''.join(lines).lower()

    legal_character = ascii_letters
    legal_character = legal_character + '0123456789'
    legal_character = legal_character + '\n\r\t '

    ptr = 0
    total_len = len(article)
    while True:
        line = ''
        if ptr >= total_len:
            break
        while article[ptr] in legal_character:
            line += article[ptr]
            ptr += 1
            if ptr >= total_len:
                break
        output_phrase_from_sentence(line, params, phrase_cnt)
        ptr += 1

    phrases, cnts = phrase_cnt.cnt2frq()

    if params.n >= 0:
        custom_print(path, phrases, cnts, params.n)
    else:
        custom_print(path, phrases, cnts)
