data_dir = '../wikipedia_data'
cstlemma_dir = '/home/sveta/unitn/hlt/CSTLemma'

#gensim word2vec parameters:
gensim_config = {

    'sg': 0,                  #training algorithm, 0=CBOW, 1=skip-gram
                              #default=0

    'size': 300,              #dimensionality of feature vectors 
                              #(size of NN layers), default=100

    'window': 5,              #max distance between current and predicted word
                              #default=5

    'alpha': 0.025,           #initial learning rate, will linearly drop to
                              #min alpha as training progresses

    'min_alpha': 0.0001,      #minimum learning rate to drop to

    'min_count': 5,           #ignore all words with freq lower than this
                              #default=5

    'max_vocab_size': 100000, #if there are more unique words than this, 
                              #prune the infrequent ones, default=None
                              #useful as a RAM saving method because for
                              #model params it requires RAM in bytes equal to:
                              #vocab_size * layer_size * float_size * 3 

    'sample': 0.001,          #threshold s for downsampling: z(w_i) = word freq
                              #keep_prob: (sqrt(z(w_i)/s) + 1) * s/z(w_i)

    'hs': 1,                  #use hierarchical softmax, hs=0 and negative!=0
                              #means use negative sampling

    'negative': 5,            #the number of noise words to draw for negative
                              #sampling, default=5

    'cbow_mean': 1,           #when using cbow, if 0 use sum of context vectors, 
                              #if 1 use their mean, default=1

    'iter': 5,                #number of iterations (epochs), default=5

    'sorted_vocab': 1,        #sort vocab by descending frequency for indexing

    'batch_words': 10000,     #target size in words for batches passed to workers
                              #default=10000

    'null_word': 0,           #

    'compute_loss': False     #

}


#also available parameters, which require some extra work to define:

#trim_rule: None,             #vocabularly trimming callable, default=None means 
                              #trim word if word count < min count

#workers: 1,                  #parallelization, default=1 (no parallelization)
                              #only works if Cython is installed

#hashfxn: <built-in hash>     #hash function to use for randomly initializing
                              #weights, default= python's built in hash function

#seed: 1                      #for a deterministically reproducible run but in
                              #you also need workers=1 and in python3 
                              #PYTHONHASHSEED=0, whic must be set in the environment
                              #before starting the python interpreter


