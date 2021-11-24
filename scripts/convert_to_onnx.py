import argparse
import keras2onnx
import tensorflow.keras as keras
import onnx

parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-i", help="Input model", type=str)
parser.add_argument("--outfile", "-o", help="Output path", type=bool, default=False)
args = parser.parse_args()

keras_model = keras.models.load_model(args.infile, compile=False)
onnx_model = keras2onnx.convert_keras(keras_model)

output =[node.name for node in onnx_model.graph.output]
print('Outputs: ', output)

onnx.save(onnx_model,args.outfile)

onnx.checker.check_model(onnx_model)
