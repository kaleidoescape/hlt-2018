# hlt-2018

A class project for Human Language Technologies at University of Trento, winter semester 2017-2018, based on the work by Conneau et al: https://arxiv.org/pdf/1710.04087.pdf


## Dependencies

- python3 with virtualenv 
- PyTorch

The rest of the dependencies will be downloaded automatically as needed during installation and include (but are not limited to):
 
- gensim
- nltk
- MUSE  https://github.com/facebookresearch/MUSE
- CSTLemma

Pre-trained word vectors are downloaded. These word vectors were trained on a comparable corpora of Dutch and Russian Wikipedia data.

The articles and a list of their titles that were used to train these vectors will be downloaded as well.

## Installation

The install script will automatically download and install all the necessary dependencies. (Note that this could take a long time, particularly if pytorch needs to be installed.)

```
git clone git@github.com:kaleidoescape/hlt-2018.git
cd hlt-2018
./install.sh
```

## Training

The train script will automatically train the models.

```
./train.sh
```

