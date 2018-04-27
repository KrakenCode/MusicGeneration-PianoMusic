'''


'''
import create_dataset as data
import generate as gen
import model as md
import sys

MAXLEN = 5
ctable=[]   # character table
model=[]    # the NN

'''
Run the model with a different command depending on what step the user is one.
Can either prepare the dataset (questions & answers), build/traing the model, or
generate new music. Three commands are: dataset, train or generate. Can also
run without a command to see usage.
'''
def run():
    # all commands will have at least 3 arguments
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    # command is which step we want to use
    command=sys.argv[1]
    if command in "dataset":                        # prepare the dataset
        input_data_directory = sys.argv[2]
        run_create_dataset(input_data_directory)
    elif command in "train":   # build and train the model
        model_name = sys.argv[2]
        run_model_train(model_name)
    elif command in "generate":                     # generate new music
        if len(sys.argv) != 4:
            print_usage()
            sys.exit(1)
        note_sequence = sys.argv[2]
        model_path = sys.argv[3]
        run_generate(note_sequence, model_path)
    else:
        print_usage()
'''
Takes the input data directory and searches for all midi files in that directory.
Converts them to questions and answers, writes those to a file and returns the
questions/answers lists.
'''       
def run_create_dataset(input_data_directory):
    chunk_size = 5      # hard coded value
    notes = data.parse_midi_files(input_data_directory)
    questions, answers = data.split_into_question_answer(notes, chunk_size)
    data.write_to_file(questions, answers)

'''
Prepares the one-hot vectors for the model, and then builds and trains the model.
'''
def run_model_train(model_name):
    x, y, ctable, chars = md.prepare_dataset()
    model = md.build_model(len(chars))
    BATCH_SIZE = 128
    md.train_model(model, ctable, x, y, BATCH_SIZE,model_name)

'''
Generates new music given the output of the model and a note sequence.
'''    
def run_generate(note_sequence, model_path):
    new_song = gen.generate(note_sequence, ctable, model)
    music_objects=gen.create_music_objects(new_song)
    gen.write_to_file(music_objects, "test.midi") # hard coded midi name

'''
Prints the usage.
'''
def print_usage():
    print("Please run with one of the three following commands: dataset, train or generate\n")
    print("Usage: "+sys.argv[0]+"dataset path_to_midi_files")
    print("OR\t" + sys.argv[0] + "train model_name path_to_question&answer\n")
    print("OR\t" + sys.argv[0] + "generate note_sequence_file model_name\n")

if __name__ == "__main__":
    run()