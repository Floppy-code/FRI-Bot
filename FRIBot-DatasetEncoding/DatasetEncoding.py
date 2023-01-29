from Encoding.Encoders import EncoderClassifier, EncoderLSTM
from Vectorization.Vectorizer import Vectorizer

#Encoding - Encoding the whole dataset into one-hot vectors and output vectors

# encoder = EncoderClassifier()
# encoder.encode_feature_set('./data/komplet2.csv', './encoded/komplet2_encoded')

encoder = EncoderLSTM()
encoder.encode_feature_set('./data/final_dataset.csv', './encoded/final_dataset')
#encoder.encode_feature_set('D:/FRI/IngProj/fri-bot2/FRI-Bot/FRIBot-DatasetEncoding/data/final_dataset.csv', 'D:/FRI/IngProj/fri-bot2/FRI-Bot/FRIBot-DatasetEncoding/encoded/final_dataset')

# Vectorization - Turning any sentence into one-hot encoded vector

# vectorizer = Vectorizer('./encoded/otazky_encoded_dictionary.dat') 
# while True:
#     input_sentence = input()
#     if (input_sentence == 'e'):
#         break

#     vector = vectorizer.vectorize_sentence(input_sentence)
#     print(vector)
#     print(vectorizer.resentence(vector))