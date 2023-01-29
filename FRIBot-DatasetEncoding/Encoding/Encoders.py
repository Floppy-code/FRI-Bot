from ntpath import join
import pickle
import numpy as np

from Encoding.EncoderBase import Encoder
from LexicalEditor.LexicalEditor import LexicalEditor

#Encoder for classifier network dataset
class EncoderClassifier(Encoder):
    def __init__(self):
        super().__init__()
        self.dictionary_counter = 0
        self.word_dictionary = {}
        self.lex_editor = LexicalEditor()
        self.dataset = None


    def encode_feature_set(self, input_file, output_file):
        #Loading dataset questions and appending IDs
        print("[INFO] Loading data", end = '')
        lines = self.load_dataset(input_file)
        print("...Done")
    
        #metadata = [x[0:4] for x in lines]
        questions = [x[5:10] for x in lines]
        #answers = [x[10:12] for x in lines]
        
        print("[INFO] Assigning unique IDs to questions", end = '')
        #Format: [(question, question_intent_id)]
        #Intents will be used in label set.
        questions_with_ids = []
        id_counter = 0
        for question_list in questions:
            for q in question_list:
                if q != '':
                    questions_with_ids.append((q, id_counter))
            id_counter += 1
        print("...Done")

        print("[INFO] Removing punctuation and building dictionary", end = '')
        #Removing punctuation, conversion to base form.
        for i in range(0, len(questions_with_ids)):
            #Processing
            processed = self.lex_editor.process_sentence(questions_with_ids[i][0])
            processed_id = questions_with_ids[i][1]
            questions_with_ids[i] = (processed, processed_id)

            #Appending unique words to dictionary
            for word in processed:
                if (word not in self.word_dictionary):
                    self.word_dictionary[word] = self.dictionary_counter
                    self.dictionary_counter += 1

        print("...Done")
        
        #Conversion to array of word vectors
        print("[INFO] Sentence vectorization", end = '')
        #Feature set format: [np vector of words, id]
        self.dataset = []
        for q in questions_with_ids:
            self.dataset.append((self.vectorize_sentence(q[0]), q[1]))
        print("...Done")

        print("[INFO] Saving dataset", end = '')
        self.save_dataset(output_file + '_dataset.dat')
        print("...Done")

        print("[INFO] Saving dictionary", end = '')
        self.save_dictionary(output_file + '_dictionary.dat')
        print("...Done")


    #Creates a vector of words for this sentence
    def vectorize_sentence(self, sentence):
        arr = np.zeros(len(self.word_dictionary))
        for word in sentence:
            arr[self.word_dictionary[word]] = 1.0

        return arr


    def load_dataset(self, filename):
        f = open(filename, encoding="utf8", mode = 'r')

        lines = []
        for line in f.readlines():
            lines.append(line.rstrip('\n').split(';'))

        return lines[1:]


    #Format: [(question, question_intent_id)]
    def save_dataset(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self.dataset, file)


    def save_dictionary(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self.word_dictionary, file)



#Encoder for LSTM network dataset
class EncoderLSTM(Encoder):

    def __init__(self):
        super().__init__()
        self.dataset = None

    def encode_feature_set(self, input_file, output_file):
        input_texts = []
        target_texts = []
        input_characters = set()
        target_characters = set()

        #Loading dataset questions and appending IDs
        print("[INFO] Loading data", end = '')
        lines = self.load_dataset(input_file)
        print("...Done")
    
        #metadata = [x[0:4] for x in lines]
        question_list = [x[1:6] for x in lines]
        answers = [x[6] for x in lines]

        #[WARN] Multiple questions with the same answers!
        for questions, answer in zip(question_list, answers):
            target_text = '\t' + answer + '\n' #start and stop characters only in target texts!
            for question in questions:
                if (question != ''):
                    input_texts.append(question)
                    target_texts.append(target_text)
                    for char in question:
                        if char not in input_characters:
                            input_characters.add(char)
            for char in target_text:
                if char not in target_characters:
                    target_characters.add(char)

        input_characters = sorted(list(input_characters))
        target_characters = sorted(list(target_characters))
        num_encoder_tokens = len(input_characters)
        num_decoder_tokens = len(target_characters)
        max_encoder_seq_length = max([len(txt) for txt in input_texts])
        max_decoder_seq_length = max([len(txt) for txt in target_texts])

        print('[INFO] Dataset: ')
        print("Number of samples:", len(input_texts))
        print("Number of unique input tokens:", num_encoder_tokens)
        print("Number of unique output tokens:", num_decoder_tokens)
        print("Max sequence length for inputs:", max_encoder_seq_length)
        print("Max sequence length for outputs:", max_decoder_seq_length)

        #Dictionaries of unique ids for each characters
        input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
        target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])
        
        #Reverse dictionaries so data can be transformed back into text
        reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
        reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

        #Feature and label set data
        encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32")
        decoder_input_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")
        decoder_target_data = np.zeros((len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")

        for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
            for t, char in enumerate(input_text):
                encoder_input_data[i, t, input_token_index[char]] = 1.0
            encoder_input_data[i, t + 1 :, input_token_index[" "]] = 1.0
            for t, char in enumerate(target_text):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                decoder_input_data[i, t, target_token_index[char]] = 1.0
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    decoder_target_data[i, t - 1, target_token_index[char]] = 1.0
            decoder_input_data[i, t + 1 :, target_token_index[" "]] = 1.0
            decoder_target_data[i, t:, target_token_index[" "]] = 1.0

        self.dataset = (encoder_input_data, decoder_input_data, decoder_target_data)
        print(f'[INFO] Saving dataset to {output_file}', end = '')
        self.save_to_file(output_file, self.dataset)
        print('...DONE')

        var_file = output_file + "_vars"
        print(f'[INFO] Saving dataset variables to {var_file}', end = '')        
        vars = (input_characters,
                target_characters,
                num_encoder_tokens,
                num_decoder_tokens,
                max_encoder_seq_length,
                max_decoder_seq_length,
                input_texts,
                target_texts)
        self.save_to_file(var_file, vars)
        print('...DONE')

        reverse_dict_file = output_file + "_reverse_dict"
        print(f'[INFO] Saving reverse dictionaries to {reverse_dict_file}', end = '')        
        reverse_dicts = (reverse_input_char_index,
                        reverse_target_char_index)
        self.save_to_file(reverse_dict_file, reverse_dicts)
        print('...DONE')

        backend_dict_file = output_file + "_backend_dictionaries"
        print(f'[INFO] Saving backend dictionaries to {backend_dict_file}', end = '')        
        backend_dicts = (input_token_index,
                        target_token_index,
                        reverse_target_char_index)
        self.save_to_file(backend_dict_file, backend_dicts)
        print('...DONE')


    def load_dataset(self, filename):
        f = open(filename, encoding="utf8", mode = 'r')

        lines = []
        for line in f.readlines():
            lines.append(line.rstrip('\n').split(';'))

        return lines[1:]


    def save_to_file(self, filename, object):
        with open(filename, 'wb') as file:
            pickle.dump(object, file)