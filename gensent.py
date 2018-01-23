from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation as PUNCTUATION
import re
import os
import w2vconfig
from pymystem3 import Mystem

class SentenceGeneratorException(Exception):
    """Raise for improper use of the SentenceGenerator."""

class SentenceGenerator(object):
    """
    Generate sentences one at a time from a list of sentences and/or
    from text files in a directory. Prepare the SentenceGenerator by
    reading from a sentence list or a directory first, then iterate
    over the SentenceGenerator to get the tokenized sentences.
    """
    NUM = 'NUM_TOKEN'

    def __init__(self, language='english', maxsents=0):
        self.filepaths = None
        self.sentence_list = None
        self.language = language
        self.m = Mystem()
        self.maxsents = maxsents
        self.count = 0

    def read_directory(self, directory):
        """Prepare the SentenceGenerator from a directory on disk."""
        self.filepaths = [os.path.join(directory, fp) 
                          for fp in os.listdir(directory)] 
        self.sentences = self._gen_sentences()

    def read_sentence_list(self, sentence_list):
        """Prepare the SentenceGenerator from a list of sentences. """
        self.sentence_list = sentence_list
        self.sentences = self._gen_sentences()
   
    def _gen_sentences(self):
        """Generate sentences first from sentence list, then from directory."""
        if self.sentence_list is None and self.filepaths is None:
            raise SentenceGeneratorException('Please prepare the '
                    'SentenceGenerator by running read_directory(directory) '
                    'or read_sentence_list(sentence_list) first.')

        if self.sentence_list is not None:
            for sentence in self.sentence_list:
                self.count += 1
                if self.maxsents and self.count > self.maxsents:
                    raise StopIteration
                yield self._process_sentence(sentence)

        if self.filepaths is not None:
            for fp in self.filepaths:
                with open(fp, 'r', encoding='utf-8') as infp:
                    text = infp.read() 
                    sents = sent_tokenize(text)
                    for sent in sents:
                        self.count += 1
                        if self.maxsents and self.count > self.maxsents:
                            raise StopIteration
                        yield self._process_sentence(sent)

    def _process_sentence(self, sentence):
        """Process a text sentence into a list of utf-8 words."""
        #regex for floats and integers starting with optional $ or €
        regex = re.compile(r'^[$€]?(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$')
        
        #split into words
        if self.language == 'russian':
            tokenized = self.m.lemmatize(sentence)
        else:
            tokenized = word_tokenize(sentence)
        
        #process into lowercased words, replacing numbers and punctuation
        tokens = []
        for w in tokenized:
            #remove !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            w = w.strip()
            if w in PUNCTUATION or not w:    
                continue
            w = w.lower()                  #lowercase
            w = re.sub(regex, self.NUM, w) #replace numbers
            tokens.append(w)

        return tokens

    def __iter__(self):
        return SentenceGeneratorIterator(self)

class SentenceGeneratorIterator(object):
    """
    An iterator for the SentenceGenerator class that can be used in order to
    iterate over the generator more than once or in parallel.
    """
    def __init__(self, sentence_generator):
        self.sentence_generator = sentence_generator
        self.sentences = self.sentence_generator._gen_sentences()

    def __iter__(self):
        return self.sentences

    def __next__(self):
        return next(self.sentences)

