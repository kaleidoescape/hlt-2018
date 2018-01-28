#!/bin/bash

wd=`pwd`
. ./dl_paths.sh #filepaths to install things to

virtualenv -p python3 env
chmod +x . ./env/bin/activate
. ./env/bin/activate
pip3 install -r requirements.txt

echo "Downloading Dutch lemmatizer."
git clone https://github.com/kuhumcst/cstlemma.git
cd cstlemma/src
make cstlemma
wget -O flexrules.dutch http://ada.sc.ku.dk/download/cstlemma/dutch/flexrules

echo "Downloading dictionaries."
cd $wd
git clone git@github.com:facebookresearch/MUSE.git
wget https://s3.amazonaws.com/arrival/dictionaries/en-nl.txt
wget https://s3.amazonaws.com/arrival/dictionaries/en-ru.txt

if [ ! -d $wikipedia_data ]; then
    echo "Downloading Wikipedia data."
    wget -O wikipedia_data.zip https://www.dropbox.com/s/a6qihkjp385d7zw/wikipedia_data.zip?dl=1
    unzip wikipedia_data.zip
else
    echo "Wikipedia data already exists in: $wikipedia_data"
fi

echo "Installation completed."
exit 0 #to exit the virtualenv subshell
