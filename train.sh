#!/bin/bash

. ./dl_paths.sh #file paths of necessary training files

#spawn a subshell for the virtualenv; it won't show the (env) prefix though
#/bin/bash -c ". ./env/bin/activate; exec /bin/bash -i"

. ./env/bin/activate

echo "Step 3: Evaluating on Russian-Dutch dictionary."
python3 create_dict.py --en-nl $nl_dict --en-ru $ru_dict --nl-ru $nl_ru_dict

wd=`pwd`
if [ ! -f $nl_vectors ] || [ ! -f $ru_vectors ]; then
    echo "Step 1: Training language specific vectors with gensim."
    mkdir -p ./vectors
    python3 w2v.py --data_dir $wikipedia_data --cstlemma_dir $cstlemma_dir
    
else
    echo "Step 1: Previously trained language specific vectors found."
fi

echo "Step 2: Training correspondences with MUSE."
cd MUSE
python3 unsupervised.py --src_lang nl --tgt_lang ru --src_emb $nl_vectors --tgt_emb $ru_vectors

exit 0 #to exit the virtualenv subshell
