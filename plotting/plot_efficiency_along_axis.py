import os
import uproot as ur
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import awkward as ak
from scipy.stats import binned_statistic
from sklearn.metrics import roc_curve, roc_auc_score
from scipy.interpolate import InterpolatedUnivariateSpline
from sklearn.metrics import accuracy_score
from pathlib import Path
import argparse

larger = 28 
large = 26
med = 20

_params = {
	"axes.titlesize": larger,
	"legend.fontsize": med,
	"figure.figsize": (16, 10),
	"axes.labelsize": larger,
	"xtick.labelsize": large,
	"ytick.labelsize": large,
	"figure.titlesize": large,
	"xtick.bottom": True,
	"xtick.direction": "in",
	"ytick.direction": "in",
	"xtick.major.size": 12,
	"ytick.major.size": 12,
	"xtick.minor.size": 8,
	"ytick.minor.size": 8,
	"ytick.left": True,
}
plt.rcParams.update(_params)

def spit_out_roc(disc,truth_array,selection_array):
    newx = np.logspace(-3.5, 0, 100)
    tprs = pd.DataFrame()
    truth = truth_array[selection_array]*1
    disc = disc[selection_array]
    tmp_fpr, tmp_tpr, _ = roc_curve(truth, disc)
    coords = pd.DataFrame()
    coords['fpr'] = tmp_fpr
    coords['tpr'] = tmp_tpr
    clean = coords.drop_duplicates(subset=['fpr'])
    spline = InterpolatedUnivariateSpline(clean.fpr, clean.tpr,k=1)
    tprs = spline(newx)
    return tprs, newx

N_BINS = 15

TIGHT = 0.01
MEDIUM = 0.001
LOSE = 0.0001

bins_pt = [25., 50., 80., 120., 200., 370., 500., 700., 1200., 1500.]
bins_eta = [-4., -2.5, -2., -1., -0.5, 0., 0.5, 1., 2., 2.5, 4]

bin_centers_pt = np.array( bins_pt[:-1] ) + np.diff(bins_pt)/2
bin_centers_eta = np.array( bins_eta[:-1] ) + np.diff(bins_eta)/2

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input directory", type=str)
parser.add_argument("--output", "-o", help="Output path", type=str)
args = parser.parse_args()

fname = args.inp
out_path = args.output

effs_pt_lose = []
effs_pt_medium = []
effs_pt_tight = []

effs_eta_lose = []
effs_eta_medium = []
effs_eta_tight = []

miss_pt_lose = []
miss_pt_medium = []
miss_pt_tight = []

n_events = []
n_events_eta = []


for root_file in Path(args.inp).rglob("pred_*.root"):
    print("Opening {}".format(root_file))
    with ur.open(root_file) as f:
        tree = f["tree"]
        pt = tree["Jet_pt_GeV"].array()
        eta = tree["Jet_eta_unscaled"].array()
        b_jets = tree["Jet_isB"].array() + tree["Jet_isBB"].array() + tree["Jet_isLeptB"].array()
        disc = tree["prob_isB"].array() + tree["prob_isBB"].array() + tree["prob_isLeptB"].array()
        summed_truth = tree["Jet_isB"].array() + tree["Jet_isBB"].array() + tree["Jet_isLeptB"].array() + tree["Jet_isC"].array() + tree["Jet_isUDS"].array() + tree["Jet_isG"].array()

        veto_c = (tree["Jet_isC"].array() != 1)
        veto_udsg = (tree["Jet_isUDS"].array() != 1)

        x_roc, y_roc = spit_out_roc(disc, b_jets, veto_udsg)
       
        tight_idx = np.where( y_roc > TIGHT )[0][0]
        medium_idx = np.where( y_roc > MEDIUM )[0][0]
        lose_idx = np.where( y_roc > LOSE )[0][0]

        tight_point = x_roc[tight_idx]
        medium_point = x_roc[medium_idx]
        lose_point = x_roc[lose_idx]

        bin_indices = np.digitize( ak.to_numpy(pt), bins_pt, right=True)

        bin_indices_eta = np.digitize( ak.to_numpy(eta), bins_eta, right=True )

        disc_bjets = disc[ np.where(b_jets) ]

        bin_indices = bin_indices[ np.where(b_jets) ]
        bin_indices_eta = bin_indices_eta[ np.where(b_jets) ]

        truth = np.ones( len(disc_bjets) )

        eff_tight = [accuracy_score(truth[bin_indices == idx], ak.to_numpy(disc_bjets[bin_indices == idx] > tight_point).astype(int)) for idx in range(len(bins_pt))]
        effs_pt_tight.append(eff_tight)

        eff_medium = [accuracy_score(truth[bin_indices == idx], ak.to_numpy(disc_bjets[bin_indices == idx] > medium_point).astype(int)) for idx in range(len(bins_pt))]
        effs_pt_medium.append(eff_medium)

        eff_lose = [accuracy_score(truth[bin_indices == idx], ak.to_numpy(disc_bjets[bin_indices == idx] > lose_point).astype(int)) for idx in range(len(bins_pt))]
        effs_pt_lose.append(eff_lose)
        n_events.append( [1 + len( np.where(bin_indices == idx)[0]) for idx in range( len(bins_pt) ) ])

        eff_tight = [accuracy_score(truth[bin_indices_eta == idx], ak.to_numpy(disc_bjets[bin_indices_eta == idx] > tight_point).astype(int)) for idx in range(len(bins_eta))]
        effs_eta_tight.append(eff_tight)

        eff_medium = [accuracy_score(truth[bin_indices_eta == idx], ak.to_numpy(disc_bjets[bin_indices_eta == idx] > medium_point).astype(int)) for idx in range(len(bins_eta))]
        effs_eta_medium.append(eff_medium)

        eff_lose = [accuracy_score(truth[bin_indices_eta == idx], ak.to_numpy(disc_bjets[bin_indices_eta == idx] > lose_point).astype(int)) for idx in range(len(bins_eta))]
        effs_eta_lose.append(eff_lose)

        n_events_eta.append( [1 + len( np.where(bin_indices_eta == idx)[0]) for idx in range( len(bins_eta) ) ])
    

