import numpy as np
import awkward
import matplotlib.pyplot as plt
import uproot3 as u3
import os
import time
import argparse
from training_branches import key_lookup, DeepCSV_all_branches , new_ntuple_keys
from training_branches import file_comparison

def track_var_to_flat(arr, idx_low, idx_high):
    arr = np.ones( (len(arr), 200))
    return awkward.to_awkward0(awkward.Array( [[ ev[ka : kb] for ka, kb in zip(kidx_a, kidx_b)] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
 

parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-i", help="Input root-file", type=str)
parser.add_argument("--offline", "-j", help="Flag for offline file", type=bool, default=False)
parser.add_argument("--output", "-o", help="Output Directory", type=str, default="converted_trees")
parser.add_argument("--key", "-k", help="Key, e.g. PuppiJet. or default", type=str, default="PuppiJet")
args = parser.parse_args()

branches_with_idx = ["TagVarCSV_trackJetDistVal", "TagVarCSV_trackDeltaR", "TagVarCSV_trackPtRatio", "TagVarCSV_trackSip3dSig", "TagVarCSV_trackSip2dSig", "TagVarCSV_trackSip3dVal", "TagVarCSV_trackSip2dVal", "TagVarCSV_trackPtRel", "TagVarCSV_trackDecayLenVal"]

branch_key = args.key

base_dir = args.output 
os.makedirs(base_dir, exist_ok = True)

infile = args.infile
name = infile.split("/")[-1].split(".")[0]

print("Processing Datafile: {}".format(name))
if args.offline is True:
    online_tree = u3.open(infile)["deepntuplizer"]["tree"] 
else:
    online_tree = u3.open(infile)["btagana"]["ttree"] 

out_path =  os.path.join( base_dir, "{}_{}.root".format(name, branch_key))
print("Creating new tree: {}",format(out_path))
# out_file = u3.recreate(out_path, compression=None)

track_key_indicator = "TagVar_"

N_jets = -1 
print("running on {} events!".format(N_jets if N_jets != -1 else "all"))

branch_dict = {}
branch_registration = {}

# out_file = u3.recreate(out_path, compression=u3.ZLIB(7))
with u3.recreate(out_path) as out_file:
    for online_key in new_ntuple_keys:
        if branch_key == "PuppiJet":
            if "PuppiJet" in online_key:
                print("processing key {}".format(online_key))
                tracking_index_low = online_tree['PuppiJet.Jet_nFirstTrkTagVar'].array()
                tracking_index_high = online_tree['PuppiJet.Jet_nLastTrkTagVar'].array()
                track_eta_index_low = online_tree['PuppiJet.Jet_nFirstTrkEtaRelTagVarCSV'].array()
                track_eta_index_high = online_tree['PuppiJet.Jet_nLastTrkEtaRelTagVarCSV'].array()
                if 'TagVarCSV_trackEtaRel' in online_key:
                    arr = track_var_to_flat( online_tree[online_key].array(), track_eta_index_low, track_eta_index_high)[:N_jets]
                    dtype = u3.newbranch(np.dtype("f8"), size="{}_counts".format(online_key),)
                    # dtype = np.dtype("f8")
                    counts = arr.counts
                    branch_dict["{}_counts".format(online_key)] = counts 
                elif any(["PuppiJet." + k == online_key for k in branches_with_idx ]):
                    print("Flat var")
                    arr = track_var_to_flat( online_tree[online_key].array(), tracking_index_low, tracking_index_high)[:N_jets]
                    dtype = u3.newbranch(np.dtype("f8"), size="{}_counts".format(online_key),)
                    # dtype = np.dtype("f8")
                    counts = arr.counts
                    branch_dict["{}_counts".format(online_key)] = counts 
                else:
                    dtype = np.dtype("f8")
                    arr = online_tree[online_key].array().flatten()[:N_jets]
                    dtype = np.dtype("f8")
                branch_registration[online_key] = dtype
                branch_dict[online_key] = arr
        else:
            if not "PuppiJet" in online_key:
                print("processing key {}".format(online_key))
                tracking_index_low = online_tree['Jet_nFirstTrkTagVar'].array()
                tracking_index_high = online_tree['Jet_nLastTrkTagVar'].array()
                # dtype = np.dtype("f8")
                track_eta_index_low = online_tree['Jet_nFirstTrkEtaRelTagVarCSV'].array()
                track_eta_index_high = online_tree['Jet_nLastTrkEtaRelTagVarCSV'].array()
                if 'TagVarCSV_trackEtaRel' in online_key:
                    arr = track_var_to_flat( online_tree[online_key].array(), track_eta_index_low, track_eta_index_high)[:N_jets]
                    dtype = u3.newbranch(np.dtype("f8"), size="{}_counts".format(online_key),)
                    # dtype = np.dtype(">f4")
                    counts = arr.counts
                    branch_dict["{}_counts".format(online_key)] = counts 
                elif any([k == online_key for k in branches_with_idx ]):
                    print("Flat var")
                    arr = track_var_to_flat( online_tree[online_key].array(), tracking_index_low, tracking_index_high)[:N_jets]
                    dtype = u3.newbranch(np.dtype("f8"), size="{}_counts".format(online_key),)
                    # dtype = np.dtype(">f4")
                    counts = arr.counts
                    branch_dict["{}_counts".format(online_key)] = counts 
                else:
                    arr = online_tree[online_key].array().flatten()[:N_jets]
                    dtype = np.dtype("f8")
                branch_registration[online_key] = dtype
                branch_dict[online_key] = arr



    print("Creating new tree for {}".format(branch_key))
    out_file["ttree"] = u3.newtree(branch_registration)
    print("Creating branches")
    # s_time = time.time()
    # from IPython import embed;embed()
    out_file["ttree"].extend(branch_dict)
    # e_time = time.time()
    # print("Total time needed for {0} events:\n{1:1.1f}".format(N_jets, e_time - s_time))
