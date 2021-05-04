import numpy as np
import matplotlib.pyplot as plt
import uproot3 as u3
import os
import argparse
from training_branches import key_lookup, DeepCSV_all_branches 
from training_branches import file_comparison
from scripts.recalculate_flightDistance import recalculate_flightDistance
from functools import reduce
from matplotlib.ticker import AutoMinorLocator
from IPython import embed

plot_configs = {'Jet_pt':{"bins": np.arange(0, 1000, 25) , "log": True},
                'Jet_eta':{"bins": np.linspace(-4.2, 4.2, 20) , "log": False},
                'TagVarCSV_jetNSecondaryVertices':{"bins": np.arange(0, 10, 1) , "log": True},
                'TagVarCSV_trackSumJetEtRatio':{"bins": np.linspace(0, 10, 10) , "log": True, "underflow": -9999.},
                'TagVarCSV_trackSumJetDeltaR':{"bins": np.linspace(0, 4, 10) , "log": True, "underflow": -9999.},
                'TagVarCSV_vertexCategory':{"bins": np.arange(0, 3, 1) , "log": True, "underflow": -9999.},
                'TagVarCSV_trackSip2dValAboveCharm':{"bins": np.linspace(-1., 0.2, 25) , "log": True, "underflow": -9999.},
                'TagVarCSV_trackSip2dSigAboveCharm':{"bins": np.linspace(-70., 70., 20) , "log": True, "underflow": -9999.},
                'TagVarCSV_trackSip3dValAboveCharm':{"bins": np.linspace(-2., 2., 15), "log": True, "underflow": -9999.},
                'TagVarCSV_trackSip3dSigAboveCharm':{"bins": np.linspace(-40, 40, 30) , "log": True, "underflow": -9999.},
                'TagVarCSV_jetNTracksEtaRel':{"bins": np.linspace(0, 12, 12) , "log": False},
                'TagVar_trackEtaRel':{"bins": np.linspace(0, 12, 12) , "log": False},
                'TagVarCSV_vertexMass':{"bins": np.linspace(0, 120, 24) , "log": True, "underflow": -9999.},
                'TagVarCSV_vertexNTracks':{"bins": np.arange(0, 21, 1) , "log": True},
                'TagVarCSV_vertexEnergyRatio':{"bins": np.linspace(0, 2.5, 30) , "log": True, "underflow": -9999.},
                'TagVarCSV_vertexJetDeltaR':{"bins": np.linspace(0., 0.3, 30) , "log": True},
                'TagVarCSV_flightDistance2dVal':{"bins": np.linspace(0., 2.5, 40) , "log": True, "underflow": -9999.},
                'TagVarCSV_flightDistance2dSig':{"bins": np.linspace(0., 200, 20) , "log": True, "underflow": -9999.},
                'TagVarCSV_flightDistance3dVal':{"bins":  np.linspace(0., 20, 40), "log": True, "underflow": -9999.},
                'TagVarCSV_flightDistance3dSig':{"bins": np.linspace(0., 200, 40) , "log": True, "underflow": -9999.},
                'TagVarCSV_trackDecayLenVal':{"bins": np.arange(0, 6, 1) , "log": True},
                'TagVarCSV_trackSip2dSig':{"bins": np.arange(-100, 100, 20) , "log": True},
                'TagVarCSV_trackSip3dSig':{"bins": np.arange(-200, 200, 20) , "log": True},
                'TagVarCSV_trackPtRatio':{"bins": np.linspace(0, 0.3, 20) , "log": True},
                'TagVarCSV_trackDeltaR':{"bins": np.linspace(0., 0.3, 20) , "log": True},
                # 'TagVarCSV_jetNSelectedTracks':{"bins": np.arange(0, 60, 1) , "log": False},
                'Jet_nseltracks':{"bins": np.arange(0, 40, 1) , "log": False},
                'TagVarCSV_trackPtRel':{"bins": np.linspace(0., 25, 30) , "log": True},
                'TagVarCSV_trackJetDistVal':{"bins": np.linspace(-0.08, 0., 15) , "log": True},
                "Jet_isB": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isBB": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isGBB": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isLeptonicB": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isLeptonicB_C": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isC": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isGCC": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isCC": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isUD": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isS": {"bins": np.linspace(0, 1.1, 15), "log": True},
                "Jet_isG": {"bins": np.linspace(0, 1.1, 15), "log": True},
                }

def compute_ratios(hist_online, hist_offline, bin_edges):
    r_a = hist_online / np.sum(hist_online)
    r_b = hist_offline / np.sum(hist_offline)
    ratios = r_a / (r_b + 1e-9)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_widths = np.diff(bin_centers)
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    return ratios, bin_centers

