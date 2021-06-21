import matplotlib.pyplot as plt
import uproot3 as u3
import os
import argparse
import numpy as np
from training_branches import key_lookup, DeepCSV_all_branches , new_ntuple_keys
from training_branches import file_comparison
from scripts.recalculate_flightDistance import recalculate_flightDistance
from functools import reduce
from matplotlib.ticker import AutoMinorLocator

plot_configs = {'jet_pt':{"bins": np.arange(0, 1000, 25) , "log": True},
                'jet_eta':{"bins": np.linspace(-4.2, 4.2, 20) , "log": False},
                'TagVarCSV_jetNSecondaryVertices':{"bins": np.arange(0, 10, 1) , "log": True},
                'TagVarCSV_trackSumJetEtRatio':{"bins": np.linspace(0, 10, 10) , "log": True, "underflow": -999.},
                'TagVarCSV_trackSumJetDeltaR':{"bins": np.linspace(0, 5, 10) , "log": True, "underflow": -999.},
                'TagVarCSV_vertexCategory':{"bins": np.arange(0, 3, 1) , "log": True, "underflow": -999.},
                'TagVarCSV_trackSip2dValAboveCharm':{"bins": np.linspace(-1., 0.2, 25) , "log": True, "underflow": -999.},
                'TagVarCSV_trackSip2dSigAboveCharm':{"bins": np.linspace(-300., 400., 20) , "log": True, "underflow": -999.},
                'TagVarCSV_trackSip3dValAboveCharm':{"bins": np.linspace(-2., 2., 15), "log": True, "underflow": -999.},
                'TagVarCSV_trackSip3dSigAboveCharm':{"bins": np.linspace(-1100, 500, 30) , "log": True},
                'TagVarCSV_jetNTracksEtaRel':{"bins": np.linspace(0, 12, 12) , "log": False},
                'TagVarCSV_trackEtaRel':{"bins": np.linspace(0, 12, 12) , "log": False},
                'TagVarCSV_vertexMass':{"bins": np.linspace(0, 550, 24) , "log": True},
                'TagVarCSV_vertexNTracks':{"bins": np.arange(0, 32, 1) , "log": True},
                'TagVarCSV_vertexEnergyRatio':{"bins": np.linspace(0, 200, 30) , "log": True},
                'TagVarCSV_vertexJetDeltaR':{"bins": np.linspace(0., 0.3, 30) , "log": True},
                'TagVarCSV_flightDistance2dVal':{"bins": np.linspace(0., 2.5, 40) , "log": True},
                'TagVarCSV_flightDistance2dSig':{"bins": np.linspace(0., 1600, 20) , "log": True},
                'TagVarCSV_flightDistance3dVal':{"bins":  np.linspace(0., 40, 40), "log": True},
                'TagVarCSV_flightDistance3dSig':{"bins": np.linspace(0., 1600, 40) , "log": True},
                'TagVarCSVTrk_trackDecayLenVal':{"bins": np.arange(0, 6, 1) , "log": True},
                'TagVarCSVTrk_trackSip2dSig':{"bins": np.arange(-300, 400, 20) , "log": True},
                'TagVarCSVTrk_trackSip3dSig':{"bins": np.arange(-800, 800, 20) , "log": True},
                'TagVarCSVTrk_trackPtRatio':{"bins": np.linspace(0, 0.3, 20) , "log": True},
                'TagVarCSVTrk_trackDeltaR':{"bins": np.linspace(0., 0.3, 20) , "log": True},
                'TagVarCSV_jetNSelectedTracks':{"bins": np.arange(0, 60, 1) , "log": False},
                'TagVarCSVTrk_trackPtRel':{"bins": np.linspace(0., 60, 30) , "log": True},
                'TagVarCSVTrk_trackJetDistVal':{"bins": np.linspace(-0.08, 0., 15) , "log": True}
                }

def compute_ratios(hist_online, hist_offline, bin_edges):
    r_a = hist_online / np.sum(hist_online)
    r_b = hist_offline / np.sum(hist_offline)
    ratios = r_a / (r_b + 1e-9)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_widths = np.diff(bin_centers)
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    return ratios, bin_centers


