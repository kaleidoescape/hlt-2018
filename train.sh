#!/bin/bash

do_baselines=1

. ./dl_paths.sh #file paths of necessary training files

. $venv/bin/activate

wd=`pwd`
if [ -f $vectors_dir/nl_vectors_lemma.txt ] && [ -f $vectors_dir/ru_vectors_lemma.txt ] && [ -f $vectors_dir/nl_vectors_nolemma.txt ] && [ -f $vectors_dir/ru_vectors_nolemma.txt ]; then
    echo "Step 1: Previously trained language specific vectors found."
elif [ ! -d $wikipedia_data ]; then 
    echo "Step 1: No Wikipedia data or pre-trained word vectors found. Exiting."
    exit 1
else
    mkdir -p $vectors_dir
    if [ ! -f $vectors_dir/nl_vectors_lemma.txt ] || [ ! -f $vectors_dir/ru_vectors_lemma.txt ]; then
        echo "Step 1: Training language specific vectors with gensim and lemmatization."
        python3 w2v.py \
            --data_dir $wikipedia_data \
            --cstlemma_dir $cstlemma_dir \
            --vectors_dir $vectors_dir \
            --lemma
    fi
    if [ ! -f $vectors_dir/nl_vectors_nolemma.txt ] || [ ! -f $vectors_dir/ru_vectors_nolemma.txt ]; then
        echo "Step 1: Training language specific vectors with gensim and no lemmatization."
        python3 w2v.py \
            --data_dir $wikipedia_data \
            --cstlemma_dir $cstlemma_dir \
            --vectors_dir $vectors_dir \
    fi 
fi

if [ ! -f $dictionaries/nl-ru.txt ] || [ ! -f $dictionaries/ru-nl.txt ]; then
    echo "Step 2: Making Dutch/Russian dictionaries."
    python3 create_dict.py \
        --nl_ru $dictionaries/nl-ru \
        --ru_nl $dictionaries/ru-nl 
else
   echo "Step 2: Previously created Dutch/Russian dictionaries found."
fi
    

echo "Step 3: Training correspondences with MUSE."
cd $wd/MUSE

#Train on our vectors which were lemmatized prior to word embedding
python3 unsupervised.py --src_lang nl --tgt_lang ru --src_emb ../vectors/nl_vectors_lemma.txt --tgt_emb ../vectors/ru_vectors_lemma.txt --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 100000

python3 unsupervised.py --src_lang ru --tgt_lang nl --src_emb ../vectors/ru_vectors_lemma.txt --tgt_emb ../vectors/nl_vectors_lemma.txt --cuda true --max_vocab 35000 --dis_most_frequent 35000 --refinement true --epoch_size 100000

#Train on our vectors which were not lemmatized prior to word embedding
python3 unsupervised.py --src_lang nl --tgt_lang ru --src_emb ../vectors/nl_vectors_nolemma.txt --tgt_emb ../vectors/ru_vectors_nolemma.txt --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 100000

python3 unsupervised.py --src_lang ru --tgt_lang nl --src_emb ../vectors/ru_vectors_nolemma.txt --tgt_emb ../vectors/nl_vectors_nolemma.txt --cuda true --max_vocab 35000 --dis_most_frequent 35000 --refinement true --epoch_size 100000

#To train the baseline models, you have to downloaded the fastText vectors,
#which are not downloaded in install.sh by default, because they are huge
if [ $do_baselines > 1 ]; then
    #Train baselines on fastText vectors
    python3 unsupervised.py --src_lang nl --tgt_lang ru --src_emb ../vectors/wiki.nl.vec --tgt_emb ../vectors/wiki.ru.vec --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 100000

    python3 unsupervised.py --src_lang ru --tgt_lang nl --src_emb ../vectors/wiki.ru.vec --tgt_emb ../vectors/wiki.nl.vec --cuda true --max_vocab 35000 --dis_most_frequent 35000 --refinement true --epoch_size 100000

    #Train baseline en-ru MUSE system to check if program works correctly
    python3 unsupervised.py --src_lang en --tgt_lang ru --src_emb ../vectors/wiki.en.vec --tgt_emb ../vectors/wiki.ru.vec --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 100000
    
    #Train baseline ru_en MUSE system to check if program works correctly
    python3 unsupervised.py --src_lang ru --tgt_lang en --src_emb ../vectors/wiki.ru.vec --tgt_emb ../vectors/wiki.en.vec --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 100000
fi

exit 0 #to exit the virtualenv subshell
