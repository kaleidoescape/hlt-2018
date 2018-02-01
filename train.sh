#!/bin/bash

. ./dl_paths.sh #file paths of necessary training files

#spawn a subshell for the virtualenv; it won't show the (env) prefix though
#/bin/bash -c ". ./env/bin/activate; exec /bin/bash -i"

. ./env/bin/activate

wd=`pwd`
if [ ! -d $wd/$wikipedia_data ] &&  [ ! -f $wd/$vectors_dir/nl_vectors.txt ] && [ ! -f $wd/$vectors_dir/ru_vectors.txt ]; then
    echo "Step 1: No Wikipedia data or pre-trained word vectors found. Exiting."
    exit 1
elif [ ! -f $wd/$vectors_dir/nl_vectors.txt ] || [ ! -f $wd/$vectors_dir/ru_vectors.txt ]; then
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
    --src_emb ../vectors/nl_vectors.txt \
    --tgt_emb ../vectors/ru_vectors.txt \


#TODO: create evaluation script or use MUSE's?
echo "Step 3: Evaluating performance."

exit 0 #to exit the virtualenv subshell
