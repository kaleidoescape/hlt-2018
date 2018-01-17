def load_dict(src_tar_fp):
    d = {}
    with open(src_tar_fp, 'r', encoding='utf-8') as infp:
        for line in infp:
            src_word, tar_word = line.split()
            if src_word == tar_word:
                continue #in this case, it's prolly just the en word twice
            if len(src_word) == 1 or len(tar_word) == 1:
                continue
            if src_word not in d:
                d[src_word] = [tar_word]
            else:
                d[src_word].append(tar_word)
    return d

def merge_dicts(dict_a, dict_b):
    merged = dict_a
    for word in dict_b:
        if word not in merged:
            merged[word] = [dict_b[word]]
        else:
            merged[word] = [merged[word], dict_b[word]]
    return merged

if __name__ == '__main__': 
    en_nl_fp = 'en-nl.txt'
    en_ru_fp = 'en-ru.txt'
    en_nl = load_dict(en_nl_fp)
    en_ru = load_dict(en_ru_fp)
    merged = merge_dicts(en_nl, en_ru)
    with open('merged.txt', 'w', encoding='utf-8') as outfp:
        for en_word in merged:
            if len(merged[en_word]) < 2:
                continue
            nl = merged[en_word][0]
            ru = merged[en_word][1]
            #TODO: lemmatization
            for nl_word in nl:
                for ru_word in ru:
                    outfp.write('{} {} {}\n'.format(nl_word, ru_word, en_word)) 