def plot_histogram(datasets, dataset_names, key, name, category_name):
    fig, ax = plt.subplots(1, 1)
    fig.subplots_adjust(hspace=0)

    for i_hist, (dataset, name) in enumerate(zip(datasets, dataset_names)):
        if name == "default": 
            hatch ="/"
        else:
            hatch = None
        ax.hist(dataset, bins = plot_configs[key]["bins"], label = "{0} $\mu=${1:1.2f} $\sigma$={2:1.2f}".format(name, np.mean(dataset), np.std(dataset)), alpha=0.5, density=True, hatch=hatch)
    ax.legend()
    if plot_configs[key]["log"] is True:
        ax.set_yscale('log')
    ax.set_ylabel("N, normalized", fontsize=15)
    ax.set_title("{}\n{}".format(name, category_name), fontsize=15)
    ax.grid(which='both', axis='y',linestyle="dashed")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    try:
        textstr = "Hello :)"
        # textstr = "Online:\nmin {0:1.2f}\nmax {1:1.2f}\nOffline:\nmin {2:1.2f}\nmax {3:1.2f}".format( np.min(online_data), np.max(online_data), np.min(offline_data), np.max(offline_data))
        # if tot_underflows != None:
            # textstr += "\nUnderflows: {}".format(tot_underflows)
    except ValueError as e:
        print(e)
        textstr = "Error"
    ax.text(0.8, 0.75, textstr, transform=ax.transAxes, fontsize=8,
                    verticalalignment='top', bbox=props)



    fig.savefig( os.path.join(plot_dir, "{}_{}.pdf".format(name, key)))
    fig.savefig( os.path.join(plot_dir, "{}_{}.png".format(name, key)))
    plt.close()

parser = argparse.ArgumentParser()
parser.add_argument("--offline", "-j", help="Input root-file for offline", type=str, default="/afs/cern.ch/work/n/neich/public/new_offline_files/TT_TuneCP5_14TeV-powheg-pythia8_PU200_new.root")
parser.add_argument("--output", "-o", help="Output directory TAG. For example v02 to add a v02 at the end of the root-file", type=str, default="v00")
parser.add_argument("--target", "-t", help="Target directory.", type=str, default="./dataset_comp")
args = parser.parse_args()

offline_file = args.offline
output_tag = args.output
target_dir = args.target
process_name = offline_file.split("/")[-1].split(".")[0]


base_dir = os.path.join(target_dir, "{}_{}".format(process_name, output_tag))
os.makedirs(base_dir, exist_ok=True)

offline_tree = u3.open(offline_file)["btagana"]["ttree"]

plot_keys = key_lookup.keys()

offline_cleaning_keys = ["TagVarCSV_flightDistance2dVal", "TagVarCSV_flightDistance2dSig", "TagVarCSV_flightDistance3dVal", "TagVarCSV_flightDistance3dSig"]

# category_names = ["b_jets", "bb+gbb_jets", "lepb_jets", "c+cc+gcc_jets", "uds_jets", "g_jes", "all_jets"]
# categories = [ ['isB'], ['isBB', 'isGBB'], ['isLeptonicB', 'isLeptonicB_C'], ['isC', 'isCC', 'isGCC'], ['isUD', 'isS'], ['isG'], ['isB','isBB', 'isGBB', 'isLeptonicB', 'isLeptonicB_C', 'isC', 'isCC', 'isGCC','isUD', 'isS', 'isG']]

categories = ["all"]
category_names = ["all"]

dataset_names = ["", "PuppiJet.", "CaloJet."]

for cat, cat_name in zip(categories, category_names):
    plot_dir = os.path.join( base_dir, cat_name )
    os.makedirs(plot_dir, exist_ok=True)

    # offline_mask = reduce(np.logical_or , [ offline_tree[k].array() == 1 for k in cat])

    # offline_mask = off_pt_mask & offline_mask

    for key  in plot_configs.keys():
        try:
            data = [ offline_tree[ d_name + key].array().flatten() for d_name in dataset_names]
        except:
            print("error during key:\t{}".format(key))
            embed()

        # if key in offline_cleaning_keys:
            # offline_data = recalculate_flightDistance(offline_tree, key)

        print("key:\t", key)
        # if "vertex" in key:
            # print("Setting Values to 0:\nOnline:\t{}\nOffline:\t{}".format(sum(np.invert(on_nSV_mask)), sum(np.invert(off_nSV_mask))))
            # online_data[np.invert(on_nSV_mask)] *= 0.
            # offline_data[np.invert(off_nSV_mask)] *= 0.

        # online_data = online_data[online_mask].flatten()
        # offline_data = offline_data[offline_mask].flatten()

        if plot_configs[key].get("underflow", False) is not False:
            masks = [ d != plot_configs[key]["underflow"] for d in data]
            data = [ d[m] for d,m in zip(data, masks) ]

        print("Starting plotting")
        plot_histogram(data, ["default", "PuppiJet", "CaloJet"], key, process_name, cat_name)
