import numpy as np
import awkward
import matplotlib.pyplot as plt
import uproot3 as u3
import os
import time
import argparse
from scripts.training_branches import key_lookup, DeepCSV_all_branches , new_ntuple_keys
from scripts.training_branches import file_comparison

def track_var_to_flat(arr, idx_low, idx_high):
    # arr = np.ones( (len(arr), 200))
    arr = awkward.to_awkward0(awkward.Array( [[[a if a != -9999. else -999. for a in ev[ka : kb + 1] ] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    # arr = awkward.to_awkward0(awkward.Array( [[ev[ka : kb] if len( ev[ka : kb] ) > 0 else [0.] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    # for i, a in enumerate(arr):
        # if len(a)== 0:
            # from IPython import embed;embed()
            # arr[i] = np.array([0.])
    return arr
    # return     # return awkward.to_awkward0(awkward.Array( [[ ev[ka : kb] if len(ev[ka : kb]) >0 else 0. for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
 

parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-i", help="Input root-file", type=str)
parser.add_argument("--offline", "-j", help="Flag for offline file", type=bool, default=False)
parser.add_argument("--output", "-o", help="Output Directory", type=str, default="converted_trees")
parser.add_argument("--key", "-k", help="Key, e.g. PuppiJet. or default", type=str, default="PuppiJet")
args = parser.parse_args()

branches_with_idx = ["TagVarCSV_trackJetDistVal",
                     "TagVarCSV_trackDeltaR",
                     "TagVarCSV_trackPtRatio",
                     "TagVarCSV_trackSip3dSig",
                     "TagVarCSV_trackSip2dSig",
                     "TagVarCSV_trackSip3dVal",
                     "TagVarCSV_trackSip2dVal",
                     "TagVarCSV_trackPtRel",
                     "TagVarCSV_trackDecayLenVal"]

branch_key = args.key

base_dir = args.output 
os.makedirs(base_dir, exist_ok = True)

SPLITS = 10

infile = args.infile
name = infile.split("/")[-1].split(".")[0]

print("Processing Datafile: {}".format(name))
if args.offline is True:
    online_tree = u3.open(infile)["deepntuplizer"]["tree"] 
else:
    online_tree = u3.open(infile)["btagana"]["ttree"] 

# out_file = u3.recreate(out_path, compression=None)

track_key_indicator = "TagVar_"

N_jets = -1
print("running on {} events!".format(N_jets if N_jets != -1 else "all"))

# branch_dict = {}
# branch_registration = {}


branch_dicts = { i_split: {"branch_dict": {}, "branch_registration": {}} for i_split in range(SPLITS) }

if branch_key == "PuppiJet":
    online_jet_pt = online_tree["PuppiJet.Jet_pt"].array()
else:
    online_jet_pt = online_tree["Jet_pt"].array()

# pt_mask = (online_jet_pt > 25.) & (online_jet_pt < 1000.)

on_mask = (online_jet_pt > 25.) & (online_jet_pt < 1000.)


n_total = len(online_tree["Jet_pt"].array()[on_mask].flatten())
n_starts = [0] + [ i * (n_total // SPLITS) for i in range(1, SPLITS) ]
n_ends = [ ns for ns in n_starts[1:] ] + [-1]

print("all keys:")
print(new_ntuple_keys)
print("-"*30)
# out_file = u3.recreate(out_path, compression=u3.ZLIB(7))
for online_key in new_ntuple_keys:
    if branch_key == "PuppiJet":
        if "PuppiJet" in online_key:
            print("processing key {}".format(online_key))
            tracking_index_low = online_tree['PuppiJet.Jet_nFirstTrkTagVar'].array()
            tracking_index_high = online_tree['PuppiJet.Jet_nLastTrkTagVar'].array()
            track_eta_index_low = online_tree['PuppiJet.Jet_nFirstTrkEtaRelTagVarCSV'].array()
            track_eta_index_high = online_tree['PuppiJet.Jet_nLastTrkEtaRelTagVarCSV'].array()
            if 'TagVarCSV_trackEtaRel' in online_key:
                arr = track_var_to_flat( online_tree[online_key].array(), track_eta_index_low, track_eta_index_high)[on_mask.flatten()][:N_jets]
                dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
                # dtype = np.dtype("f4")
                for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                    counts = arr[n_start: n_end].counts
                    branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts 
                # branch_dict["{}_counts".format(online_key)] = counts 
            elif any(["PuppiJet." + k == online_key for k in branches_with_idx ]):
                print("Flat var")
                arr = track_var_to_flat( online_tree[online_key].array(), tracking_index_low, tracking_index_high)[on_mask.flatten()][:N_jets]
                dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
                # dtype = np.dtype("f4")
                for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                    counts = arr[n_start: n_end].counts
                    branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts 
                # branch_dict["{}_counts".format(online_key)] = counts 
            else:
                dtype = np.dtype("f4")
                arr = online_tree[online_key].array()[on_mask].flatten()[:N_jets]
                # dtype = np.dtype("f4")

            for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                branch_dicts[i_split]["branch_registration"][online_key] = dtype
                branch_dicts[i_split]["branch_dict"][online_key] = arr[n_start: n_end]
            # branch_registration[online_key] = dtype
            # branch_dict[online_key] = arr
    else:
        if not "PuppiJet" in online_key:
            print("processing key {}".format(online_key))
            tracking_index_low = online_tree['Jet_nFirstTrkTagVar'].array()
            tracking_index_high = online_tree['Jet_nLastTrkTagVar'].array()
            # dtype = np.dtype("f4")
            track_eta_index_low = online_tree['Jet_nFirstTrkEtaRelTagVarCSV'].array()
            track_eta_index_high = online_tree['Jet_nLastTrkEtaRelTagVarCSV'].array()
            if 'TagVarCSV_trackEtaRel' in online_key:
                # from IPython import embed;embed()
                arr = track_var_to_flat( online_tree[online_key].array(), track_eta_index_low, track_eta_index_high)[on_mask.flatten()][:N_jets]
                dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
                # dtype = np.dtype(">f4")
                for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                    counts = arr[n_start: n_end].counts
                    branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts 
                # branch_dict["{}_counts".format(online_key)] = counts 
            elif any([k == online_key for k in branches_with_idx ]):
                print("Flat var")
                arr = track_var_to_flat( online_tree[online_key].array(), tracking_index_low, tracking_index_high)[on_mask.flatten()][:N_jets]
                dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
                # dtype = np.dtype(">f4")
                for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                    counts = arr[n_start: n_end].counts
                    branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts 
                # branch_dict["{}_counts".format(online_key)] = counts 
            else:
                arr = online_tree[online_key].array()[on_mask].flatten()[:N_jets]
                dtype = np.dtype("f4")

            for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
                branch_dicts[i_split]["branch_registration"][online_key] = dtype
                branch_dicts[i_split]["branch_dict"][online_key] = arr[n_start: n_end]
            # branch_registration[online_key] = dtype
            # branch_dict[online_key] = arr


for i_split in range(SPLITS):
    out_path =  os.path.join( base_dir, "{}_{}_{}.root".format(name, branch_key, i_split))
    print("Creating new tree: {}".format(out_path))
    with u3.recreate(out_path, compression=u3.ZLIB(6)) as out_file:
        print("Creating new tree for {}".format(branch_key))
        out_file["ttree"] = u3.newtree(branch_dicts[i_split]["branch_registration"])
        print("Creating branches")
        # s_time = time.time()
        out_file["ttree"].extend(branch_dicts[i_split]["branch_dict"])
        # from IPython import embed;embed()
        # e_time = time.time()
        # print("Total time needed for {0} events:\n{1:1.1f}".format(N_jets, e_time - s_time))
