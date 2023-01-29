import stanza

#Class used to return sentence as a list of base words without any punctuation
class LexicalEditor():
    def __init__(self):
        self.punctuation = [('á', 'a'), ('ä', 'a'), ('č', 'c'), ('ď', 'd'), ('é','e'), ('í', 'i'), ('ĺ', 'l'), ('ľ', 'l'), \
                    ('ň', 'n'), ('ó', 'o'), ('ô', 'o'), ('ŕ', 'r'), ('š', 's'), ('ť', 't'), ('ú', 'u'), ('ý', 'y'), ('ž', 'z')]
        self.accepted_types = ["ADJ", "ADV", "NOUN", "NUM", "VERB"]
        self.natural_language_processor = stanza.Pipeline(lang='sk', processors='tokenize,mwt,pos,lemma')


    #Removes all punctuation for word
    def erase_punctuation(self, word):
        for p in self.punctuation:
            word = word.replace(p[0], p[1])

        return word


    #Returns true if the word is a adjective, noun, etc.
    def is_accepted_part_of_speech(self, pos):
        if (pos in self.accepted_types):
                return True
        return False


    #Returns sentence as a list of words
    def process_sentence(self, sentence) -> list:
        output_sentence = []

        doc = self.natural_language_processor(sentence)
        for s in doc.sentences:
            for word in s.words:
                if (self.is_accepted_part_of_speech(word.upos)):
                    output_sentence.append(self.erase_punctuation(word.lemma))

        return " ".join(output_sentence)
