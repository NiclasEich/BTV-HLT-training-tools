import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
import uproot3 as ur
import mplhep as hep
import numpy as np
# import mplhep as hep
from matplotlib.ticker import AutoMinorLocator
matplotlib.use('Agg')
plt.style.use(hep.style.ROOT)

dir_base = os.path.join( os.getenv("TrainingOutput"), os.getenv("TrainingVersion")+"_pred")

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input dir", type=str, default=dir_base)
parser.add_argument("--inp2", "-j", help="Input dir 2", type=str, default=dir_base)
parser.add_argument("--output", "-o", help="Output directory for the plots", type=str, default=dir_base)
parser.add_argument("--tag", "-t", help="Tag", default="all")
args = parser.parse_args()

tag = args.tag

out_dir = os.path.join( args.output, "plots" )
os.makedirs( out_dir, exist_ok = True)


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

file_name = os.path.join(args.inp, "ROCS_DeepCSV.root")
with ur.open(file_name) as tree:

    roc_0 = tree["roccurve_0"]
    roc_1 = tree["roccurve_1"]
    roc_2 = tree["roccurve_2"]
    roc_3 = tree["roccurve_3"]
    roc_4 = tree["roccurve_4"]
    roc_5 = tree["roccurve_5"]

    # roc_charm_light = tree["roccurve_charm_light"]
    # roc_charm_b = tree["roccurve_charm_b"]
    # roc_charm_light_no_retraining = tree["roccurve_charm_light_no_retraining"]
    # roc_charm_b_no_retraining = tree["roccurve_charm_b_no_retraining"]

    # roc_charm_light_run2 = tree["roccurve_charm_light_run2"]
    # roc_charm_b_run2 = tree["roccurve_charm_b_run2"]

# roc_old = ur.open( "/nfs/dust/cms/user/neich/BTV/Trainings/DeepJet_prod_05_pred/ROCS_DeepCSV.root")["roccurve_0"]






x_0 = roc_0.xvalues
y_0 = roc_0.yvalues

x_1 = roc_1.xvalues
y_1 = roc_1.yvalues

x_0_DeepCSV = roc_2.xvalues
y_0_DeepCSV = roc_2.yvalues
# from IPython import embed;embed()

x_1_DeepCSV = roc_3.xvalues
y_1_DeepCSV = roc_3.yvalues

# x_charm_vs_light = roc_charm_light.xvalues
# y_charm_vs_light = roc_charm_light.yvalues

# x_charm_vs_b = roc_charm_b.xvalues
# y_charm_vs_b = roc_charm_b.yvalues


file_name = os.path.join(args.inp2, "ROCS_DeepCSV.root")
with  ur.open( file_name) as tree:
    roc_CSV = tree["roccurve_0"]
    roc_CSV_charm = tree["roccurve_1"]
    
    # roc_CSV_charm_vs_l = tree["roccurve_charm_light"]
    # roc_CSV_charm_vs_b = tree["roccurve_charm_b"]

    # x_csv_charm_vs_l = roc_CSV_charm_vs_l.xvalues
    # y_csv_charm_vs_l = roc_CSV_charm_vs_l.yvalues

    # x_csv_charm_vs_b = roc_CSV_charm_vs_b.xvalues
    # y_csv_charm_vs_b = roc_CSV_charm_vs_b.yvalues


x_CSV = roc_CSV.xvalues
y_CSV = roc_CSV.yvalues

x_CSV_charm = roc_CSV_charm.xvalues
y_CSV_charm = roc_CSV_charm.yvalues

x_0_DeepJet = roc_4.xvalues
y_0_DeepJet = roc_4.yvalues

x_1_DeepJet = roc_5.xvalues
y_1_DeepJet = roc_5.yvalues

# x_broken = roc_old.xvalues
label = ""
# y_broken = roc_old.yvalues

"""
offline evaluated models
"""
with ur.open("/nfs/dust/cms/user/neich/BTV/DeepJet_ttBarHad_30pt.root") as f:
    x_offline_DeepJet_light, y_offline_DeepJet_light = f["roccurve_0"].xvalues, f["roccurve_0"].yvalues
    x_offline_DeepJet_charm, y_offline_DeepJet_charm= f["roccurve_1"].xvalues, f["roccurve_1"].yvalues

