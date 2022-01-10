import argparse
import os
import subprocess
import numpy as np
import time
from pathlib import Path
from collections import namedtuple, defaultdict

FILE_NUMBERS = {
        "QCD_Pt50to80": 1891,
        "GluGluToHHTo4B_cHHH5": 144,
        "GluGluToHHTo4B_cHHH1": 130,
        "QCD_Pt80to120": 1284,
        "QCD_Pt470to600": 1423,
        "QCD_Pt300to470": 1392,
        "QCD_Pt600toInf": 1464,
        "TTbar_14TeV": 9790,
        "VBFHHTo4B": 136,
        "QCD_Pt120to170": 1991,
        "QCD_Pt170to300": 1330,
        "QCD_Pt30to50": 5115,
        }

    
GLOBAL_FILE_COUNTER = 0

def create_root_file(out_path, file_queue):
    tmp_file_path = "tmp_filelist.txt"

    if os.path.isfile(tmp_file_path):
        raise OSError(f"File {tmp_file_path} should not exist!")

    with open(tmp_file_path, "a") as filelist:
        filelist.write("\n".join(map(str, file_queue)))

    command = "hadd {}.root @{}".format(out_path , str(tmp_file_path))
    print(f"Command-test:\n{command}")
    print(f"filelist:\n", tmp_file_path)
    subprocess.check_call(command , shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
    global GLOBAL_FILE_COUNTER
    GLOBAL_FILE_COUNTER += 1
    print(f"Created file!")
    os.remove(tmp_file_path)

def build_directory_dict(path, test_frac):
    directories = {x.name: {"path": x.path,
                            "root_files": Path(x.path).rglob("**/*.root"),
                            "n_files": FILE_NUMBERS[x.name] 
                            # "n_files": sum(1 for i in Path(x.path).rglob("**/*.root"))
                            } for x in os.scandir(path) if x.is_dir()}
    for name, value in directories.items():
        value["n_test"] = int( value["n_files"] * 1./ test_frac)
        value["n_train"] = value["n_files"] - value["n_test"]
    return directories

def build_files(directory_dict, name_list, out_path, out_name="root_file", number_key="n_train", n_files_per_file=500):

    n_remaining = sum( directory_dict[name][number_key] for name in name_list)
    n_file = 0
    while n_remaining > 0:
        file_list = []
        n_remaining = sum(directory_dict[name][number_key] for name in name_list)
        choices = defaultdict(int)
        for i in range(min(n_files_per_file, n_remaining )):
            choice = np.random.choice( name_list, p=[ directory_dict[proc][number_key]/n_remaining for proc in name_list] )
            choices[choice] += 1
            directory_dict[choice][number_key] -= 1
            file_list.append( next(directory_dict[choice]["root_files"]))
            n_remaining = sum(directory_dict[name][number_key] for name in name_list)
        create_root_file(os.path.join( out_path, "{0}_{1:02d}".format(out_name, n_file)), file_list)
        print("Created file with:\n", ";\t".join("{}: {}".format(name, choices[name]) for name in name_list))
        n_file += 1
        del choices
    return directory_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", help="Base directory ", type=str)
    parser.add_argument("--output", "-o", help="Output directory", type=str, default=False)
    parser.add_argument("--testfrac", "-t", help="Fraction in percentage to use for test, e.g. 10 for 10 percent",
                        default=10, type=int)
    args = parser.parse_args()

    base_dir = args.directory
    out_dir = args.output
    test_path = os.path.join( out_dir, "test")
    train_path = os.path.join( out_dir, "train")
    test_frac = int(args.testfrac)

    if os.path.isdir(args.output):
        raise OSError(f"Path {out_dir} already exists! Please specify a new directory")
    else:
        os.makedirs(out_dir)
        os.makedirs(test_path)
        os.makedirs(train_path)

    directory_dict = build_directory_dict(base_dir, test_frac=test_frac)

    print("Files:")
    for name, value in directory_dict.items():
        print(f"{name}")
        print("N files:\t{}".format(value["n_files"]))

    """
    Test-files
    """
    # build QCD- test files
    qcd_test_path = os.path.join( test_path, "qcd")
    os.makedirs(qcd_test_path)
    qcd_names = [d_name for d_name in directory_dict.keys() if "QCD" in d_name]
    directory_dict = build_files(directory_dict, qcd_names, qcd_test_path, out_name="qcd", number_key="n_test")
    
    # build ttbar test files
    ttbar_test_path = os.path.join( test_path, "ttbar")
    os.makedirs(ttbar_test_path)
    ttbar_names = ["TTbar_14TeV"]
    directory_dict = build_files(directory_dict, ttbar_names, ttbar_test_path, out_name="ttbar", number_key="n_test")

    """
    Train-files
    """
    directory_dict = build_files(directory_dict, list(directory_dict.keys()), train_path, out_name="train_file", number_key="n_train")

    from IPython import embed;embed()
    print(f"GLOBAL_FILE_COUNTER = {GLOBAL_FILE_COUNTER}")

if __name__ == "__main__":
    main()