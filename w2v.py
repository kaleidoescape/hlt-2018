import gensim
import os
import w2vconfig
import gensent
import time
import argparse


class AlterParser(argparse.ArgumentParser):
    """Change behaviour of ArgumentParser.error() to print help and exit."""
    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(2)

def parse_args():
    """Parse command line arguments."""
    parser = AlterParser(prog='train_gensim_vectors.py', 
            description='Use gensim to train Dutch and Russian word vectors.')
    parser.add_argument('--data_dir', default=w2vconfig.data_dir,
        help='directory where text data is located (with subdirs "nl" and "ru" which contain vector text files)')
    parser.add_argument('--cstlemma_dir', default=w2vconfig.cstlemma_dir,
        help='directory where CSTLemma for lemmatizing Dutch is located')
    parser.add_argument('--vectors_dir', default=w2vconfig.vectors_dir,
        help='directory where vectors text files will be saved')
    parser.add_argument('--lemma', action='store_true', default=False,
        help='lemmatize the sentences before training word vectors')
    args = parser.parse_args()

    return args

args = parse_args()

print('Working on Dutch...')
start_time = time.time()

nl_direc = os.path.join(args.data_dir, 'nl')
nl_sents = gensent.SentenceGenerator(language='dutch', lemma=args.lemma, cstlemma_dir=args.cstlemma_dir)
nl_sents.read_directory(nl_direc)
nl_model = gensim.models.Word2Vec(nl_sents, **w2vconfig.gensim_config)
nl_vectors = nl_model.wv
print('Dutch word tokens: {}'.format(nl_sents.word_token_count))
print('Dutch vocab size: {}'.format(len(nl_model.wv.vocab)))
if args.lemma:
    nl_vectors_fp = os.path.join(args.vectors_dir, 'nl_vectors_lemma.txt')
else:
    nl_vectors_fp = os.path.join(args.vectors_dir, 'nl_vectors_nolemma.txt')
nl_vectors.save_word2vec_format(nl_vectors_fp, binary=False)

elapsed_time = time.time() - start_time
print('Elapsed time:', elapsed_time)

print() #print line break

print('Working on Russian...')
start_time = time.time()

ru_direc = os.path.join(args.data_dir, 'ru')
ru_sents = gensent.SentenceGenerator(language='russian', lemma=args.lemma)
ru_sents.read_directory(ru_direc)
ru_model = gensim.models.Word2Vec(ru_sents, **w2vconfig.gensim_config)
print('Russian word tokens: {}'.format(ru_sents.word_token_count))
print('Russian vocab size: {}'.format(len(ru_model.wv.vocab)))
ru_vectors = ru_model.wv
if args.lemma:
    ru_vectors_fp = os.path.join(args.vectors_dir, 'ru_vectors_lemma.txt')
else:
    ru_vectors_fp = os.path.join(args.vectors_dir, 'ru_vectors_nolemma.txt')
ru_vectors.save_word2vec_format(ru_vectors_fp, binary=False)

elapsed_time = time.time() - start_time
print('Elapsed time:', elapsed_time)

