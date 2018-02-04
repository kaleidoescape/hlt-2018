#!/bin/bash

. ./dl_paths.sh #file paths of necessary training files

. $venv/bin/activate

wd=`pwd`
if [ ! -d $wikipedia_data ] &&  [ ! -f $vectors_dir/nl_vectors.txt ] && [ ! -f $vectors_dir/ru_vectors.txt ]; then
    echo "Step 1: No Wikipedia data or pre-trained word vectors found. Exiting."
    exit 1
elif [ ! -f $vectors_dir/nl_vectors.txt ] || [ ! -f $vectors_dir/ru_vectors.txt ]; then
    echo "Step 1: Training language specific vectors with gensim."
    mkdir -p $vectors_dir
    python3 w2v.py \
        --data_dir $wikipedia_data \
        --cstlemma_dir $cstlemma_dir \
        --vectors_dir $vectors_dir
        
    
else
    echo "Step 1: Previously trained language specific vectors found."
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
python3 unsupervised.py --src_lang nl --tgt_lang ru --src_emb ../vectors/nl_vectors.txt --tgt_emb ../vectors/ru_vectors.txt --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 200000

python3 unsupervised.py --src_lang ru --tgt_lang nl --src_emb ../vectors/ru_vectors.txt --tgt_emb ../vectors/nl_vectors.txt --cuda True --max_vocab 35000 --dis_most_frequent 35000 --refinement True --epoch_size 200000

exit 0 #to exit the virtualenv subshell
