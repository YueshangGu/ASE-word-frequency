import argparse
from utils import count_char_frequency
from utils import count_word_frequency
from utils import count_phrase_frequency
import sys
from utils import operate_in_dir


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='output character frequencies')
    parser.add_argument('-f', action='store_true', help='output word frequencies')
    parser.add_argument('-p', type=int, default=-1, help='output phrase frequencies')
    parser.add_argument('-d', action='store_true', help='treat the string as a directory')
    parser.add_argument('-s', action='store_true', default='', help='recurse into sub_dir')
    parser.add_argument('-n', type=int, default=-1, help='output the first n items')
    parser.add_argument('-x', type=str, default='', help='stop words')
    parser.add_argument('-v', type=str, default='', help='verb file')

    def preprocess_argv():
        argvs = sys.argv
        # if '-d' in argvs and '-s' in argvs:
        #     argvs.remove('-d')
        # for x in ['-f', '-c']:
        #     if x in argvs:
        #         path = argvs[-1]
        #         argvs.remove(x)
        #         argvs.remove(path)
        #         argvs.append(x)
        #         argvs.append(path)
        path = argvs[-1]
        argvs.remove(path)
        return argvs, path

    argvs, path = preprocess_argv()
    params = parser.parse_args(argvs[1:])
    # params.d = params.s  # 这句话导致 -d 功能失效
    return params, path


if __name__ == '__main__':
    params, path = get_args()
    if params.d or params.s:
        operate_in_dir(params, path)
    elif params.p > 0:
        count_phrase_frequency(path, params)
    elif params.c:
        count_char_frequency(path, params)
    elif params.p == -1 and params.f:
        count_word_frequency(path, params)
