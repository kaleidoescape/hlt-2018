import gensim
import os
import w2vconfig
import gensent


nl_direc = os.path.join(w2vconfig.data_dir, 'nl')
ru_direc = os.path.join(w2vconfig.data_dir, 'ru')

nl_sents = gensent.SentenceGenerator(language='dutch')
ru_sents = gensent.SentenceGenerator(language='russian')

nl_sents.read_directory(nl_direc)
ru_sents.read_directory(ru_direc)

nl_model = gensim.models.Word2Vec(nl_sents, **w2vconfig.gensim_config)
ru_model = gensim.models.Word2Vec(ru_sents, **w2vconfig.gensim_config)

nl_vectors = nl_model.wv
ru_vectors = ru_model.wv

nl_vectors.save('nl_vectors')
ru_vectors.save('ru_vectors')
