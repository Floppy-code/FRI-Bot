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
            reference = [y_single_true.split(' ')]
            candidate = y_single_pred.split(' ')

            score = sentence_bleu(reference, candidate)

            BLEU_score_sum += score
            #print(f"True:  {y_single_true}\nFalse: {y_single_pred}") #DEBUG
        
        BLEU_score_average = BLEU_score_sum / len(y_true)
        print(f"BLEU Score Avg: {BLEU_score_average}")

    def BLEU_metrics_DNN(self, y_true, y_pred):
        raise Exception("Not implemented yet!")