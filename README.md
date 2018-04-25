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
* [Using KrakenKeys] (#using-krakenkeys)
* [Playing a Midi](#playing-a-midi)
* [Our Results](#our-results)

## Installation


These instructions will assume you are using Anaconda and TensorFlow.

If you do not have [Anaconda] (https://conda.io/docs/user-guide/install/index.html) and [TensorFlow] (https://www.tensorflow.org/install/) install it first.


### Install Music21

If you are running Mac OS X or Ubuntu, you can just paste the following command into your terminal.

```
pip3 install music21
```

## Using KrakenKeys
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