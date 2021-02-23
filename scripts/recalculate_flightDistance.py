import numpy as np
import awkward as ak
keys = ["TagVarCSV_flightDistance2dVal", "TagVarCSV_flightDistance2dSig", "TagVarCSV_flightDistance3dVal", "TagVarCSV_flightDistance3dSig"]

def recalculate_flightDistance(tree, key):
    substitute_value = -99.

    vertex_mask = (tree["TagVarCSV_vertexCategory"].array() == 1) | (tree["TagVarCSV_vertexCategory"].array() == 2)

    branch = tree[key].array().copy()
    zeros = ak.broadcast_arrays(0., branch)[0]
    ret_arr = ak.where(vertex_mask, zeros, branch)
    return ak.to_awkward0(ret_arr)

def recalculate_flightDistance_from_arrays(value_branch, condition_branch):
    substitute_value = -99.
    vertex_mask = (condition_branch == 1) | (condition_branch == 2)

    branch = value_branch.copy()
    zeros = ak.broadcast_arrays(0., branch)[0]
    ret_arr = ak.where(vertex_mask, zeros, branch)
    return ak.to_akward0(ret_arr)
