#!/bin/bash

get_fastText=0  #download Facebook fastText vectors (VERY time consuming)
get_wikipedia=1 #download Wikipedia comparable corpora (time consuming)

wd=`pwd`
. ./dl_paths.sh #filepaths to install things to

echo "Activating python3 virtualenv."
if [ ! -d $venv ]; then
    virtualenv -p python3 env
    chmod +x . ./env/bin/activate
    . ./env/bin/activate
    echo "Installing pytorch to virtualenv in $venv"
    pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp35-cp35m-linux_x86_64.whl 
    pip3 install torchvision
else
    . $venv/bin/activate
fi

echo "Installing other requirements."
pip3 install -r requirements.txt

echo "Downloading Dutch lemmatizer."
mkdir -p $cstlemma_dir
cd $cstlemma_dir
wget -O makecstlemma.bash https://raw.githubusercontent.com/kuhumcst/cstlemma/master/doc/makecstlemma.bash
chmod +x ./makecstlemma.bash
./makecstlemma.bash
#Have to download this file after make
wget -O $cstlemma_dir/flexrules.dutch http://ada.sc.ku.dk/download/cstlemma/dutch/flexrules

echo "Downloading MUSE."
cd $wd
git clone git@github.com:facebookresearch/MUSE.git

#Have to create them after MUSE installation
echo "Creating Dutch/Russian dictionaries."
cd $wd
mkdir -p $dictionaries
if [ ! -f $dictionaries/en-nl.txt ]; then
    echo "Downloading en-nl dictionary."
    wget -O $dictionaries/en-nl.txt https://s3.amazonaws.com/arrival/dictionaries/en-nl.txt
fi
if [ ! -f $dictionaries/en-ru.txt ]; then
    echo "Downloading en-ru dictionary."
    wget -O $dictionaries/en-ru.txt https://s3.amazonaws.com/arrival/dictionaries/en-ru.txt
fi

#TODO update this
if [ ! -d $vectors_dir/nl_vectors.txt ] || [ ! -f $vectors_dir/ru_vectors.txt ]; then
    echo "Downloading pre-trained word vectors."
    wget -O vectors.zip https://www.dropbox.com/s/nl7bwt5rnf0jhsz/vectors.zip?dl=1
    unzip vectors.zip
else
    echo "Pre-trained word vectors already exist: $vectors_dir"
fi

if [ $get_fastText > 0 ] && [ -f $vectors_dir/wiki.en.vec ] && [ -f $vectors_dir/wiki.nl.vec ] && [ -f $vectors_dir/wiki.ru.vec ]; then
    echo "Found fastText vectors. Not re-downloading."
elif [ $get_fastText > 0 ]
    echo "Downloading fastText word embeddings. This will take a really long time and require 9GB of space!"
    if [ ! -f $vectors_dir/wiki.en.vec ]; then
        curl -Lo $vectors_dir/wiki.en.vec https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.vec
    fi
    if [ ! -f $vectors_dir/wiki.nl.vec ]; thnl
        curl -Lo $vectors_dir/wiki.nl.vec https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.nl.vec
    fi
    if [ ! -f $vectors_dir/wiki.ru.vec ]; thru
        curl -Lo $vectors_dir/wiki.ru.vec https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.ru.vec
    fi
fi

echo "Cloning biwikibot."
git clone git@github.com:kaleidoescape/biwikibot.git

if [ $get_wikipedia > 0 ] && [ ! -d $wikipedia_data ]; then
    echo "Downloading Wikipedia data."
    wget -O wikipedia_data.zip https://www.dropbox.com/s/a6qihkjp385d7zw/wikipedia_data.zip?dl=1
    unzip wikipedia_data.zip 
fi

echo "Installation completed."
exit 0 #to exit the virtualenv subshell
