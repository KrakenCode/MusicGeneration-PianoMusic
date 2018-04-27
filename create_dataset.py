#
# Code to parse midi and musicxml files for their piano notes/chords
#

import glob
from music21 import converter, instrument, note, chord
from tqdm import tqdm
import sys

'''
Parses midi and xml files in the given directory "input_data_directory." Converts
the file to instrument parts using music21 converter. Then pulls out only the
piano parts and parses those notes by converting them to strings. Returns a
list of all the piano notes found.
'''
def make_path_recursive(path):
    if path[len(path)-3:] == '/**':
        return path
    else:
        if path[len(path)-1:] == '/':
            path += '**'
        else:
            path += '/**'
        return path
    
def parse_midi_files(input_data_directory):
    
    input_data_directory = make_path_recursive(input_data_directory)
    
    notes = [] # list of all notes from midi files
    # iterate over all the files in the given directory
    for file in tqdm(glob.glob(input_data_directory, recursive=True)):
        # check that file is either midi or xml
        if not file.endswith('.mid') and not file.endswith('.xml'):
            continue

        # use music21 converter to parse the midi and partiion by instrument
        curr_midi = converter.parse(file)
        instrument_parts = instrument.partitionByInstrument(curr_midi)

        piano_to_parse = [] # list of piano music objects

        # catch midi files that aren't partitioned by instrument
        if instrument_parts is None:
            continue

        # iterate over all instrument parts and pick only piano
        for part in instrument_parts.parts:
            curr_instrum = str(part.recurse()).lower()
            if 'piano' in curr_instrum:
                piano_to_parse.append(part)

        # parse all of the notes in the piano parts
        for piano in piano_to_parse:
            piano_notes = piano.makeRests(fillGaps=True, inPlace=False).recurse()
            for element in piano_notes:
                if isinstance(element, note.Rest):
                    notes.append('rest')
                elif isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    curr_chord = sorted(list(str(n) for n in element.pitches))
                    notes.append('|'.join(curr_chord))

    return notes


'''
Yield successive chunk_size chunks from list notes.
'''
def divide_chunks(notes, chunk_size):
    # looping till length of notes
    for i in range(0, len(notes), chunk_size):
        yield notes[i:i + chunk_size]

'''
Divides the given list of notes into two files; one for questions and one
for answers. Uses chunk_size to determine the length of a question/answer.
This is how many elements each question/answer will have.

'''
def split_into_question_answer(notes, chunk_size):

    split_notes = list(divide_chunks(notes, chunk_size))

    questions = split_notes[:-1]
    answers = split_notes[1:]

    return questions, answers

'''
Writes the given questions and answers lists to individal files under the
names "questions.txt" and "answers.txt"
'''
def write_to_file(questions, answers):

    qfile = open('questions.txt', 'w')
    afile = open('answers.txt', 'w')

    for line in questions:
        qfile.write(' '.join(line))
        qfile.write('\n')

    for line in answers:
        afile.write(' '.join(line))
        afile.write('\n')

    qfile.close()
    afile.close()
      

if __name__ == "__main__":
    chunk_size = 5      # hard coded value
    if (len(sys.argv) < 2):
        print("Usage: "+ sys.argv[0]+ " path_to_midi_files")
        sys.exit(1)
    input_data_directory = sys.argv[1]
    notes = parse_midi_files(input_data_directory)
    questions, answers = split_into_question_answer(notes, chunk_size)
    write_to_file(questions, answers)
