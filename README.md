# MusicGeneration-PianoMusic

<div style="text-align:center">Spring 2018 - Repository for Team Ex Machina</div>

<div style="text-align:right"><img src="kraken_3.png" height="130"></div>


**KrakenKeys** is a research project exploring the role of artificial intelligence in developing
new musical compositions given a theme or genre.  Primarily this involves using algorithms such as
recurrent neural network, and lstm for generating musical notes.  It also involved using open source
tools such as [TensorFlow Seq2Seq](https://www.tensorflow.org/tutorials/seq2seq) for training the ai
on the note and chord patterns.  The project also used [Music21](http://web.mit.edu/music21/doc/about/what.html) for extracting piano notes and chords from midi and musicXML files.  This allows building a
creative tool for artists with artists block.

## Getting Started

* [Installation](#installation)
* [Using KrakenKeys](#using-krakenkeys)
* [Playing a Midi](#playing-a-midi)
* [Our Demo](#our-demo)
* [Team Members](#team-members)

## Installation

### Dependencies
| Name          | Versions      |
| ------------- |:-------------:|
| TensorFlow    | 1.5           |
| Keras         | 2.1.5         |
| Music21       | 5.2.0         |

These instructions will assume you are using Anaconda and TensorFlow.

If you do not have [Anaconda](https://conda.io/docs/user-guide/install/index.html) and [TensorFlow](https://www.tensorflow.org/install/) install it first.


### Install Music21

If you are running Mac OS X or Ubuntu, you can just paste the following command into your terminal.

```
pip3 install music21
```

## Using KrakenKeys

The generation of a song from scratch is broken up into three separate python files.
**create_dataset.py**, **train_model.py**, and **generate.py**. We have a included a small data set
in the directory **test_midi** which is in the github repo.

To generate the **questions.txt** and **answers.txt** files needed for training, run
```
python create_dataset.py <path_to_dataset>
```
Include a '\*\*' after the directory, **path_to_dataset/\*\***, to ensure that **create_dataset.py**
recursively grabs the midi files from the dataset. If you forget to include the '\*\*'s they will
be added anyway.


After the **questions.txt** and **answers.txt** text files have been generated, you can run **train_model.py**
to train the model. Run
```
python train_model.py <model_name>
```
to train a model with the name **\<model_name\>**.


Once you have a trained model you can use **generate.py** to create a song. Run
```
python generate.py <model_name>
```
where the **\<model_name\>** is the already trained model.

A random sequence of five notes will be chosen from either **answers.txt**
or **questions.txt** and be used to start the generation of a song. The song will be stored in a
file called **test.midi** which can be played using either **timidity** or **Windows Media Player**.

We have included an already trained model in the github repo which will produce
much better music compared to training a model on the small dataset that we
provided.

To generate a song using our pre-trained model start by running
```
python generate.py ourModel
```
which will generate a song using our model.

## Playing a MIDI

For our project we used timidity to play our midi files.

These instructions will assume you have **Ubuntu** or **Mac OS X**.
### Install Timidity

If you are running **Ubuntu**, you can just paste the following command into your terminal.

```
sudo apt-get install timidity timidity-interfaces-extra
```

If you are running **Mac OS X**, you can just paste the following command into your terminal.

```
brew install timidity
```

### Play Midi File

```
timidity <midi file>
```
## Our Demo

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/IDTTb6FbX-k/0.jpg)](http://www.youtube.com/watch?v=IDTTb6FbX-k)

## Team Members

Dalton Sumrall, Trase Westbrook, Austin Carpenter, Cassidy Matousek, Soe Than, Julia Vasquez
