
import os
import sys
from pymystem3 import Mystem
import nl_lemmatizer
import w2vconfig
import argparse
import gensim

class AlterParser(argparse.ArgumentParser):
    """Change behaviour of ArgumentParser.error() to print help and exit."""
    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(2)

def parse_args():
    """Parse command line arguments."""
    parser = AlterParser(prog='create_dict.py', 
            description='Create a Dutch-Russian dictionary from English-Dutch and English-Russian ones.')
    parser.add_argument('--en_nl',
        default=w2vconfig.dicts_dir + 'en-nl.txt',
        help='file path to English-Dutch dictionary')
    parser.add_argument('--en_ru',
        default=w2vconfig.dicts_dir + 'en-ru.txt',
        help='file path to English-Russian dictionary')
    parser.add_argument('--nl_ru',
        help='File name where to store nl-ru dictionary (without file extension)')
    parser.add_argument('--ru_nl',
        help='File name where to store ru-nl dictionary (without file extension)')
    args = parser.parse_args()
    return args

def load_dict(src_tar_fp):
    d = {}
    with open(src_tar_fp, 'r', encoding='utf-8') as infp:
        for line in infp:
            src_word, tar_word = line.split()
            if src_word == tar_word:
                continue #in this case, it's prolly just the en word twice
            if len(src_word) == 1 or len(tar_word) == 1:
                continue
            if src_word not in d:
                d[src_word] = [tar_word]
            else:
                d[src_word].append(tar_word)
    return d

def merge_dicts(dict_a, dict_b):
    merged = {}
    for word in dict_b:
        if word not in dict_a:
            continue
        else:
            merged[word] = [dict_a[word], dict_b[word]]
    for word in dict_a:
        if word not in dict_b:
            continue
        else:
            merged[word] = [dict_a[word], dict_b[word]]
            
    return merged

def generate_triplets(merged):
    triplets = [] # changed this to a list to keep the dicts "roughly" sorted on freq info (assuming that the 
                  # translations of English words are roughly as frequent as the English words, which is needed for MUSE
    for en_word in merged:
        if len(merged[en_word]) < 2:
            continue
        nl = merged[en_word][0]
        ru = merged[en_word][1]
        for nl_word in nl:
            for word in nl_lemmatizer.lemmatize(nl_word):
                nl_word = word
                for ru_word in ru:
                    ru_word = r.lemmatize(ru_word)[0]
                    if (nl_word, ru_word, en_word) not in triplets:
                        triplets.append((nl_word, ru_word, en_word))
    return triplets
  
def create_5000_6500(triplets):
    """
    Create files titled nl-ru.5000-6500.txt and ru-nl.5000-6500.txt
    but they will have more words in them than that, to account for
    some duplicates. They are titled that because that's what MUSE
    has hardcoded as a filepath..
    """
    suff = '.5000-6500.txt'
    nl_ru_seen = set()
    ru_nl_seen = set()
    nl_ru_c = 0
    ru_nl_c = 0
    nl_vecs = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(w2vconfig.vectors_dir, 'nl_vectors.txt'))
    ru_vecs = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(w2vconfig.vectors_dir, 'ru_vectors.txt'))
    with open(args.nl_ru + suff , 'w', encoding='utf-8') as nl_ru_fp:
        with open(args.ru_nl + suff, 'w', encoding='utf-8') as ru_nl_fp:
            for triplet in triplets:
                nl = triplet[0].strip()
                ru = triplet[1].strip()
                try:
                    ru_vecs[ru]
                    nl_vecs[nl]
                except KeyError:
                    continue
                if nl not in nl_ru_seen and ru not in nl_ru_seen:
                    nl_ru_c += 1
                    nl_ru_seen.add(nl)
                    nl_ru_seen.add(ru)
                    if 5000 < nl_ru_c <= 7500:
                        nl_ru_fp.write('{} {}\n'.format(nl, ru))
                if nl not in ru_nl_seen and ru not in ru_nl_seen:
                    ru_nl_c += 1
                    ru_nl_seen.add(nl)
                    ru_nl_seen.add(ru)
                    if 5000 < ru_nl_c <= 7500:
                        ru_nl_fp.write('{} {}\n'.format(ru, nl))

def create_dicts(triplets):
    with open(args.nl_ru + '.txt', 'w', encoding='utf-8') as nl_ru_fp:
        with open(args.ru_nl + '.txt', 'w', encoding='utf-8') as ru_nl_fp:
            for triplet in triplets:
                nl = triplet[0].strip()
                ru = triplet[1].strip()
                nl_ru_fp.write('{} {}\n'.format(nl, ru))
                ru_nl_fp.write('{} {}\n'.format(ru, nl))
        
if __name__ == '__main__':
    args = parse_args()
    r = Mystem()
    en_nl_fp = args.en_nl
    en_ru_fp = args.en_ru
    en_nl = load_dict(en_nl_fp)
    en_ru = load_dict(en_ru_fp)
    merged = merge_dicts(en_nl, en_ru)
    triplets = generate_triplets(merged)
    create_dicts(triplets)
    create_5000_6500(triplets)





