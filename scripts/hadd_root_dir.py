import argparse
import os
import subprocess
from pathlib import Path

N_JETS = int( 5*1e3)
N_FILE = int( 5*1e6)

N_QUEUE = N_FILE/N_JETS

parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-d", help="Base directory ", type=str)
parser.add_argument("--output", "-o", help="Output directory", type=str, default=False)
parser.add_argument("--fname", "-n", help="Name for output files", type=str, default="output")
parser.add_argument("--process", "-p", help="Proc-name to parse, e.g. QCD_Pt20to30_flat. Give none for wildcard", default="*")
args = parser.parse_args()

file_queue = []
file_queue_n = 0
file_idx = 0
tmp_file_path = "tmp_filelist.txt"
print("Removing pot. filelist")
print("Running on {}!".format(args.process))
print("Running in\n{}".format(args.directory))
try:
    os.remove(tmp_file_path)
except FileNotFoundError:
    pass

os.makedirs(str(args.output), exist_ok=True)

for root_file in Path(args.directory).rglob("**/{}/**/*.root".format(args.process)):
    if file_queue_n == N_QUEUE: 
        with open(tmp_file_path, "a") as filelist:
            filelist.write("\n".join(map(str, file_queue)))
        command = "hadd {}.root @{}".format(os.path.join( str(args.output), str(args.fname) + "_{0:03d}".format(file_idx) ) , str(tmp_file_path))
        file_idx += 1
        file_queue = []
        file_queue_n = 0
        # print(command)
        print("Executing hadd!")
        subprocess.check_call( command , shell=True)
        os.remove(tmp_file_path)
    file_queue.append( root_file )
    file_queue_n += 1

file_idx += 1
with open(tmp_file_path, "a") as filelist:
    filelist.write("\n".join(map(str, file_queue)))
command = r"hadd {}.root @{}".format(os.path.join( str(args.output), str(args.fname) + "_{0:03d}".format(file_idx) ) , str(tmp_file_path))

file_queue = []
file_queue_n = 0
subprocess.check_call( command, shell=True )
os.remove(tmp_file_path)

print("In total saved files: {}".format(file_idx +1))
