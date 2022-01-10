import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
import sys
import os
import argparse
sys.modules["keras"] = tf.keras

parser = argparse.ArgumentParser()
parser.add_argument("model")
parser.add_argument("--output", "-o", help="Output path", default="./", type=str)
args = parser.parse_args()

model_name = args.model 
out_path = args.output

model = load_model(model_name)
model.save_weights(os.path.join(out_path, 'DeepCSV_weights.h5'))


#from models import dense_model
from DeepJetCore.training.training_base import training_base

#from keras.layers import Dense, Dropout, Flatten, Convolution2D, merge, Convolution1D, Conv2D, BatchNormalization
from keras.layers import Dense, Dropout, Flatten,Concatenate, Lambda, Convolution2D, LSTM, Convolution1D, Conv2D,GlobalAveragePooling1D, GlobalMaxPooling1D,TimeDistributed, BatchNormalization
from keras.models import Model, Sequential

nclasses = 4

model = Sequential( [

     Dense(100, activation='relu',kernel_initializer='lecun_uniform', input_shape=(66,1)),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(100, activation='relu',kernel_initializer='lecun_uniform'),
     Dense(nclasses, activation='softmax',kernel_initializer='lecun_uniform')
])

arch = model.to_json()
with open(os.path.join( out_path, 'DeepCSV_arch.json'), 'w') as arch_file:
    arch_file.write(arch)
