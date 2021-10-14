import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input file", type=str)
parser.add_argument("--labels", "-l", help="Input file with labels", type=str)
parser.add_argument("--name", "-n", help="Name of feature, e.g. pT", type=str)
parser.add_argument("--output", "-o", help="Output directory", type=str)
args = parser.parse_args()

def plot_histogram(online_data, key, name, category_name, plot_dir):
    fig, ax = plt.subplots(1, 1)
    fig.subplots_adjust(hspace=0)

    if len(online_data.shape) > 1:
        online_data = online_data.flatten()
    # hist_online, bin_edges = np.histogram( online_data, bins=20)
    binspace = np.linspace(-2., 2., 20)

    ax.hist( online_data, bins = binspace,  label = "Online $\mu=${0:1.2f} $\sigma$={1:1.2f}".format(np.mean(online_data), np.std(online_data)), color="red", alpha=0.5, density=True)
    ax.legend()
    ax.set_ylabel("N, normalized", fontsize=15)
    ax.set_title("{}\n{}".format(name, category_name), fontsize=15)
    ax.grid(which='both', axis='y',linestyle="dashed")

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    try:
        textstr = "min {0:1.2f}\nmax {1:1.2f}\nmean {2:1.2f}\nstd {3:1.2f}".format( np.min(online_data), np.max(online_data), np.mean(online_data), np.std(online_data))
    except ValueError as e:
        print(e)
        textstr = "Error"
    ax.text(0.8, 0.75, textstr, transform=ax.transAxes, fontsize=8,
                    verticalalignment='top', bbox=props)

    ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.tick_params(which='minor', length=4, color='black')

    fig.savefig( os.path.join(plot_dir, "{0}.png".format(name)))
    plt.close()

data = np.load(args.inp)
labels = np.load(args.labels)
print("Shape: {}".format(data.shape))

# os.makedirs( args.output, exist_ok=True)

# label_names = ['Jet_isB','Jet_isBB','Jet_isLeptonicB','Jet_isC','Jet_isUDS','Jet_isG']

# N_features = data.shape[1]


# for i, label_name in enumerate(label_names):
    # out_dir = os.path.join( args.output, label_name )
    # os.makedirs( out_dir, exist_ok=True)

    # print("Label: {}".format(label_name))
    # data_flavour = data[ np.where( labels[:,i] )[0], : ]

    # for idx in range(N_features):
        # # print("\tPlotting feature #{0:2d}".format(idx))
        # plot_histogram(data_flavour[:, idx], idx, "feature_{0:02d}_{1}".format(idx, label_name), label_name, out_dir)
