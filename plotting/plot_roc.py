import os
import uproot3
import matplotlib
import matplotlib.pyplot as plt
# import mplhep as hep
from matplotlib.ticker import AutoMinorLocator
matplotlib.use('Agg')

out_dir = "./offline_results/new_preprocessing_18/prediction/"

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

file_name = "ROCS_DeepCSV.root"
tree = uproot3.open(os.path.join(out_dir, file_name))

roc_0 = tree["roccurve_0"]
roc_1 = tree["roccurve_1"]

x_0 = roc_0.xvalues
y_0 = roc_0.yvalues

x_1 = roc_1.xvalues
y_1 = roc_1.yvalues

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.plot(x_1, y_1, label="b vs c", color="green")
ax.plot(x_0, y_0, label="b vs udsg", color="red")
ax.set_title("RocCurve DeepCSV", fontsize=24)
ax.set_xlabel("b-id. efficency")
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel("misid. prob.")
ax.set_yscale("log")
ax.set_xlim(0.4, 1.)
ax.set_ylim(9.*1e-4, 1.)
ax.grid(True, "both", linestyle="dashed")
ax.legend()
# hep.cms.label(
        # llabel="Private Work",
	# year=None,
	# lumi=None,
        # loc=0,
        # ax=ax,
        # )
fig.savefig(os.path.join(out_dir, "roc_curve.png"))
