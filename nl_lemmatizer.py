import subprocess

def create_lemma_dict(lemma_dict):
    lemmas = {}
    with open(lemma_dict, 'r', encoding='utf-8') as f:
        for line in f:
            w, l = line.split()
            if w not in lemmas: 
                lemmas[w] = l
    return lemmas
    
def lemmatize(word, lemma_dict):
    if word in lemma_dict:
        return lemma_dict[word]
    else:
        return word
        
def lemmatize(word):
    with open('input_word.txt', 'w', encoding='utf-8') as f:
        f.write(word)
    text = subprocess.check_output("~/Documenten/HLT/lemmatizer-2/cstlemma/cstlemma -L -f ~/Documenten/HLT/lemmatizer-2/cstlemma/flexrules -i input_word.txt", shell=True)
    words = text.decode().split()[-1]
    return(words.split('|'))
    
