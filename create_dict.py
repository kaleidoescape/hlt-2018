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
    parser.add_argument('--en_nl',
        type=str, 
        default=w2vconfig.dicts_dir + 'en-nl.txt',
        help='file path to English-Dutch dictionary')
    parser.add_argument('--en_ru',
        type=str, 
        default=w2vconfig.dicts_dir + 'en-ru.txt',
        help='file path to English-Russian dictionary')
    parser.add_argument('--directory',
        type=str, 
        default=w2vconfig.dicts_dir,
        help='where to create the new dictionary or dictionaries')
    parser.add_argument('--save_merged',
        type=str, 
        default=w2vconfig.dicts_dir + 'merged.txt',
        help='File name where to store en-nl-ru dictionary (no, if no dictionary should be created')
    parser.add_argument('--load_merged',
        type=str, 
        default=w2vconfig.dicts_dir + 'merged.txt',
        help='Load a previously stored merged en-nl-ru dictionary')
    parser.add_argument('--nl_ru',
        type=str, 
        default='no',
        help='File name where to store nl-ru dictionary (no, if no dictionary should be created')
    parser.add_argument('--ru_nl',
        type=str, 
        default='no',
        help='File name where to store ru-nl dictionary (no, if no dictionary should be created')
    parser.add_argument('--minimum',
        type=int,
        default=0,
        help='Create a dictionary starting from the n\'th lemma in the English dictionary')
    parser.add_argument('--maximum',
        type=int,
        default=-1,
        help='Create a dictionary ending after the n\'th lemma in the English dictionary (-1 for end of dictionary')
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
   
    
def load_triplets(fp):
    triplets = []
    with open(fp, 'r', encoding='utf-8') as infp:
        for line in infp:
            en_word, nl_word, ru_word = line.split()
            triplets.append((nl_word, ru_word, en_word))
            
    return triplets
    
    
def save_triplets(fp, triplets):
    with open(fp, 'w', encoding='utf-8') as outfp:
        for triplet in triplets:
            outfp.write('{} {} {}\n'.format(triplet[2], triplet[0], triplet[1]))

        
if __name__ == '__main__':
    args = parse_args()
    if args.maximum != -1:
       assert args.minimum < args.maximum
    r = Mystem()
    en_nl_fp = args.en_nl
    en_ru_fp = args.en_ru
    en_nl = load_dict(en_nl_fp)
    en_ru = load_dict(en_ru_fp)
    
    if os.path.isfile(args.load_merged):
        triplets = load_triplets(args.load_merged)
    else:
        merged = merge_dicts(en_nl, en_ru)
        triplets = generate_triplets(merged)
        
        if args.merged != 'no':
            fp = os.path.join(args.directory, args.merged)
            save_triplets(fp, triplets)
        
    
    # Keep track of many lemmas have been stored in dictionary 
    if args.maximum == -1:
        maximum = len(triplets)               
    elif args.maximum < len(triplets):                
        maximum = args.maximum
    else:
        maximum = len(triplets)
    minimum = args.minimum
    
    if args.nl_ru != 'no':
        seen_lemmas = set()
        fp = os.path.join(args.directory, args.nl_ru)
        with open(fp, 'w', encoding='utf-8') as outfp:
            i=minimum
            count = minimum
            while count < maximum and i < len(triplets):
                outfp.write('{}\t{}\n'.format(triplets[i][0], triplets[i][1])) 
                if not triplets[i][1] in seen_lemmas:
                    count += 1
                    seen_lemmas.add(triplets[i][0])
                i += 1
                    
    if args.ru_nl != 'no':
        seen_lemmas = set()
        count = args.minimum
        fp = os.path.join(args.directory, args.ru_nl)
        with open(fp, 'w', encoding='utf-8') as outfp:
            i=minimum
            count = minimum
            while count < maximum and i < len(triplets):
                outfp.write('{}\t{}\n'.format(triplets[i][1], triplets[i][0])) 
                if not triplets[i][1] in seen_lemmas:
                    count += 1
                    seen_lemmas.add(triplets[i][1])
                i += 1
    
