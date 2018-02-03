#!/bin/bash

. ./dl_paths.sh #file paths of necessary training files

#spawn a subshell for the virtualenv; it won't show the (env) prefix though
#/bin/bash -c ". ./env/bin/activate; exec /bin/bash -i"

. ./env/bin/activate

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
        --nl_ru $dictionaries/nl-ru.txt \
        --ru_nl $dictionaries/ru-nl.txt 
        
    #python3 create_dict.py \
    #    --nl_ru $dictionaries/nl-ru.0-5000.txt \
    #    --ru_nl $dictionaries/ru-nl.0-5000.txt \
    #    --minimum 0 \
    #    --maximum 5000 
        
    python3 create_dict.py \
        --nl_ru $dictionaries/nl-ru.5000-6500.txt \
        --ru_nl $dictionaries/ru-nl.5000-6500.txt \
        --minimum 5000 \
        --maximum 6500 
else
   echo "Step 2: Previously created Dutch/Russian dictionaries found."
fi
    

echo "Step 3: Training correspondences with MUSE."
cd $wd/MUSE
python3 unsupervised.py \
    --src_lang nl \
    --tgt_lang ru \
    --src_emb ../vectors/nl_vectors.txt \
    --tgt_emb ../vectors/ru_vectors.txt \
    --cuda "True" \
    --refinement "True" \
    --max_vocab 35000 \
    --dis_most_frequent 35000 \
    --epoch_size 10000 \
    --n_epochs 1


exit 0 #to exit the virtualenv subshell
