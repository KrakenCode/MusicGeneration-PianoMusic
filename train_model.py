from __future__ import print_function
from keras.models import Sequential
from keras import layers
import numpy as np
from six.moves import range
import os
import sys

MAXLEN = 5

class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'
    
'''
Sets up vocabulary (character table) for encoding and decoding using the 
questions and answers from the dataset. Retrieves the questions and answers
from the text files they were saved to.
Returns encoded questions and answers, and a vocabulary table
'''

def check_path(path):
    if path[len(path)-1:] != '/':
        path += '/'
    return path


def prepare_dataset():
    #answer_path = path_to_data + 'answers.txt'
    #question_path = path_to_data + 'questions.txt'    
    chars = get_all_notes('answers.txt').union(get_all_notes('questions.txt'))
    ctable = CharacterTable(chars)
    
    questions = []    # input
    answers = []     # output
    print('Generating data...')
    
    questions = get_tokenized_notes('questions.txt')
    answers = get_tokenized_notes('answers.txt')
    
    print('Vectorization...')
    # TODO are x and y the encoded questions/answers?
    x = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)
    y = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool) # TODO should this be len(answers) ?
    for i, sentence in enumerate(questions):
        x[i] = ctable.encode(sentence, MAXLEN)
    for i, sentence in enumerate(answers):
        y[i] = ctable.encode(sentence, MAXLEN)
    
    return x, y, ctable, chars

'''
This should be called twice with both the questions and answers output
from the generate_dataset.py functions
'''
def get_all_notes(filename):
    # creates a set of all possible tokens (notes) the NN can use
    try:
        file = open(filename)
    except:
        print("Must run create_dataset.py before training model. Exiting...")
        print("Usage: create_dataset.py path_to_midi_files")
        sys.exit(1)
    notes = set()
    for line in file.readlines():
        line = line.rstrip()
        tokens = line.split(' ')
        for token in tokens:
            notes.add(token)
        notes.add(' ')
    return notes

'''
This function goes through the file and tokenizes the lines into notes
returns a list of list of note tokens created from the given file
'''
def get_tokenized_notes(filename):
    file = open(filename)
    notes = []
    for line in file.readlines():
        line = line.rstrip()
        tokens = line.split(' ')
        
        if len(tokens) > MAXLEN:
            tokens = tokens[:MAXLEN]
        elif len(tokens) < MAXLEN:
            tokens = tokens + [' '] * (MAXLEN-len(tokens))
        
        notes.append(tokens)
    return notes

def clean_lines(lines):
    
    notes = []
    for line in lines:
        line = line.rstrip()
        tokens = line.split(' ')
        
        if len(tokens) > MAXLEN:
            tokens = tokens[:MAXLEN]
        elif len(tokens) < MAXLEN:
            tokens = tokens + [' '] * (MAXLEN-len(tokens))
        
        notes.append(tokens)
    return notes

"""Given a set of characters:
+ Encode them to a one hot integer representation
+ Decode the one hot integer representation to their character output
+ Decode a vector of probabilities to their character output
"""
class CharacterTable(object):
    '''
    Initialize character table.
    chars: Characters that can appear in the input. (this is the output from get_notes)
    '''
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    '''
    One hot encode given string C.
    num_rows: Number of rows in the returned one hot encoding. This is
                used to keep the # of rows for each data the same.
    '''
    def encode(self, C, num_rows):
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            x[i, self.char_indices[c]] = 1
        return x
    
    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ' '.join(self.indices_char[x] for x in x)
    
'''
Build the model given the number of tokens. Returns the model.
'''
def build_model(num_tokens):
    # Try replacing GRU, or SimpleRNN.
    RNN = layers.LSTM
    HIDDEN_SIZE = 128
    LAYERS = 3
    
    print('Build model...')
    model = Sequential()
    model.add(RNN(HIDDEN_SIZE, input_shape=(MAXLEN, num_tokens)))
    model.add(layers.RepeatVector(MAXLEN))
    
    for _ in range(LAYERS):
        model.add(RNN(HIDDEN_SIZE, return_sequences=True))
    
    # Apply a dense layer to the every temporal slice of an input. For each of step
    # of the output sequence, decide which character should be chosen.
    model.add(layers.TimeDistributed(layers.Dense(num_tokens)))
    model.add(layers.Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()

    return model

'''
Train the model each generation and show predictions against the validation
dataset. Takes the model, character table, questions (x) and answers (y), and 
batch size as inputs.
'''
def train_model(model, ctable, x, y, BATCH_SIZE, model_name):
    # Shuffle (x, y) in unison as the later parts of x will almost all be larger
    # digits.
    indices = np.arange(len(y))
    np.random.shuffle(indices)
    x = x[indices]
    y = y[indices]
    
    # Explicitly set apart 10% for validation data that we never train over.
    split_at = len(x) - len(x) // 10
    (x_train, x_val) = x[:split_at], x[split_at:]
    (y_train, y_val) = y[:split_at], y[split_at:]
    
    print('Training Data:')
    print(x_train.shape)
    print(y_train.shape)
    
    print('Validation Data:')
    print(x_val.shape)
    print(y_val.shape)
    
    # check if this file does not exist and save
    if model_name in os.listdir():
        model.load_weights(model_name)
    # change 1000 to number of epochs variable
    for iteration in range(1000, 1):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(x_train, y_train,
                  batch_size=BATCH_SIZE,
                  epochs=1,
                  validation_data=(x_val, y_val), shuffle=True)
        # Select 10 samples from the validation set at random so we can visualize
        # errors.
        # visualization of the training and whether we predicted correctly
        for i in range(10):
            ind = np.random.randint(0, len(x_val))
            rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
            preds = model.predict_classes(rowx, verbose=0)
            q = ctable.decode(rowx[0])
            correct = ctable.decode(rowy[0])
            guess = ctable.decode(preds[0], calc_argmax=False)
            print('Q', q, end=' ')
            print('T', correct, end=' ')
            if correct == guess:
                print(colors.ok + '☑' + colors.close, end=' ')
            else:
                print(colors.fail + '☒' + colors.close, end=' ')
            print(guess)  
    model.save_weights(model_name)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: " + sys.argv[0] + " model_name\n")
        sys.exit(1)
    model_name = sys.argv[1]
    x, y, ctable, chars = prepare_dataset()
    model = build_model(len(chars))
    BATCH_SIZE = 128
    train_model(model, ctable, x, y, BATCH_SIZE, model_name)