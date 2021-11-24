import uproot as ur
from pathlib import Path
from tqdm import tqdm

ppath  = Path("/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/no_zero_cpfcan")

broken_files = []
pbar = tqdm(list(ppath.glob("**/*.root")))

for file_path in pbar:
    pbar.set_description("Broken: {0:2d}".format( len(broken_files) ))
    broken = False
    with ur.open(file_path) as root_file:
        tree = root_file["ttree"]
        for key in tree.keys():
            if len(tree[key].array()) == 0:
                broken = True
                break
    if broken is True:
        broken_files.append("".join(str(file_path).split("/")[-2:]))
print("Broken:\n{}".format(broken_files))
