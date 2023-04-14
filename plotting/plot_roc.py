import os
import uproot3 as ur
import matplotlib
import matplotlib.pyplot as plt
import argparse
# import mplhep as hep
from matplotlib.ticker import AutoMinorLocator
matplotlib.use('Agg')

dir_base = os.path.join( os.getenv("TrainingOutput"), os.getenv("TrainingVersion")+"_pred")

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input dir", type=str, default=dir_base)
parser.add_argument("--output", "-o", help="Output directory for the plots", type=str, default=dir_base)
parser.add_argument("--deepCSV", "-d", help="Is deepCSV", default=False, action="store_true")
parser.add_argument("--tag", "-t", help="Tag", default="all")
args = parser.parse_args()

tag = args.tag

out_dir = os.path.join( args.output, "plots" )
os.makedirs( out_dir, exist_ok = True)

if not(args.deepCSV) is True:
    label = "DeepJet"
else:
    label = "DeepCSV"


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
tree = ur.open( file_name)

roc_0 = tree["roccurve_0"]
roc_1 = tree["roccurve_1"]
# roc_2 = tree["roccurve_2"]
# roc_3 = tree["roccurve_3"]

# roc_old = ur.open( "/nfs/dust/cms/user/neich/BTV/Trainings/DeepJet_prod_05_pred/ROCS_DeepCSV.root")["roccurve_0"]

# if not(args.deepCSV):
#     roc_4 = tree["roccurve_4"]
#     roc_5 = tree["roccurve_5"]

x_0 = roc_0.xvalues
y_0 = roc_0.yvalues

x_1 = roc_1.xvalues
y_1 = roc_1.yvalues

# x_0_DeepCSV = roc_2.xvalues
# y_0_DeepCSV = roc_2.yvalues
# from IPython import embed;embed()

# x_1_DeepCSV = roc_3.xvalues
# y_1_DeepCSV = roc_3.yvalues

# if not(args.deepCSV):
#     x_0_DeepJet = roc_4.xvalues
#     y_0_DeepJet = roc_4.yvalues

#     x_1_DeepJet = roc_5.xvalues
#     y_1_DeepJet = roc_5.yvalues

# x_broken = roc_old.xvalues
# y_broken = roc_old.yvalues

"""
offline evaluated models
"""
# with ur.open("/nfs/dust/cms/user/neich/BTV/DeepJet_ttBarHad_30pt.root") as f:
#     x_offline_DeepJet_light, y_offline_DeepJet_light = f["roccurve_0"].xvalues, f["roccurve_0"].yvalues
#     x_offline_DeepJet_charm, y_offline_DeepJet_charm= f["roccurve_1"].xvalues, f["roccurve_1"].yvalues

# with ur.open("/nfs/dust/cms/user/neich/BTV/DeepCSV_ttBarHad_30pt.root") as f:
#     x_offline_DeepCSV_light, y_offline_DeepCSV_light = f["roccurve_0"].xvalues, f["roccurve_0"].yvalues
#     x_offline_DeepCSV_charm, y_offline_DeepCSV_charm= f["roccurve_1"].xvalues, f["roccurve_1"].yvalues

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_0, y_0, label="b vs udsg Retraining", color="red")
ax.set_title("RocCurve {}".format(label), fontsize=24)
ax.set_xlabel("b-id. efficiency")

ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())

ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.01, 1.)
ax.set_ylim(9.*1e-5, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_light_deepJet.png"))
print("Saving light deepJet")


fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_1, y_1, label="b vs c Retraining", color="red", linestyle="dashed")
ax.set_title("RocCurve {}".format(label), fontsize=24)
ax.set_xlabel("b-id. efficiency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.01, 1.)
ax.set_ylim(9.*1e-5, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
fig.savefig(os.path.join(out_dir, f"{tag}roc_curve_charm.png"))
print("Saving charm")