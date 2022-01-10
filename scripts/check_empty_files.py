import uproot as ur
from pathlib import Path
from tqdm import tqdm
from zlib import error as zlibError
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="Base directory ", type=str)
args = parser.parse_args()

ppath  = Path(args.directory)


broken_files = []
pbar = tqdm(list(ppath.glob("**/*.root")))

for file_path in pbar:
    pbar.set_description("Broken: {0:2d}".format( len(broken_files) ))
    broken = False
    try:
        with ur.open(file_path) as root_file:
            tree = root_file["ttree"]
            for key in tree.keys():
                if len(tree[key].array()) == 0:
                    broken = True
                    break
        if broken is True:
            broken_files.append("".join(str(file_path).split("/")[-2:]))
    except ValueError as e:
        print("File is broken and seems to be empty!")
        print("path:\n", file_path)
        broken_files.append("".join(str(file_path).split("/")[-2:]))
    except zlibError as e:
        print("File has some zlib issues?!")
        print("path:\n", file_path)
        broken_files.append("".join(str(file_path).split("/")[-2:]))
print("Broken:\n{}".format(broken_files))
