from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation as PUNCTUATION
import re
import os
import subprocess
from pymystem3 import Mystem
import w2vconfig


class SentenceGeneratorException(Exception):
    """Raise for improper use of the SentenceGenerator."""

class SentenceGenerator(object):
    """
    Generate sentences one at a time from a list of sentences and/or
    from text files in a directory. Prepare the SentenceGenerator by
    reading from a sentence list or a directory first, then iterate
    over the SentenceGenerator to get the tokenized sentences.
    """
    NUM = 'NUM'
    UNK = 'UNK'
    PUNCTUATION = PUNCTUATION

    def __init__(self, language='english', maxsents=0, lemma=False, cstlemma_dir=None):
        self.filepaths = None
        self.sentence_list = None
        self.language = language
        self.m = Mystem()
        self.maxsents = maxsents
        self.count = 0
        self.word_token_count = 0
        self.lemma = lemma
        self.cstlemma_dir = cstlemma_dir
        if not self.cstlemma_dir:
            self.cstlemma_dir = w2vconfig.cstlemma_dir

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

        if self.filepaths is not None and self.lemma:
            for fp in self.filepaths:
                if self.language == 'dutch': 
                    text = self._get_filetext_with_cstlemma(fp)
                    sents = sent_tokenize(text, language=self.language)
                    for sent in sents:
                        self.count += 1
                        if self.maxsents and self.count > self.maxsents:
                            raise StopIteration
                        yield self._process_sentence(sent) 
                else:
                    with open(fp, 'r', encoding='utf-8') as infp:
                        text = infp.read() 
                        sents = sent_tokenize(text) #split into sentences
                        for sent in sents:
                            self.count += 1
                            if self.maxsents and self.count > self.maxsents:
                                raise StopIteration
                            yield self._process_sentence(sent)
        elif self.filepaths is not None:
            for fp in self.filepaths:
                with open(fp, 'r', encoding='utf-8') as infp:
                    text = infp.read() 
                    sents = sent_tokenize(text) #split into sentences
                    for sent in sents:
                        self.count += 1
                        if self.maxsents and self.count > self.maxsents:
                            raise StopIteration
                        yield self._process_sentence(sent)


    def _get_filetext_with_cstlemma(self, fp):
        cmd = "{}/cstlemma/cstlemma -L -f {}/cstlemma/flexrules.dutch -i {}".format(self.cstlemma_dir, self.cstlemma_dir, fp)
        process = subprocess.Popen(cmd, shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        lines = process.stdout.readlines()
        s = ''
        i = 0
        for line in lines:
            i += 1
            if i<3: 
                continue #first two lines are just info from CSTLemma
            line = line.decode().strip()
            if line:
                line = line.split()[-1]
                line = line.split('|')[0]
                s += ' '+line
        return s

    def _process_sentence(self, sentence):
        """Process a text sentence into a list of utf-8 words."""
        #regex for floats and integers starting with optional $ or €
        regex = re.compile(r'^[$€]?(?=.)([+-]?([0-9]*)(\.([0-9]+))?)$')
        
        #split into words
        if self.language == 'russian' and self.lemma:
            tokenized = self.m.lemmatize(sentence)
        else:
            tokenized = word_tokenize(sentence)
        
        #process into lowercased words, replacing numbers and punctuation
        tokens = []
        for w in tokenized:
            w = w.strip().lower()
            w = re.sub(regex, self.NUM, w)    #replace numbers
            if w in self.PUNCTUATION or not w:  
                continue              #remove !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            if len(w.split()) > 1: #replace words with spaces inside w/ UNK;
                continue           #(TODO these probably shouldn't exist)
            tokens.append(w)
            self.word_token_count += 1
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