print("Events per bin pt:")
print( np.sum(n_events, axis=0) )
print("Events per bin eta:")
print( np.sum(n_events_eta, axis=0) )

effs_pt_tight_total = np.average(effs_pt_tight, weights=n_events, axis=0)
effs_pt_medium_total = np.average(effs_pt_medium, weights=n_events, axis=0)
effs_pt_lose_total = np.average(effs_pt_lose, weights=n_events, axis=0)

effs_eta_tight_total = np.average(effs_eta_tight, weights=n_events_eta, axis=0)
effs_eta_medium_total = np.average(effs_eta_medium, weights=n_events_eta, axis=0)
effs_eta_lose_total = np.average(effs_eta_lose, weights=n_events_eta, axis=0)

n_events_total = np.sum(n_events, axis=0)
n_events_total_eta = np.sum(n_events_eta, axis=0)


err_eta_tight = 1./(n_events_total_eta**2)* np.sqrt( effs_eta_tight_total + effs_eta_tight_total**2 )
err_eta_medium = 1./(n_events_total_eta**2)* np.sqrt( effs_eta_medium_total + effs_eta_medium_total**2 )
err_eta_lose = 1./(n_events_total_eta**2)* np.sqrt( effs_eta_lose_total + effs_eta_lose_total**2 )

err_pt_tight = 1./(n_events_total**2)* np.sqrt( effs_pt_tight_total + effs_pt_tight_total**2 )
err_pt_medium = 1./(n_events_total**2)* np.sqrt( effs_pt_medium_total + effs_pt_medium_total**2 )
err_pt_lose = 1./(n_events_total**2)* np.sqrt( effs_pt_lose_total + effs_pt_lose_total**2 )



fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.errorbar( bin_centers_pt, effs_pt_lose_total[1:], yerr=err_pt_lose[1:], marker="*",fmt="",  linestyle="dashed", label="b-jet id. eff. lose")
ax.errorbar( bin_centers_pt, effs_pt_medium_total[1:], yerr=err_pt_medium[1:], marker="*",fmt="",  linestyle="dashed", label="b-jet id. eff. medium")
ax.errorbar( bin_centers_pt, effs_pt_tight_total[1:], yerr=err_pt_tight[1:], marker="*", fmt="", linestyle="dashed", label="b-jet id. eff. tight")
ax.legend(fontsize=25)
ax.set_xlabel("$p_T$[GeV]", fontsize=25)
ax.set_title("b-jet id. effic. per $p_T$", fontsize=25)
fig.savefig( os.path.join( out_path, "b_eff_pt.png") )

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.errorbar( bin_centers_eta, effs_eta_lose_total[1:], yerr=err_eta_lose[1:], marker="*",fmt="",  linestyle="dashed", label="b-jet id. eff. lose")
ax.errorbar( bin_centers_eta, effs_eta_medium_total[1:], yerr=err_eta_medium[1:], marker="*",fmt="",  linestyle="dashed", label="b-jet id. eff. medium")
ax.errorbar( bin_centers_eta, effs_eta_tight_total[1:], yerr=err_eta_tight[1:], marker="*",fmt="",  linestyle="dashed", label="b-jet id. eff. tight")
ax.legend(fontsize=25)
ax.set_xlabel("$\eta$", fontsize=25)
ax.set_title("b-jet id. effic. per $\eta$", fontsize=25)
fig.savefig( os.path.join( out_path, "b_eff_eta.png") )