with ur.open("/nfs/dust/cms/user/neich/BTV/DeepCSV_ttBarHad_30pt.root") as f:
    x_offline_DeepCSV_light, y_offline_DeepCSV_light = f["roccurve_0"].xvalues, f["roccurve_0"].yvalues
    x_offline_DeepCSV_charm, y_offline_DeepCSV_charm= f["roccurve_1"].xvalues, f["roccurve_1"].yvalues

# fig, ax = plt.subplots(1, 1, figsize=(15, 10))
# ax.plot(x_offline_DeepCSV_light, y_offline_DeepCSV_light, label="b vs udsg DeepCSV Off-Off", color="green")
# ax.plot(x_offline_DeepCSV_charm, y_offline_DeepCSV_charm, color="green", linestyle="dashed")
# ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="b vs udsg DeepJet Offline", color="black")
# ax.plot(x_offline_DeepJet_charm, y_offline_DeepJet_charm, color="blue", linestyle="dashed")
# ax.plot(x_0, y_0, label="b vs udsg Retraining DeepJet", color="red")
# ax.plot(x_CSV, y_CSV, label="b vs udsg Retraining DeepCSV", color="red", linestyle="dashed")
# # ax.plot(x_broken, y_broken, label="b vs udsg broken matrix", color="orange")
# ax.plot(x_0_DeepCSV, y_0_DeepCSV, label="b vs udsg DeepCSV Off-On", color="purple")
# ax.plot(x_1, y_1, label="b vs c", color="red", linestyle="dashed")
# ax.plot(x_1_DeepCSV, y_1_DeepCSV, color="purple", linestyle="dashed")
# ax.set_title("RocCurve Tagger Run 3".format(label), fontsize=24)
# ax.set_xlabel("b-jet identification efficiency")
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.set_ylabel("light flavour misidentification rate")
# ax.set_yscale("log")
# ax.set_xlim(0.01, 1.)
# ax.set_ylim(9.*1e-4, 1.)
# ax.grid(True, "both", linestyle="dashed")
# ax.legend()
# fig.savefig(os.path.join(out_dir, f"{tag}_roc_curve_all.png"))
# print("Saving all")

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="offline DeepJet", color="black")
ax.plot(x_0, y_0, label="online DeepJet".format(label), color="red")
ax.plot(x_0_DeepJet, y_0_DeepJet, label="online DeepJet no retraining", color="orange")
ax.plot(x_offline_DeepCSV_light, y_offline_DeepCSV_light, label="offline DeepCSV", color="black", linestyle="dashed")
ax.plot(x_CSV, y_CSV, label="online DeepCSV", color="red", linestyle="dashed")
# ax.plot(x_broken, y_broken, label="b vs udsg broken matrix", color="orange")
ax.plot(x_0_DeepCSV, y_0_DeepCSV, label="online DeepCSV Run 2", color="blue", linestyle="dashed")

# ax.set_title("Expected b-Tagging Performance Run 3".format(label), fontsize=24)
ax.set_xlabel("b jet identification efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("light-flavour jet misidentification rate")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(4.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed", alpha=0.5)
ax.legend(loc="best", bbox_to_anchor=(0.77, 0.7), ncol=2)
hep.cms.label( loc=1, lumi=None, year=None, rlabel="13 TeV, 14 TeV")
fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_light.png"))
print("Saving light")


# fig, ax = plt.subplots(1, 1, figsize=(15, 10))
# ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="b vs udsg DeepJet Off-Off", color="blue")
# ax.plot(x_0, y_0, label="b vs udsg Retraining DeepJet", color="red")
# ax.plot(x_CSV, y_CSV, label="b vs udsg Retraining DeepCSV", color="red", linestyle="dashed")

# ax.set_title("RocCurve Tagger Run 3".format(label), fontsize=24)
# ax.set_xlabel("b-jet identification efficiency")
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.set_ylabel("light flavour misidentification rate")
# ax.set_yscale("log")
# ax.set_xlim(0.01, 1.)
# ax.set_ylim(9.*1e-4, 1.)
# ax.grid(True, "both", linestyle="dashed")
# ax.legend()
# fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_light_deepJet.png"))
# print("Saving light deepJet")

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepJet_charm, y_offline_DeepJet_charm, label="offline DeepJet", color="black")
ax.plot(x_1, y_1, label="online DeepJet", color="red")
ax.plot(x_1_DeepJet, y_1_DeepJet, label="online DeepJet no retraining", color="orange")
ax.plot(x_offline_DeepCSV_charm, y_offline_DeepCSV_charm, label="offline DeepCSV",color="black", linestyle="dashed")
ax.plot(x_CSV_charm, y_CSV_charm, label="online DeepCSV", color="red", linestyle="dashed")
ax.plot(x_1_DeepCSV, y_1_DeepCSV, label="online DeepCSV Run 2", color="blue", linestyle="dashed")

