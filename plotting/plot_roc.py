import os
import uproot3
import uproot as ur
import matplotlib
import matplotlib.pyplot as plt
import argparse
# import mplhep as hep
from matplotlib.ticker import AutoMinorLocator
matplotlib.use('Agg')

dir_base = os.path.join( os.getenv("TrainingOutput"), os.getenv("TrainingVersion")+"_pred")

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input dir", type=str, default=dir_base)
args = parser.parse_args()

out_dir = os.path.join( args.inp, "plots" )
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
tree = uproot3.open(os.path.join(args.inp, file_name))

roc_0 = tree["roccurve_0"]
roc_1 = tree["roccurve_1"]
roc_2 = tree["roccurve_2"]
roc_3 = tree["roccurve_3"]
roc_4 = tree["roccurve_4"]
roc_5 = tree["roccurve_5"]

x_0 = roc_0.xvalues
y_0 = roc_0.yvalues

x_1 = roc_1.xvalues
y_1 = roc_1.yvalues

x_0_DeepCSV = roc_2.xvalues
y_0_DeepCSV = roc_2.yvalues
# from IPython import embed;embed()

x_1_DeepCSV = roc_3.xvalues
y_1_DeepCSV = roc_3.yvalues

x_0_DeepJet = roc_4.xvalues
y_0_DeepJet = roc_4.yvalues

x_1_DeepJet = roc_5.xvalues
y_1_DeepJet = roc_5.yvalues


"""
offline evaluated models
"""
with ur.open("/nfs/dust/cms/user/neich/BTV/DeepJet_ttBarHad_30pt.root") as f:
    x_offline_DeepJet_light, y_offline_DeepJet_light = f["roccurve_0"].values()
    x_offline_DeepJet_charm, y_offline_DeepJet_charm= f["roccurve_1"].values()

with ur.open("/nfs/dust/cms/user/neich/BTV/DeepCSV_ttBarHad_30pt.root") as f:
    x_offline_DeepCSV_light, y_offline_DeepCSV_light = f["roccurve_0"].values()
    x_offline_DeepCSV_charm, y_offline_DeepCSV_charm= f["roccurve_1"].values()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepCSV_light, y_offline_DeepCSV_light, label="b vs udsg DeepCSV Off-Off", color="black")
ax.plot(x_offline_DeepCSV_charm, y_offline_DeepCSV_charm, color="black", linestyle="dashed")
ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="b vs udsg DeepJet Off-Off", color="black")
ax.plot(x_offline_DeepJet_charm, y_offline_DeepJet_charm, color="black", linestyle="dashed")
ax.plot(x_0, y_0, label="b vs udsg Retraining", color="red")
ax.plot(x_0_DeepCSV, y_0_DeepCSV, label="b vs udsg DeepCSV Off-On", color="purple")
ax.plot(x_0_DeepJet, y_0_DeepJet, label="b vs udsg DeepJet Off-On", color="orange")
ax.plot(x_1, y_1, label="b vs c", color="red", linestyle="dashed")
ax.plot(x_1_DeepCSV, y_1_DeepCSV, color="purple", linestyle="dashed")
ax.plot(x_1_DeepJet, y_1_DeepJet, color="orange", linestyle="dashed")
ax.set_title("RocCurve DeepJet", fontsize=24)
ax.set_xlabel("b-id. efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(9.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, "roc_curve_all.png"))
print("Saving all")

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepCSV_light, y_offline_DeepCSV_light, label="b vs udsg DeepCSV Off-Off", color="black")
ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="b vs udsg DeepJet Off-Off", color="black")
ax.plot(x_0, y_0, label="b vs udsg Retrained", color="red")
ax.plot(x_0_DeepCSV, y_0_DeepCSV, label="b vs udsg DeepCSV Off-On", color="purple")
ax.plot(x_0_DeepJet, y_0_DeepJet, label="b vs udsg DeepJet Off-On", color="orange")

ax.set_title("RocCurve DeepJet", fontsize=24)
ax.set_xlabel("b-id. efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(9.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, "roc_curve_light.png"))
print("Saving light")


fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepJet_light, y_offline_DeepJet_light, label="b vs udsg DeepJet Off-Off", color="black")
ax.plot(x_0, y_0, label="b vs udsg Retraining", color="red")
ax.plot(x_0_DeepJet, y_0_DeepJet, label="b vs udsg DeepJet Off-On", color="orange")

ax.set_title("RocCurve DeepJet", fontsize=24)
ax.set_xlabel("b-id. efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(9.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, "roc_curve_light_deepJet.png"))
print("Saving light deepJet")

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_offline_DeepCSV_charm, y_offline_DeepCSV_charm, label="b vs c DeepCSV Off-Off",color="black", linestyle="dashed")
ax.plot(x_offline_DeepJet_charm, y_offline_DeepJet_charm, label="b vs c DeepJet Off-Off", color="black", linestyle="dashed")
ax.plot(x_1, y_1, label="b vs c Retraining", color="red", linestyle="dashed")
ax.plot(x_1_DeepCSV, y_1_DeepCSV, label="b vs c DeepCSV Off-On", color="purple", linestyle="dashed")
ax.plot(x_1_DeepJet, y_1_DeepJet, label="b vs c DeepJet Off-On", color="orange", linestyle="dashed")
ax.set_title("RocCurve DeepJet", fontsize=24)
ax.set_xlabel("b-id. efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(9.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, "roc_curve_charm.png"))
print("Saving charm")
