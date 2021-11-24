
echo "$BTVHLTToolsDirectory"
#source ${BTVHLTToolsDirectory}/setup.sh

proc=$condor_proc

base=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged/
out=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/debuggingDefaults/$proc/

mkdir $out

#num=$(printf "%03d" $1)

num=$1

#file=${base}/${proc}/${proc}_${num}.root

file=${base}/${proc}/ntuple_merged_${num}.root
echo "Processing $file"
echo "python3 -u ${BTVHLTToolsDirectory}/scripts/convert_events_to_jets.py -i $file -o $out --key $proc"
python3 -u $BTVHLTToolsDirectory/scripts/convert_events_to_jets.py -i $file -o $out --key $proc
