from os import path
import tf2onnx
import tensorflow.keras as keras
import onnx

model_path = "/nfs/dust/cms/user/neich/BTV/Trainings/DeepJet_prod_07" 

keras_model = keras.models.load_model(path.join( model_path, "KERAS_check_best_model.h5"), compile=False)
onnx_model = tf2onnx.convert.from_keras(keras_model, output_path=path.join(model_path, 'DeepJet.onnx') )

from IPython import embed;embed()
# output =[node.name for node in onnx_model.graph.output]
# print('Outputs: ', output)

# onnx.save(onnx_model,p)

# onnx.checker.check_model(onnx_model)
