import os
import sys
from pymystem3 import Mystem
import nl_lemmatizer
import w2vconfig
import argparse

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
    parser.add_argument('--en-nl',
        type=str, 
        default='en-nl.txt',
        help='file path to English-Dutch dictionary')
    parser.add_argument('--en-ru',
        type=str, 
        default='en-ru.txt',
        help='file path to English-Russian dictionary')
    parser.add_argument('--directory',
        type=str, 
        default=w2vconfig.nl_ru_dict,
        help='where to create the new Dutch-Russian dictionary or dictionaries')
    parser.add_argument('--nl-ru',
        type=bool, 
        default=True,
        help='Create a Dutch to Russian dictionary if set to True')
    parser.add_argument('--ru-nl',
        type=bool, 
        default=True,
        help='Create a Russian to Dutch dictionary if set to True')
    args = parser.parse_args()

#    if not args.en_nl:
#        args.en_nl = 'en-nl.txt'
#    if not args.en_ru:
#        args.en_ru = 'en-ru.txt'
#    if not args.nl_ru:
#        args.nl_ru = w2vconfig.nl_ru_dict

#    if os.path.exists(args.directory):
#        print('Dutch-Russian dictionary already exists: {}'.format(args.nl_ru))
#        sys.exit(0)
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


if __name__ == '__main__':
    args = parse_args()
    r = Mystem()
    en_nl_fp = args.en_nl
    en_ru_fp = args.en_ru
    en_nl = load_dict(en_nl_fp)
    en_ru = load_dict(en_ru_fp)
    merged = merge_dicts(en_nl, en_ru)
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
    if args.nl_ru:
        with open(args.directory+'nl-ru.txt', 'w', encoding='utf-8') as outfp:
            for triplet in triplets:
                outfp.write('{}\t{}\n'.format(triplet[0], triplet[1])) 
    if args.ru_nl:
        with open(args.directory+'ru-nl.txt', 'w', encoding='utf-8') as outfp:
            for triplet in triplets:
                outfp.write('{}\t{}\n'.format(triplet[1], triplet[0])) 
   
            
            
#with open(args.filepath+'nl-ru.txt', 'w', encoding='utf-8') as outfp:
#        for triplet in triplets:
#            outfp.write('{} {}\n'.format(triplet[2], triplet[0], triplet[1])) 
