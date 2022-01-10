import os
import argparse
import uproot3 as ur
from utils.plotting import create_histogram_ratio_figure
from scripts.training_branches import btag_analyzer_key_match, binning


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="Input training file", type=str)
    parser.add_argument("file2", help="Input btaganalyzer file", type=str, default="v00")
    parser.add_argument("--output", "-o", help="Output directory", default="./" )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    with ur.open(args.file1) as file1, ur.open(args.file2) as file2:
        tree1 = file1["ttree"]
        tree2 = file2["btagana/ttree"]
        names = ["training","btanalyzer"]

        for key1, key2 in btag_analyzer_key_match.items():
            print(f"Plotting {key1} vs {key2}")
            array1 = tree1[key1].array().flatten()
            array2 = tree2[key2].array().flatten()

            debug=False
            # if key1 == "TagVarCSV_jetNTracks":
            #     debug = True
            fig, ax = create_histogram_ratio_figure([array1, array2], names, xlabel=key1, title="Comparison-Plot", bins=binning.get(key1, 20), debug=debug)
            fig.savefig( os.path.join( args.output, f"comparisoin_{key1}.png") )

if __name__ == "__main__":
    main()