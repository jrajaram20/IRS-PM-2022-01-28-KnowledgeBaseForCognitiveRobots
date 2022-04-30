import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
#from keras.models import load_model
import json
import random
import os
import tensorflow as tf

lemmatizer = WordNetLemmatizer()
sdir = os.path.dirname(os.path.realpath(__file__))+'/'
intents = json.loads(open(sdir+'speech/intents_bob.json').read())
words = pickle.load(open(sdir+'speech/words.pkl','rb'))
classes = pickle.load(open(sdir+'speech/classes.pkl','rb'))
model = tf.keras.models.load_model(sdir+'speech/chatbot_model.h5')

class chat1():
    def clean_up_sentence(self,sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self,sentence, words, show_details=True):
    # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(self,sentence, model):
    # filter out predictions below a threshold
        p = self.bow(sentence, words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.5
        #r = None
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        
    # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

        return return_list

    def getResponse(self,ints, intents_json):
        tag = "None"
        try:
            tag = ints[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if(i['tag']== tag):
                    result = random.choice(i['responses'])
                    break
        except:
            result = "index out of range"
        return result, tag

    def chatbot_response(self,msg):
        ints = self.predict_class(msg, model)
        res,tag = self.getResponse(ints, intents)
        #print(res)
        return res,tag

if __name__ == '__main__':
    c1 = chat1()
    msg = "find the position of redcoins"
    #res = c1.chatbot_response(msg)
    getr = c1.chatbot_response(msg)
    print(getr)
