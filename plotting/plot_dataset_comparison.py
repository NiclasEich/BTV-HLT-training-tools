import numpy as np
import matplotlib.pyplot as plt
import uproot3 as u3
import awkward
import os
import argparse
from scripts.training_branches import key_lookup, DeepCSV_all_branches, new_ntuple_keys
from scripts.training_branches import file_comparison
from scripts.recalculate_flightDistance import recalculate_flightDistance
from functools import reduce
from matplotlib.ticker import AutoMinorLocator

def track_var_to_flat(arr, idx_low, idx_high):
    arr = awkward.to_awkward0(awkward.Array( [[[a for a in ev[ka : kb + 1] ] for ka, kb in zip(kidx_a, kidx_b) ] for ev, kidx_a, kidx_b in zip(arr, idx_low, idx_high)])).flatten(axis=0)
    return arr

plot_configs = {'Jet_pt':{"bins": np.arange(0, 1000, 25) , "log": True},
                'Jet_eta':{"bins": np.linspace(-4.2, 4.2, 20) , "log": False},
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

branches_with_idx = ["TagVarCSV_trackJetDistVal",
                     "TagVarCSV_trackDeltaR",
                     "TagVarCSV_trackPtRatio",
                     "TagVarCSV_trackSip3dSig",
                     "TagVarCSV_trackSip2dSig",
                     "TagVarCSV_trackSip3dVal",
                     "TagVarCSV_trackSip2dVal",
                     "TagVarCSV_trackPtRel",
                     "TagVarCSV_trackDecayLenVal"]

def compute_ratios(hist_online, hist_offline, bin_edges):
    r_a = hist_online / np.sum(hist_online)
    r_b = hist_offline / np.sum(hist_offline)
    ratios = r_a / (r_b + 1e-9)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_widths = np.diff(bin_centers)
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    return ratios, bin_centers


def plot_histogram(online_data, offline_data, key, name, category_name):
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0)

    hist_online, bin_edges = np.histogram( online_data, bins=plot_configs.get(key, {"bins": 15})["bins"])
    try:
        hist_offline, bin_edges = np.histogram( offline_data, bins=plot_configs.get(key, {"bins": 15})["bins"])
    except ValueError as e:
        print("Error in hist-computation!")
        print(e)
        return

    error_online = 1./np.sqrt(hist_online)
    error_offline = 1./np.sqrt(hist_offline)

    ratio_error = np.sqrt( (error_online* 1./(hist_offline) ) **2 + ( hist_online/(hist_offline **2)) **2 )

    ratios, bin_centers = compute_ratios(hist_online, hist_offline, bin_edges)

    ax[0].hist( online_data, bins = plot_configs.get(key, {"bins": "auto"})["bins"],  label = "Online $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(online_data), np.std(online_data)), color="red", alpha=0.5, density=True)
    try:
        ax[0].hist( offline_data, bins = plot_configs.get(key, {"bins": "auto"})["bins"], label = "Offline $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(offline_data), np.std(offline_data)), color="blue", alpha=0.5, density=True)
    except ValueError as e:
        print(e)
    ax[0].legend()
    if plot_configs.get(key, {"log": True})["log"] is True:
        ax[0].set_yscale('log')
    ax[0].set_ylabel("N, normalized", fontsize=15)
    ax[0].set_title("{}\n{}".format(name, category_name), fontsize=15)
    ax[0].grid(which='both', axis='y',linestyle="dashed")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    try:
        textstr = "Online:\nmin {0:1.2f}\nmax {1:1.2f}\nOffline:\nmin {2:1.2f}\nmax {3:1.2f}".format( np.min(online_data), np.max(online_data), np.min(offline_data), np.max(offline_data))
        if tot_underflows != None:
            textstr += "\nUnderflows: {}".format(tot_underflows)
    except ValueError as e:
        print(e)
        textstr = "Error"
    ax[0].text(0.8, 0.75, textstr, transform=ax[0].transAxes, fontsize=8,
                    verticalalignment='top', bbox=props)

    bin_widths = np.diff(bin_centers) 
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    ax[1].errorbar(
        bin_centers,
        ratios,
        xerr=bin_widths,
        yerr=ratio_error,
        color="black",
        linestyle="None",
        marker=None,
    )
    ax[1].axhline(y=1.0, linestyle="dashed", color="grey", alpha=0.5)
    ax[1].xaxis.set_minor_locator(AutoMinorLocator()) 
    ax[1].tick_params(which='minor', length=4, color='black')
    ax[1].set_ylabel(
        "$\\frac{{{0}}}{{{1}}}$".format("online", "offline")
    )
    ax[1].set_xlabel(key, fontsize=15)
    ax[1].set_ylim(
        0.5, 1.5)

    fig.savefig( os.path.join(plot_dir, "{}_{}.png".format(name, key)))
    fig.savefig( os.path.join(plot_dir, "{}_{}.pdf".format(name, key)))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", "-i", help="Input root-file", type=str)
    parser.add_argument("--offline", "-j", help="Input root-file for offline", type=str, default="/afs/cern.ch/work/n/neich/public/new_offline_files/TT_TuneCP5_14TeV-powheg-pythia8_PU200_new.root")
    parser.add_argument("--output", "-o", help="Output directory TAG. For example v02 to add a v02 at the end of the root-file", type=str, default="v00")
    parser.add_argument("--target", "-t", help="Target directory.", type=str, default="./dataset_comp")
    args = parser.parse_args()

    online_file = args.online
    offline_file = args.offline
    output_tag = args.output
    target_dir = args.target
    process_name = online_file.split("/")[-1].split(".")[0]


    base_dir = os.path.join(target_dir, "{}_{}".format(process_name, output_tag))
    os.makedirs(base_dir, exist_ok=True)

    offline_tree = u3.open(offline_file)["btagana"]["ttree"]
    online_tree =  u3.open(online_file)["ttree"]

    plot_keys = key_lookup.keys()

    online_jet_pt = online_tree[key_lookup["Jet_pt"]].array()
    offline_jet_pt = offline_tree["Jet_pt"].array()

    off_pt_mask = (offline_jet_pt > 25.) & (offline_jet_pt < 10000.)
    on_pt_mask = (online_jet_pt > 25.) & (online_jet_pt < 10000.)

    online_nSV = online_tree[key_lookup["TagVarCSV_jetNSecondaryVertices"]].array()
    offline_nSV = offline_tree["TagVarCSV_jetNSecondaryVertices"].array()

    on_nSV_mask = online_nSV > 0
    off_nSV_mask = offline_nSV > 0 

    offline_cleaning_keys = ["TagVarCSV_flightDistance2dVal", "TagVarCSV_flightDistance2dSig", "TagVarCSV_flightDistance3dVal", "TagVarCSV_flightDistance3dSig"]

    category_names = ["b_jets", "bb+gbb_jets", "lepb_jets", "c+cc+gcc_jets", "uds_jets", "g_jes", "all_jets"]
    categories = [ ['Jet_isB'], ['Jet_isBB', 'Jet_isGBB'], ['Jet_isLeptonicB', 'Jet_isLeptonicB_C'], ['Jet_isC', 'Jet_isCC', 'Jet_isGCC'], ['Jet_isUD', 'Jet_isS'], ['Jet_isG'], ['Jet_isB','Jet_isBB', 'Jet_isGBB', 'Jet_isLeptonicB', 'Jet_isLeptonicB_C', 'Jet_isC', 'Jet_isCC', 'Jet_isGCC','Jet_isUD', 'Jet_isS', 'Jet_isG']]

    for cat, cat_name in zip(categories, category_names):
        plot_dir = os.path.join( base_dir, cat_name )
        print("Creating plot-dir {}".format(plot_dir))
        os.makedirs(plot_dir, exist_ok=True)

        offline_mask = reduce(np.logical_or , [ offline_tree[k].array() == 1 for k in cat])
        online_mask = reduce(np.logical_or , [ online_tree[key_lookup[k]].array() == 1 for k in cat])

        online_mask = on_pt_mask & online_mask
        offline_mask = off_pt_mask & offline_mask

        tracking_index_low = offline_tree['Jet_nFirstTrkTagVarCSV'].array()
        tracking_index_high = offline_tree['Jet_nLastTrkTagVarCSV'].array()
        # dtype = np.dtype("f4")
        track_eta_index_low = offline_tree['Jet_nFirstTrkEtaRelTagVarCSV'].array()
        track_eta_index_high = offline_tree['Jet_nLastTrkEtaRelTagVarCSV'].array()

        for key in key_lookup.keys():
            online_data = online_tree[key_lookup[key]].array()
            offline_data = offline_tree[key].array()

            if key in offline_cleaning_keys:
                offline_data = recalculate_flightDistance(offline_tree, key)

            print("key:\t", key)

            online_data = online_data[online_mask].flatten()

            if 'TagVarCSV_trackEtaRel' in key:
                offline_data = track_var_to_flat( offline_tree[key].array(), track_eta_index_low, track_eta_index_high)[offline_mask.flatten()]
            elif any([k == key for k in branches_with_idx ]):
                offline_data = track_var_to_flat( offline_tree[key].array(), tracking_index_low, tracking_index_high)[offline_mask.flatten()]
            else:
                offline_data = offline_data[offline_mask].flatten()

            if plot_configs.get(key, {}).get("underflow", False) is not False:
                mask = offline_data != plot_configs.get(key, {"underflow": -999999.}).get("underflow", -99999.)
                tot_underflows = sum(np.invert(mask))
                offline_data = offline_data[mask]
            else:
                tot_underflows = None

            print("Starting plotting")
            plot_histogram(online_data, offline_data, key, process_name, cat_name)
