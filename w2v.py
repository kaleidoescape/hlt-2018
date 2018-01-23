import gensim
import os
import w2vconfig
import gensent


nl_direc = os.path.join(w2vconfig.data_dir, 'nl')
nl_sents = gensent.SentenceGenerator(language='dutch', maxsents=100)
nl_sents.read_directory(nl_direc)
nl_model = gensim.models.Word2Vec(nl_sents, **w2vconfig.gensim_config)
nl_vectors = nl_model.wv
nl_vectors.save('nl_vectors')

ru_direc = os.path.join(w2vconfig.data_dir, 'ru')
ru_sents = gensent.SentenceGenerator(language='russian', maxsents=100)
ru_sents.read_directory(ru_direc)
ru_model = gensim.models.Word2Vec(ru_sents, **w2vconfig.gensim_config)
ru_vectors = ru_model.wv
ru_vectors.save('ru_vectors')
