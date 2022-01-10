import matplotlib.pyplot as plt
import uproot3 as u3
import tqdm
import os
import argparse
import numpy as np
import awkward as ak
from scripts.training_branches import key_lookup, DeepCSV_all_branches, new_ntuple_keys,file_comparison
from scripts.recalculate_flightDistance import recalculate_flightDistance
from plotting.plot_dataset_comparison import plot_configs
from functools import reduce
from matplotlib.ticker import AutoMinorLocator
from contextlib import ExitStack
import matplotlib
matplotlib.use('Agg')


key_pairs = {
        "npv":"DeepFlavourInput_nPVS",
        # "nCpfcand":"DeepFlavourInput_n_charged",
        # :"DeepFlavourInput_NFirst_charged",
        # :"DeepFlavourInput_NLast_charged",
        # :"DeepFlavourInput_multi_charged",
        # :"DeepFlavourInput_charged_Sip3dVal",
        # :"DeepFlavourInput_charged_Sip3dSig",
        # :"DeepFlavourInput_charged_quality",
        # :"DeepFlavourInput_charged_chi2",
        "Cpfcan_BtagPf_trackEtaRel":"DeepFlavourInput_charged_btagpf_trackEtaRel",
        "Cpfcan_BtagPf_trackPtRel":"DeepFlavourInput_charged_btagpf_trackPtRel",
        "Cpfcan_BtagPf_trackPPar":"DeepFlavourInput_charged_btagpf_trackPPar",
        "Cpfcan_BtagPf_trackDeltaR":"DeepFlavourInput_charged_btagpf_trackDeltaR",
        "Cpfcan_BtagPf_trackPParRatio":"DeepFlavourInput_charged_btagpf_trackPParRatio",
        "Cpfcan_BtagPf_trackSip2dVal":"DeepFlavourInput_charged_btagpf_trackSip2dVal",
        "Cpfcan_BtagPf_trackSip2dSig":"DeepFlavourInput_charged_btagpf_trackSip2dSig",
        "Cpfcan_BtagPf_trackSip3dVal":"DeepFlavourInput_charged_btagpf_trackSip3dVal",
        "Cpfcan_BtagPf_trackSip3dSig":"DeepFlavourInput_charged_btagpf_trackSip3dSig",
        "Cpfcan_BtagPf_trackJetDistVal":"DeepFlavourInput_charged_btagpf_trackJetDistVal",
        "Cpfcan_ptrel":"DeepFlavourInput_charged_ptrel",
        "Cpfcan_drminsv":"DeepFlavourInput_charged_drminsv",
        "Cpfcan_VTX_ass":"DeepFlavourInput_charged_VTX_ass",
        "Cpfcan_puppiw":"DeepFlavourInput_charged_puppiw",
        "nNpfcand":"DeepFlavourInput_n_neutral",
        # :"DeepFlavourInput_NFirst_neutral",
        # :"DeepFlavourInput_NLast_neutral",
        # :"DeepFlavourInput_multi_neutral",
        "Npfcan_drminsv":"DeepFlavourInput_neutral_drminsv",
        "Npfcan_HadFrac":"DeepFlavourInput_neutral_hadFrac",
        "Npfcan_ptrel":"DeepFlavourInput_neutral_ptrel",
        "Npfcan_deltaR":"DeepFlavourInput_neutral_deltaR",
        "Npfcan_isGamma":"DeepFlavourInput_neutral_isGamma",
        "Npfcan_puppiw":"DeepFlavourInput_neutral_puppiw",
        # "nsv":"DeepFlavourInput_n_sv",
        # :"DeepFlavourInput_NFirst_sv",
        # :"DeepFlavourInput_NLast_sv",
        # :"DeepFlavourInput_multi_sv",
        "sv_d3d": "DeepFlavourInput_sv_d3d",
        "sv_d3dsig": "DeepFlavourInput_sv_d3dsig",
        "sv_normchi2": "DeepFlavourInput_sv_normchi2",
        "sv_pt": "DeepFlavourInput_sv_pt",
        "sv_deltaR":"DeepFlavourInput_sv_deltaR",
        "sv_mass":"DeepFlavourInput_sv_mass",
        "sv_ntracks":"DeepFlavourInput_sv_ntracks",
        "sv_chi2":"DeepFlavourInput_sv_chi2",
        "sv_dxy":"DeepFlavourInput_sv_dxy",
        "sv_dxysig":"DeepFlavourInput_sv_dxysig",
        "sv_costhetasvpv":"DeepFlavourInput_sv_costhetasvpv",
        "sv_enratio":"DeepFlavourInput_sv_enratio"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files1", "-i1", help="Input 1 root-file, this should be mc", type=str)
    parser.add_argument("--file2", "-i2", help="Input 2 root-file, this should be data", type=str)
    parser.add_argument("--output", "-o", help="Output directory TAG. For example v02 to add a v02 at the end of the root-file", type=str, default="v00")
    parser.add_argument("--target", "-t", help="Target directory.", type=str, default="./dataset_comp")
    args = parser.parse_args()

    paths_mc = args.files1.split(",")
    path_data = args.file2
    output_tag = args.output

    with ExitStack() as file_stack_mc, u3.open(path_data) as file_data:

        files_mc = [file_stack_mc.enter_context( u3.open(fname)) for fname in paths_mc]

        trees_mc = [file_mc["ttree"] for file_mc in files_mc]
        tree_data = file_data["btagana/ttree"]

        masks_mc = [tree_mc["Jet_pt"].array() > 25. for tree_mc in trees_mc]
        mask_data = tree_data["Jet_pt"].array() > 25.

        keys_data = [k.decode("utf-8") for k in tree_data.keys()]

        for key_mc, key_data in key_pairs.items():
            print(f"Plotting {key_mc}")
            try:
                arrs_mc = [tree_mc[key_mc].array()[mask_mc] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]
            except ValueError as e:
                arrs_mc = [tree_mc[key_mc].array()[ak.any(mask_mc, axis=-1)] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]
            except IndexError as e:
                arrs_mc = [tree_mc[key_mc].array()[ak.any(mask_mc, axis=-1)] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]

            try:
                arr_data = tree_data[key_data].array()[mask_data]
            except ValueError as e:
                arr_data = tree_data[key_data].array()[ak.any(mask_data, axis=-1)]
            except IndexError as e:
                arr_data = tree_data[key_data].array()[ak.any(mask_data, axis=-1)]

            mc = ak.to_numpy( np.concatenate([ak.flatten(arr_mc, axis=-1) for arr_mc in arrs_mc]))
            data = ak.to_numpy( ak.flatten(arr_data, axis=-1))

            plot_histogram( mc, data, key_mc, "default", "all", args.target)

        for key in new_ntuple_keys:
            if key in keys_data:
                print(f"Plotting {key}")

                try:
                    arrs_mc = [tree_mc[key].array()[mask_mc] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]
                except ValueError as e:
                    arrs_mc = [tree_mc[key].array()[ak.any(mask_mc, axis=-1)] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]
                except IndexError as e:
                    arrs_mc = [tree_mc[key].array()[ak.any(mask_mc, axis=-1)] for tree_mc, mask_mc in zip(trees_mc, masks_mc)]

                try:
                    arr_data = tree_data[key].array()[mask_data]
                except ValueError as e:
                    arr_data = tree_data[key].array()[ak.any(mask_data, axis=-1)]
                except IndexError as e:
                    arr_data = tree_data[key].array()[ak.any(mask_data, axis=-1)]

                mc = ak.to_numpy( np.concatenate([ak.flatten(arr_mc, axis=-1) for arr_mc in arrs_mc]))
                data = ak.to_numpy( ak.flatten(arr_data, axis=-1))

                plot_histogram( mc, data, key, "data_MC_comparison", "all", args.target)

def compute_ratios(hist_online, hist_offline, bin_edges):
    r_a = hist_online / np.sum(hist_online)
    r_b = hist_offline / np.sum(hist_offline)
    ratios = r_a / (r_b + 1e-9)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_widths = np.diff(bin_centers)
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    return ratios, bin_centers


def plot_histogram(online_data, offline_data, key, name, category_name, plot_dir):
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0)

    hist_online, bin_edges = np.histogram( online_data, bins=plot_configs.get(key, {"bins": 15})["bins"])
    try:
        hist_offline, bin_edges = np.histogram( offline_data, bins=plot_configs.get(key, {"bins": 15})["bins"])
    except ValueError as e:
        print("Error in hist-computation!")
        print(e)
        raise NotI
    error_online = 1./np.sqrt(hist_online)
    error_offline = 1./np.sqrt(hist_offline)

    ratio_error = np.sqrt( (error_online* 1./(hist_offline) ) **2 + ( hist_online/(hist_offline **2)) **2 )

    ratios, bin_centers = compute_ratios(hist_online, hist_offline, bin_edges)

    ax[0].hist( online_data, bins = plot_configs.get(key, {"bins": bin_edges})["bins"],  label = "MC $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(online_data), np.std(online_data)), color="red", alpha=0.5, density=True)
    try:
        ax[0].hist( offline_data, bins = plot_configs.get(key, {"bins": bin_edges})["bins"], label = "Data $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(offline_data), np.std(offline_data)), color="blue", alpha=0.5, density=True)
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
        textstr = "MC:\nmin {0:1.2f}\nmax {1:1.2f}\nData:\nmin {2:1.2f}\nmax {3:1.2f}".format( np.min(online_data), np.max(online_data), np.min(offline_data), np.max(offline_data))
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
    main()