def plot_histogram(online_data, key, name, category_name):
    fig, ax = plt.subplots(1, 1)
    fig.subplots_adjust(hspace=0)

    hist_online, bin_edges = np.histogram( online_data, bins=plot_configs[key]["bins"])

    ax.hist( online_data, bins = plot_configs[key]["bins"],  label = "Online $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(online_data), np.std(online_data)), color="red", alpha=0.5, density=True)
    ax.legend()
    if plot_configs[key]["log"] is True:
        ax.set_yscale('log')
    ax.set_ylabel("N, normalized", fontsize=15)
    ax.set_title("{}\n{}".format(name, category_name), fontsize=15)
    ax.grid(which='both', axis='y',linestyle="dashed")

    # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # # place a text box in upper left in axes coords
    # try:
        # textstr = "Online:\nmin {0:1.2f}\nmax {1:1.2f}\nOffline:\nmin {2:1.2f}\nmax {3:1.2f}".format( np.min(online_data), np.max(online_data), np.min(offline_data), np.max(offline_data))
        # if tot_underflows != None:
            # textstr += "\nUnderflows: {}".format(tot_underflows)
    # except ValueError as e:
        # print(e)
        # textstr = "Error"
    # ax.text(0.8, 0.75, textstr, transform=ax[0].transAxes, fontsize=8,
                    # verticalalignment='top', bbox=props)


    ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.tick_params(which='minor', length=4, color='black')

    fig.savefig( os.path.join(plot_dir, "{}_{}.png".format(name, key)))
    fig.savefig( os.path.join(plot_dir, "{}_{}.pdf".format(name, key)))
    plt.close()

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-i", help="Input root-file", type=str)
parser.add_argument("--output", "-o", help="Output directory TAG. For example v02 to add a v02 at the end of the root-file", type=str, default="v00")
parser.add_argument("--target", "-t", help="Target directory.", type=str, default="./dataset_comp")
args = parser.parse_args()

online_file = args.file
target_dir = args.target
output_tag = args.output
process_name = online_file.split("/")[-1].split(".")[0]

base_dir = os.path.join(target_dir, "{}_{}".format(process_name, output_tag))
os.makedirs(base_dir, exist_ok=True)

online_tree =  u3.open(online_file)["ttree"]

plot_keys = key_lookup.keys()

online_jet_pt = online_tree[key_lookup["jet_pt"]].array()

on_pt_mask = (online_jet_pt > 25.) & (online_jet_pt < 1000.)

online_nSV = online_tree[key_lookup["TagVarCSV_jetNSecondaryVertices"]].array()

on_nSV_mask = online_nSV > 0


category_names = ["b_jets", "bb+gbb_jets", "lepb_jets", "c+cc+gcc_jets", "uds_jets", "g_jes", "all_jets"]
categories = [ ['isB'], ['isBB', 'isGBB'], ['isLeptonicB', 'isLeptonicB_C'], ['isC', 'isCC', 'isGCC'], ['isUD', 'isS'], ['isG'], ['isB','isBB', 'isGBB', 'isLeptonicB', 'isLeptonicB_C', 'isC', 'isCC', 'isGCC','isUD', 'isS', 'isG']]

for cat, cat_name in zip(categories, category_names):
    plot_dir = os.path.join( base_dir, cat_name )
    os.makedirs(plot_dir, exist_ok=True)

    online_mask = reduce(np.logical_or , [ online_tree[key_lookup[k]].array() == 1 for k in cat])

    online_mask = on_pt_mask & online_mask

    for key  in plot_configs.keys():
        online_data = online_tree[key_lookup[key]].array()

        # print("key:\t", key)
        # if "vertex" in key:
            # print("Setting Values to 0:\nOnline:\t{}\nOffline:\t{}".format(sum(np.invert(on_nSV_mask)), sum(np.invert(off_nSV_mask))))
            # online_data[np.invert(on_nSV_mask)] *= 0.

        online_data = online_data[online_mask].flatten()

        print("Starting plotting")
        plot_histogram(online_data, key, process_name, cat_name)