# ax.set_title("RocCurve Tagger Run 3".format(label), fontsize=24)
ax.set_xlabel("b jet identification efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("c jet misidentification rate")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(4.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed", alpha=0.5)
ax.legend(loc=4, ncol=2)
hep.cms.text(text="Work in Progress", loc=1)
# hep.cms.label(text="Work in Progress", loc=1, lumi=None, year=None, rlabel="13 TeV, 14 TeV")
fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_charm.png"))
fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_charm.pdf"))
print("Saving charm")

print("Load C-tagging arrays")

base = "/nfs/dust/cms/user/neich/BTV/ROCs/UL2017/"
deepJet_c_vs_l = np.load(base + "CvL_DeepJet.npy") 
deepJet_c_vs_b = np.load(base + "CvB_DeepJet.npy") 
deepCSV_c_vs_l = np.load(base + "CvL_DeepCSV.npy") 
deepCSV_c_vs_b = np.load(base + "CvB_DeepCSV.npy") 


# fig, ax = plt.subplots(1, 1, figsize=(15, 10))
# ax.plot(deepJet_c_vs_l[0], deepJet_c_vs_l[1], label="offline DeepJet", color="black")
# ax.plot(x_charm_vs_light, y_charm_vs_light, label="online DeepJet", color="red")
# ax.plot(roc_charm_light_no_retraining.xvalues,roc_charm_light_no_retraining.yvalues,  label="online DeepJet no retraining", color="orange")
# ax.plot(deepCSV_c_vs_l[0], deepCSV_c_vs_l[1], label="offline DeepCSV", color="black", linestyle="dashed")
# ax.plot(x_csv_charm_vs_l, y_csv_charm_vs_l, label="online DeepCSV", color="red", linestyle="dashed")
# ax.plot(roc_charm_light_run2.xvalues,roc_charm_light_run2.yvalues, label="online DeepCSV Run 2", linestyle="dashed", color="blue")
# ax.set_xlabel("c jet identification efficiency")
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.set_ylabel("light jet misidentification rate")
# ax.set_yscale("log")
# ax.set_xlim(0.0, 1.)
# ax.set_ylim(4.*1e-4, 1.)
# ax.grid(True, "both", linestyle="dashed", alpha=0.5)
# ax.legend(loc=4, ncol=2)
# hep.cms.label(loc=1, lumi=None, year=None, rlabel="13 TeV, 14 TeV")
# fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_charm_vs_light.png"))
# print("Saving charm vs light")

# fig, ax = plt.subplots(1, 1, figsize=(15, 10))
# ax.plot(deepJet_c_vs_b[0], deepJet_c_vs_b[1], label="offline DeepJet", color="black")
# ax.plot(x_charm_vs_b, y_charm_vs_b, label="online DeepJet", color="red")
# ax.plot(roc_charm_b_no_retraining.xvalues,roc_charm_b_no_retraining.yvalues,  label="online DeepJet no retraining", color="orange")
# ax.plot(deepCSV_c_vs_b[0], deepCSV_c_vs_b[1], label="offline DeepCSV", color="black", linestyle="dashed")
# ax.plot(x_csv_charm_vs_b, y_csv_charm_vs_b, label="online DeepCSV", color="red", linestyle="dashed")
# ax.plot(roc_charm_b_run2.xvalues,roc_charm_b_run2.yvalues, label="online DeepCSV Run 2", linestyle="dashed", color="blue")
# ax.set_xlabel("c jet identification efficiency")
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_ticks_position('both')
# ax.xaxis.set_minor_locator(AutoMinorLocator())
# ax.set_ylabel("b jet misidentification rate")
# ax.set_yscale("log")
# ax.set_xlim(0.0, 1.)
# ax.set_ylim(4.*1e-4, 1.)
# ax.grid(True, "both", linestyle="dashed", alpha=0.5)
# ax.legend(loc=4, ncol=2)
# hep.cms.label(loc=1, lumi=None, year=None, rlabel="13 TeV, 14 TeV")
# fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_charm_vs_b.png"))
# print("Saving charm vs b")
