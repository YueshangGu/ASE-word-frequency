import argparse
from utils import count_char_frequency
from utils import count_word_frequency
from utils import count_phrase_frequency
import sys
from utils import operate_in_dir


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default='', help='output character frequencies')
    parser.add_argument('-f', type=str, default='', help='output word frequencies')
    parser.add_argument('-p', type=int, default=-1, help='output phrase frequencies')
    parser.add_argument('-d', type=str, default='', help='treat the string as a directory')
    parser.add_argument('-s', type=str, default='', help='recurse into sub_dir')
    parser.add_argument('-n', type=int, default=-1, help='output the first n items')
    parser.add_argument('-x', type=str, default='', help='stop words')
    parser.add_argument('-v', type=str, default='', help='verb file')

    def preprocess_argv():
        argvs = sys.argv
        if '-d' in argvs and '-s' in argvs:
            argvs.remove('-d')
        return argvs

    argvs = preprocess_argv()
    params = parser.parse_args(argvs[1:])
    params.d = params.s
    return params


if __name__ == '__main__':
    params = get_args()
    if params.d:
        operate_in_dir(params, params.d)
    if params.p > 0:
        count_phrase_frequency(params.f, params)
    if params.c:
        count_char_frequency(params.c, params)
    if params.p == -1 and params.f:
        count_word_frequency(params.f, params)
