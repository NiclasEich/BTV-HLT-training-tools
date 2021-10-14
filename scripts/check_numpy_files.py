import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input root-file", type=str)
args = parser.parse_args()

data = np.load( args.inp )

print("Shape:\t", data.shape)
print("Mean:\t", np.mean(data) )
print("Std:\t", np.std(data) )
print("Max:\t", np.max(data) )
print("Max:\t", np.max(data) )
print("isnan:\t", np.any( np.isnan(data) ) )
