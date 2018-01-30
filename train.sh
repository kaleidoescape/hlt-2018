#!/bin/bash

. ./dl_paths.sh #file paths of necessary training files

#spawn a subshell for the virtualenv; it won't show the (env) prefix though
#/bin/bash -c ". ./env/bin/activate; exec /bin/bash -i"

. ./env/bin/activate

wd=`pwd`
if [ ! -f $wd/$vectors_dir/nl_vectors.txt ] || [ ! -f $wd/$vectors_dir/ru_vectors.txt ]; then
    echo "Step 1: Training language specific vectors with gensim."
    mkdir -p $wd/$vectors_dir
    python3 w2v.py \
        --data_dir $wd/$wikipedia_data \
        --cstlemma_dir $wd/$cstlemma_dir \
        --vectors_dir $wd/$vectors_dir
    
else
    echo "Step 1: Previously trained language specific vectors found."
fi

#TODO this step doesn't work yet
echo "Step 2: Training correspondences with MUSE."
cd $wd/MUSE
python3 unsupervised.py \
    --src_lang nl \
    --tgt_lang ru \
    --src_emb $wd/$vectors_dir/nl_vectors.txt \
    --tgt_emb $wd/$vectors_dir/ru_vectors.txt

#TODO: write evaluation script
echo "Step 3: Evaluating on Russian-Dutch dictionary."
cd $wd
if [ ! -f $wd/$dictionaries/nl-ru.txt ] || [ ! -f $wd/$dictionaries/ru-nl.txt ]; then
    python3 create_dict.py \
        --en_nl $dictionaries/en-nl.txt \
        --en_ru $dictionaries/en-ru.txt \
        --directory=$dictionaries
fi

exit 0 #to exit the virtualenv subshell
