from keras.models import load_model
from keras import backend as K
import tensorflow as tf
import numpy as np
import json

global graph
graph = tf.get_default_graph() 

# Set environment variables
model_file_name = 'model.h5'
lexicon_file_name = 'lexicon.json'

class TkPt_Tagger():

    def __init__(self):
        self.model = load_model(model_file_name)

        with open(lexicon_file_name, 'r') as f:
            lexicon_plus = json.loads(f.read())

        self.lexicon = lexicon_plus['lexicon']
        self.tags = lexicon_plus['tags']
        self.max_length = lexicon_plus['max_length']
        self.unknown_index = lexicon_plus['unknown_index']

    def X_toANN(self, x):
        x_aux = np.zeros(self.max_length)
        index = 0
        for word in x.split():
            if word in self.lexicon:
                x_aux[index] = self.lexicon[word]
            else:
                x_aux[index] = self.unknown_index
            index += 1
        return np.array(x_aux)

    def GetTag(self, prediction):
        for p in prediction:
            p = p.tolist()
            ind_max = p.index(max(p))
            tag = self.tags[ind_max]
            return tag

    def Classify(self, message):
    	# Transform the message
        message_input = np.array([self.X_toANN(message)])

    	# Predict
        # I had to declare the graph to ensure all the tensors were running on the same thread
        with graph.as_default():
            prediction = self.model.predict(message_input, batch_size=1, verbose=0)

    	# Process prediction
        tag = self.GetTag(prediction)

    	# Return tag
        return tag
