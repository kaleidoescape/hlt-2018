# hlt-2018

A class project for Human Language Technologies at University of Trento, winter semester 2017-2018.

https://github.com/facebookresearch/MUSE
https://arxiv.org/pdf/1710.04087.pdf

## Dependencies

- python3 with virtualenv and pip

The rest of the dependencies will be downloaded automatically as needed during installation and include (but are not limited to):
 
- pytorch
- gensim
- nltk
- MUSE 
- CSTLemma

Pre-trained word vectors are downloaded. These word vectors were trained on a comparable corpora of Dutch and Russian Wikipedia data with vocab sizes of:

Dutch word tokens: 126607116
Dutch vocab size: 29801

Russian word tokens: 197270646
Russian vocab size: 39147

The articles and a list of their titles that were used to train these vectors will be downloaded as well.

## Installation

The install script will automatically download and install all the necessary dependencies. (Note that this could take a long time, particularly if pytorch needs to be installed.)

```
./install.sh
```

## Training

The train script will automatically train any portions that weren't downloaded.

```
./train.sh
```

