import gensim
import os
import w2vconfig
import gensent


#just some data to play around with for now
directory = os.path.join(os.path.join(w2vconfig.data_dir, 'en'), 'train')

sentences = gensent.SentenceGenerator()
sentences.read_directory(directory)
model = gensim.models.Word2Vec(sentences, min_count=1)
words = list(model.wv.vocab)
print(model['to'])
