#!/bin/bash

wd=`pwd`
. ./dl_paths.sh #filepaths to install things to

echo "Activating python3 virtualenv."
virtualenv -p python3 env
chmod +x . ./env/bin/activate
. ./env/bin/activate

echo "Installing pytorch."
pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp35-cp35m-linux_x86_64.whl 
pip3 install torchvision

echo "Installing other requirements."
pip3 install -r requirements.txt

echo "Downloading Dutch lemmatizer."
mkdir -p $cstlemma_dir
cd $cstlemma_dir
wget -O makecstlemma.bash https://raw.githubusercontent.com/kuhumcst/cstlemma/master/doc/makecstlemma.bash
wget -O flexrules.dutch http://ada.sc.ku.dk/download/cstlemma/dutch/flexrules
chmod +x ./makecstlemma.bash
./makecstlemma.bash

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

echo "Downloading MUSE."
git clone git@github.com:facebookresearch/MUSE.git

if [ ! -d $vectors ]; then
    echo "Downloading pre-trained word vectors."
    wget -O vectors.zip https://www.dropbox.com/s/nl7bwt5rnf0jhsz/vectors.zip?dl=1
    unzip vectors.zip -d $vectors_dir
else
    echo "Pre-trained word vectors already exist: $vectors_dir"
fi

#TODO it an option to run the training on this data rather than on pre-trained vectors
if [ ! -d $wikipedia_data ]; then
    echo "Downloading Wikipedia data."
    wget -O wikipedia_data.zip https://www.dropbox.com/s/a6qihkjp385d7zw/wikipedia_data.zip?dl=1
    unzip wikipedia_data.zip -d $wikipedia_data
else
    echo "Wikipedia data already exists in: $wikipedia_data"
fi



echo "Installation completed."
exit 0 #to exit the virtualenv subshell
