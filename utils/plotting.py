import matplotlib.pyplot as plt
import numpy as np
from matplotlib import use as MPLuse
from matplotlib.ticker import AutoMinorLocator

MPLuse("agg")

def compute_ratios(hist_a, hist_b, bin_edges):
    r_a = hist_a / np.sum(hist_b)
    r_b = hist_b / np.sum(hist_b)
    ratios = r_a / (r_b + 1e-9)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_widths = np.diff(bin_centers)
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0

    return ratios, bin_centers

def create_histogram_figure(arrays, names, xlabel=None, bins=None, title=None, log=True):
    """Function that creates a matplotlib figure of N-arrays


    Args:
        arrays ([single numpy array or list of arrays]): [description]
        names ([type]): [description]
        var_name ([type]): [description]
        bins ([type], optional): [description]. Defaults to None.
        title (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [returns figure and axis object]
    """

    fig, ax = plt.subplots(1, 1)

    # conver
    if not isinstance(arrays, list):
        arrays = [arrays]
        names = [names]

    # histogram the data
    hists = []

    for arr in arrays:
        if bins is None:
            hist, bin_edges= np.histogram(arr, bins=20)
            bins = bin_edges
        else:
            hist, bin_edges = np.histogram(arr, bins=bins)
        hists.append(hist)
    
    for array, hist, name in zip(arrays, hists, names):
        arr_mean, arr_sigma, arr_max, arr_min = np.mean(array), np.std(array), np.max(array), np.min(array)
        label = "{0} $\mu=${1:1.2f} $\sigma$={2:1.2f} max={3:1.2f} min={4:1.2f}".format(name, arr_mean, arr_sigma, arr_max, arr_min)
        ax.hist( hist, bins=bin_edges, label=name)

    ax.set_ylabel("Entries (normalized)")
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=15)
    if title is not None:
        ax.set_title(title, fontsize=20)
    if log is True:
        ax.set_yscale('log')

    ax.grid(which='both', axis='y',linestyle="dashed")
    ax.xaxis.set_minor_locator(AutoMinorLocator()) 
    ax.tick_params(which='minor', length=4, color='black')

    return fig, ax


def create_histogram_ratio_figure(arrays, names, xlabel=None, bins=None, title=None, log=True, debug=False):
    """

    Args:
        arrays ([type]): [description]
        names ([type]): [description]
        xlabel ([type], optional): [description]. Defaults to None.
        bins ([type], optional): [description]. Defaults to None.
        title ([type], optional): [description]. Defaults to None.
        log (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """

    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0)

    # conver
    if not isinstance(arrays, list):
        arrays = [arrays]
        names = [names]

    # histogram the data
    hists = []
    for arr in arrays:
        if bins is None:
            hist, bin_edges= np.histogram(arr, bins=20)
            bins = bin_edges
        else:
            hist, bin_edges = np.histogram(arr, bins=bins)
            bins = bin_edges
        hists.append(hist)

    def comp_err(a, b):
        return np.sqrt((a* 1./(b) ) **2 + ( a/(b **2)) **2)

    # cmoputer ratios
    errors = [1./np.sqrt(hist) for hist in hists]
    # ratio_errors [ np.sqrt((errors[0]* 1./(error) ) **2 + ( errors[0]/(error **2)) **2) for error in errors[1:]]
    ratio_errors = [ comp_err(errors[0], err) for err in errors[1:]]


    ratios, bin_centers = zip(*[compute_ratios(hists[0], hist, bin_edges) for hist in hists[1:]])
    bin_centers = bin_centers[0]
    bin_widths = np.diff(bin_centers) 
    bin_widths = np.append(bin_widths, bin_widths[-1]) / 2.0
    
    if debug==True:
        from IPython import embed;embed()

    # start plotting
    for array, hist, name in zip(arrays, hists, names):
        arr_mean, arr_sigma, arr_max, arr_min = np.mean(array), np.std(array), np.max(array), np.min(array)
        label = "{0} $\mu=${1:1.2f} $\sigma$={2:1.2f} max={3:1.2f} min={4:1.2f}".format(name, arr_mean, arr_sigma, arr_max, arr_min)
        ax[0].hist(array, bins=bin_edges, label=label, alpha=0.5, density=True)

    ax[0].set_ylabel("Entries (normalized)")
    if xlabel is not None:
        ax[1].set_xlabel(xlabel, fontsize=15)
    if title is not None:
        ax[0].set_title(title, fontsize=20)
    if log is True:
        ax[0].set_yscale('log')

    ax[0].grid(which='both', axis='y',linestyle="dashed")
    ax[0].xaxis.set_minor_locator(AutoMinorLocator()) 
    ax[0].tick_params(which='minor', length=4, color='black')
    ax[0].legend()

    for ratio, ratio_error, name in zip(ratios, ratio_errors, names[1:]):
        ax[1].errorbar(
            bin_centers,
            ratio,
            xerr=bin_widths,
            yerr=ratio_error,
            linestyle="None",
            marker=None,
            label=name
        )
    ax[1].set_ylabel(
        "$\\frac{{{0}}}{{{1}}}$".format(names[0], "other")
    )
    ax[1].set_ylim(
        0.5, 1.5)

    return fig, ax