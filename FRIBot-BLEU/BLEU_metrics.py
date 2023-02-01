import pickle
import numpy as np
from nltk.translate.bleu_score import sentence_bleu

class BLEUMetrics():

    def __init__(self, reverse_target_characted_indexes, max_sentence_len):
        self.reverse_char_dir = reverse_target_characted_indexes
        self.max_sentence_length = max_sentence_len


    #BLEU score as is only works for a single sentence, we therefore use it in this case to calculate 
    #the average BLEU score for train set
    def BLEU_metrics_LSTM(self, y_true, y_pred):
        BLEU_score_sum = 0
        BLEU_score_average = 0

        for y_single_true, y_single_pred in zip(y_true, y_pred):
            print(y_single_true.shape)
            sentence_true, sentence_pred = self.LSTM_convert_to_sentences(y_single_true, y_single_pred)

            reference = [sentence_true.split(' ')]
            candidate = sentence_pred.split(' ')

            score = sentence_bleu(reference, candidate)

            BLEU_score_sum += score

            print(f"True:  {sentence_true}\nFalse: {sentence_pred}")
        
        BLEU_score_average = BLEU_score_sum / len(y_true)
        print(f"BLEU Score Avg: {BLEU_score_average}")

    def BLEU_metrics_DNN(self, y_true, y_pred):
        raise Exception("Not implemented yet!")


    def LSTM_convert_to_sentences(self, y_true, y_pred):
        sentence_true = ''
        sentence_pred = ''
        
        true_indexes = [np.argmax(x) for x in y_true]
        pred_indexes = [np.argmax(x) for x in y_pred]

        true_chars = [self.reverse_char_dir[x] for x in true_indexes]
        pred_chars = [self.reverse_char_dir[x] for x in pred_indexes]

        for x in true_chars:
            if (x == '\n'): 
                break
            sentence_true += x

        for x in pred_chars:
            if (x == '\n'): 
                break
            sentence_pred += x

        return (sentence_true, sentence_pred)
        

y = pickle.load(open('komplet_dataset', 'rb'))[2]
reverse_input_char_index, reverse_target_char_index = pickle.load(open('komplet_dataset_reverse_dict', 'rb'))

metrics = BLEUMetrics(reverse_target_char_index, 255)
print("DATA LOADED")

print(y.shape)
print(metrics.BLEU_metrics_LSTM(y[10:105], y[10:105]))
