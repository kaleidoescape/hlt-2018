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
    parser.add_argument('--data_dir',
        help='directory where text data is located (with subdirs "nl" and "ru" which contain vector text files)')
    parser.add_argument('--cstlemma_dir',
        help='directory where CSTLemma for lemmatizing Dutch is located')
    args = parser.parse_args()
    
    if not args.data_dir:
        args.data_dir = w2vconfig.data_dir
    if not args.cstlemma_dir:
        args.cstlemma_dir = w2vconfig.cstlemma_dir

    return args

args = parse_args()

print('Working on Dutch...')
start_time = time.time()

nl_direc = os.path.join(w2vconfig.data_dir, 'nl')
nl_sents = gensent.SentenceGenerator(language='dutch', maxsents=100)
nl_sents.read_directory(nl_direc)
nl_model = gensim.models.Word2Vec(nl_sents, **w2vconfig.gensim_config)
nl_vectors = nl_model.wv
print('Dutch word tokens: {}'.format(nl_sents.word_token_count))
print('Dutch vocab size: {}'.format(len(nl_model.wv.vocab)))
nl_vectors.save_word2vec_format('vectors/nl_vectors.txt', binary=False)

elapsed_time = time.time() - start_time
print('Elapsed time:', elapsed_time)

print() #print line break

print('Working on Russian...')
start_time = time.time()

ru_direc = os.path.join(w2vconfig.data_dir, 'ru')
ru_sents = gensent.SentenceGenerator(language='russian', maxsents=100)
ru_sents.read_directory(ru_direc)
ru_model = gensim.models.Word2Vec(ru_sents, **w2vconfig.gensim_config)
print('Russian word tokens: {}'.format(ru_sents.word_token_count))
print('Russian vocab size: {}'.format(len(ru_model.wv.vocab)))
ru_vectors = ru_model.wv
ru_vectors.save_word2vec_format('vectors/ru_vectors.txt', binary=False)

elapsed_time = time.time() - start_time
print('Elapsed time:', elapsed_time)

