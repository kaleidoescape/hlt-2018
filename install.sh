#!/bin/bash

wd=`pwd`
. ./dl_paths.sh #filepaths to install things to

virtualenv -p python3 env
chmod +x . ./env/bin/activate
. ./env/bin/activate
pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.0.post4-cp35-cp35m-linux_x86_64.whl 
pip3 install torchvision
pip3 install -r requirements.txt

echo "Downloading Dutch lemmatizer."
mkdir -p cstlemma
cd cstlemma
wget -O makecstlemma.bash https://raw.githubusercontent.com/kuhumcst/cstlemma/master/doc/makecstlemma.bash
wget -O flexrules.dutch http://ada.sc.ku.dk/download/cstlemma/dutch/flexrules
chmod +x ./makecstlemma.bash
./makecstlemma.bash

echo "Downloading dictionaries."
cd $wd
git clone git@github.com:facebookresearch/MUSE.git
if [ ! -d en-nl.txt ]; then
    wget https://s3.amazonaws.com/arrival/dictionaries/en-nl.txt
fi
if [ ! -d en-ru.txt ]; then
    wget https://s3.amazonaws.com/arrival/dictionaries/en-ru.txt
fi

if [ ! -d $wikipedia_data ]; then
    echo "Downloading Wikipedia data."
    wget -O wikipedia_data.zip https://www.dropbox.com/s/a6qihkjp385d7zw/wikipedia_data.zip?dl=1
    unzip wikipedia_data.zip
else
    echo "Wikipedia data already exists in: $wikipedia_data"
fi

echo "Installation completed."
exit 0 #to exit the virtualenv subshell
