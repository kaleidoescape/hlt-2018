import gensim
import os
import w2vconfig
import gensent

nl_direc = os.path.join(w2vconfig.data_dir, 'nl')
nl_sents = gensent.SentenceGenerator(language='dutch')
nl_sents.read_directory(nl_direc)
print('Dutch word tokens: {}'.format(nl_sents.word_token_count))
nl_model = gensim.models.Word2Vec(nl_sents, **w2vconfig.gensim_config)
nl_vectors = nl_model.wv
print('Dutch vocab size: {}'.format(len(nl_model.wv.vocab)))
nl_vectors.save_word2vec_format('nl_vectors', binary=False)

ru_direc = os.path.join(w2vconfig.data_dir, 'ru')
ru_sents = gensent.SentenceGenerator(language='russian')
ru_sents.read_directory(ru_direc)
print('Russian word tokens: {}'.format(ru_sents.word_token_count))
ru_model = gensim.models.Word2Vec(ru_sents, **w2vconfig.gensim_config)
print('Russian vocab size: {}'.format(len(ru_model.wv.vocab)))
ru_vectors = ru_model.wv
ru_vectors.save_word2vec_format('ru_vectors', binary=False)
