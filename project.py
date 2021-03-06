from flask import Flask
from flask import request, jsonify
from flask import render_template
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import MaxPooling1D
from keras.layers import Flatten, GlobalMaxPooling1D, GlobalAveragePooling1D
from keras.layers import Dropout, BatchNormalization, Input, SpatialDropout1D
from keras.layers import Dense, Bidirectional, concatenate
from keras.models import Model
from keras.optimizers import Adam
import keras.backend as K
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense,Input
from numpy import asarray
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

x=[]
f = open('newtok2.txt', 'r')
x = f.readlines()
f.close()


#config = tf.ConfigProto( intra_op_parallelism_threads=1,inter_op_parallelism_threads=1)
#sess = tf.Session(config=config)
#graph = tf.get_default_graph()
sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()
t  = Tokenizer(40000)
t.fit_on_texts(x)
import nltk
nltk.download('punkt')
from nltk import word_tokenize


app = Flask(__name__)

set_session(sess)
model_dwn = load_model('HHH.hdf5')
#model_dwn = load_model('unbiased_model.hdf5',custom_objects={'SeqSelfAttention': SeqSelfAttention})
model_dwn._make_predict_function()

@app.route('/')
@app.route("/project")
def project():
    return render_template('index.html', methods=['GET', 'POST'])


@app.route('/', methods=['GET', 'POST'])
@app.route("/project",methods=['GET', 'POST'])
def project_post():
    
    '''
    For rendering results on HTML GUI
    '''
    stop_words = ['a', 'and', 'are']
    input_string = request.form['comment']
    text_tokens = word_tokenize(input_string)
    #int_features = [int(x) for x in request.form.values()]
    tokens_without_sw = [word for word in text_tokens if not word in stop_words]
    # final_features = [np.array(int_features)]
    filtered_sentence = (" ").join(tokens_without_sw)
    lower_sentence = filtered_sentence.lower()
    encoded_sample = t.texts_to_sequences([lower_sentence])
# defining a max size for padding.
    max_len = 150
# padding the vectors of each datapoint to fixed length of 100.
    pad_sample = pad_sequences(encoded_sample,maxlen = max_len,padding='post')

    global sess
    global graph
    with graph.as_default():
    	set_session(sess)
    	results = model_dwn.predict(pad_sample)
    	#results = sum(results)
    	# return str(results)
    if results > 0.5 and len(lower_sentence) > 2:
        return render_template('index.html', prediction_text='Toxic', p='{}'.format(input_string), result='{}'.format(results), methods=['GET', 'POST'])
    else:
        return render_template('post.html', prediction_text='Not Toxic', p='{}'.format(lower_sentence), result='{}'.format(results),  methods=['GET', 'POST'])
        
    


