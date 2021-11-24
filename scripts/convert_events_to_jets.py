import os
import time
import math
import awkward
import argparse
import numpy as np
import uproot3 as u3
from scripts.training_branches import key_lookup, DeepCSV_all_branches , new_ntuple_keys, default_values
from scripts.training_branches import file_comparison

def track_var_to_flat(arr, idx_low, idx_high, **kwargs):
    if kwargs.get("default", None) is not None:
        arr = awkward.to_awkward0(awkward.Array( [[[a if a != kwargs["default"]["old"] else kwargs["default"]["new"] for a in ev[ka : kb + 1] ] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    else:
        arr = awkward.to_awkward0(awkward.Array( [[[a for a in ev[ka : kb + 1] ] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    return arr

    # arr = awkward.to_awkward0(awkward.Array( [[ev[ka : kb] if len( ev[ka : kb] ) > 0 else [0.] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    # for i, a in enumerate(arr):
        # if len(a)== 0:
            # from IPython import embed;embed()
            # arr[i] = np.array([0.])
    # return     # return awkward.to_awkward0(awkward.Array( [[ ev[ka : kb] if len(ev[ka : kb]) >0 else 0. for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)


parser = argparse.ArgumentParser()
parser.add_argument("--infile", "-i", help="Input root-file", type=str)
parser.add_argument("--offline", "-j", help="Flag for offline file", type=bool, default=False)
parser.add_argument("--output", "-o", help="Output Directory", type=str, default="converted_trees")
parser.add_argument("--key", "-k", help="Key, e.g. PuppiJet. or default", type=str, default="default")
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
branches_with_idx_cpf =[
    'Cpfcan_BtagPf_trackEtaRel',
    'Cpfcan_BtagPf_trackPtRel',
    'Cpfcan_BtagPf_trackPPar',
    'Cpfcan_BtagPf_trackDeltaR',
    'Cpfcan_BtagPf_trackPParRatio',
    'Cpfcan_BtagPf_trackSip2dVal',
    'Cpfcan_BtagPf_trackSip2dSig',
    'Cpfcan_BtagPf_trackSip3dVal',
    'Cpfcan_BtagPf_trackSip3dSig',
    'Cpfcan_BtagPf_trackJetDistVal',
    'Cpfcan_ptrel',
    'Cpfcan_drminsv',
    'Cpfcan_VTX_ass',
    'Cpfcan_puppiw',
    'Cpfcan_chi2',
    'Cpfcan_quality',
    ]
branches_with_idx_npf =[
    'Npfcan_ptrel',
    'Npfcan_deltaR',
    'Npfcan_isGamma',
    'Npfcan_HadFrac',
    'Npfcan_drminsv',
    'Npfcan_puppiw',
    ]
branches_with_idx_sv =[
    'sv_pt',
    'sv_deltaR',
    'sv_mass',
    'sv_ntracks',
    'sv_chi2',
    'sv_normchi2',
    'sv_dxy',
    'sv_dxysig',
    'sv_d3d',
    'sv_d3dsig',
    'sv_costhetasvpv',
    'sv_enratio'
]

branch_key = args.key
base_dir = args.output

infile = args.infile
name = infile.split("/")[-1].split(".")[0]

print("Creating {}".format(base_dir))
print("exists? {}".format( os.path.isdir(base_dir) ))

os.makedirs(base_dir, exist_ok = True)

maxJets = 500000

print("Processing Datafile: {}".format(name))
if args.offline is True:
    online_tree = u3.open(infile)["deepntuplizer"]["tree"]
else:
    online_tree = u3.open(infile)["btagana"]["ttree"]

track_key_indicator = "TagVar_"
N_jets = -1
print("running on {} events!".format(N_jets if N_jets != -1 else "all"))

if branch_key == "PuppiJet":
    online_jet_pt = online_tree["PuppiJet.Jet_pt"].array()
else:
    online_jet_pt = online_tree["Jet_pt"].array()
    online_jet_npfc = online_tree[key_lookup["nCpfcand"]].array()

on_mask = (online_jet_pt > 25.) & (online_jet_pt < 1000.)
on_mask = on_mask & online_jet_npfc > -1


n_total = len(online_tree["Jet_pt"].array()[on_mask].flatten())

print ("Number of entries:",online_tree.numentries)
print ("Number of jets:",n_total)
SPLITS = int(math.ceil(n_total/maxJets))
print ("Into N files:",SPLITS)
print ("With ~jets per file:", n_total/SPLITS)

branch_dicts = { i_split: {"branch_dict": {}, "branch_registration": {}} for i_split in range(SPLITS) }

n_starts = [0] + [ i * (n_total // SPLITS) for i in range(1, SPLITS) ]
n_ends = [ ns for ns in n_starts[1:] ] + [-1]

tracking_index_low = online_tree['Jet_nFirstTrkTagVarCSV'].array()
tracking_index_high = online_tree['Jet_nLastTrkTagVarCSV'].array()
cpf_index_low = online_tree['DeepFlavourInput_NFirst_charged'].array()
cpf_index_high = online_tree['DeepFlavourInput_NLast_charged'].array()
npf_index_low = online_tree['DeepFlavourInput_NFirst_neutral'].array()
npf_index_high = online_tree['DeepFlavourInput_NLast_neutral'].array()
sv_index_low = online_tree['DeepFlavourInput_NFirst_sv'].array()
sv_index_high = online_tree['DeepFlavourInput_NLast_sv'].array()
track_eta_index_low = online_tree['Jet_nFirstTrkEtaRelTagVarCSV'].array()
track_eta_index_high = online_tree['Jet_nLastTrkEtaRelTagVarCSV'].array()

for online_key in new_ntuple_keys:
    kwargs = {}

    if 'TagVarCSV_trackEtaRel' in online_key:
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
        arr = track_var_to_flat( online_tree[online_key].array(), track_eta_index_low, track_eta_index_high, **kwargs)[on_mask.flatten()][:N_jets]
        dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
        for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
            counts = arr[n_start: n_end].counts
            branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts
    elif any([k == online_key for k in branches_with_idx ]):
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
        arr = track_var_to_flat( online_tree[online_key].array(), tracking_index_low, tracking_index_high, **kwargs)[on_mask.flatten()][:N_jets]
        dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
        for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
            counts = arr[n_start: n_end].counts
            branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts
    elif any([k == online_key for k in branches_with_idx_cpf ]):
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
        arr = track_var_to_flat( online_tree[key_lookup[online_key]].array(), cpf_index_low, cpf_index_high, **kwargs)[on_mask.flatten()][:N_jets]
        dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
        for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
            counts = arr[n_start: n_end].counts
            branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts
    elif any([k == online_key for k in branches_with_idx_npf ]):
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
        arr = track_var_to_flat( online_tree[key_lookup[online_key]].array(), npf_index_low, npf_index_high, **kwargs)[on_mask.flatten()][:N_jets]
        dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
        for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
            counts = arr[n_start: n_end].counts
            branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts
    elif any([k == online_key for k in branches_with_idx_sv ]):
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
        arr = track_var_to_flat( online_tree[key_lookup[online_key]].array(), sv_index_low, sv_index_high, **kwargs)[on_mask.flatten()][:N_jets]
        dtype = u3.newbranch(np.dtype("f4"), size="{}_counts".format(online_key),)
        for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
            counts = arr[n_start: n_end].counts
            branch_dicts[i_split]["branch_dict"]["{}_counts".format(online_key)] = counts
    else:
        arr = online_tree[key_lookup[online_key]].array()[on_mask].flatten()[:N_jets]
        if default_values.get(online_key, None) is not None:
            kwargs["default"] = default_values[online_key]
            arr[ arr == kwargs["default"]["old"] ] = kwargs["default"]["new"]
        dtype = np.dtype("f4")

    for i_split, (n_start, n_end) in enumerate(zip(n_starts, n_ends)):
        branch_dicts[i_split]["branch_registration"][online_key] = dtype
        branch_dicts[i_split]["branch_dict"][online_key] = arr[n_start: n_end]

for i_split in range(SPLITS):
    out_path =  os.path.join( base_dir, "{}_{}_{}.root".format(name, branch_key, i_split))
    print("Creating new tree: {}".format(out_path))
    with u3.recreate(out_path, compression=u3.ZLIB(6)) as out_file:
        print("Creating new tree for {}".format(branch_key))
        out_file["ttree"] = u3.newtree(branch_dicts[i_split]["branch_registration"])
        print("Creating branches")
        out_file["ttree"].extend(branch_dicts[i_split]["branch_dict"])
