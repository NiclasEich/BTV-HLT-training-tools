echo "$BTVHLTToolsDirectory"
#source ${BTVHLTToolsDirectory}/setup.sh

proc=$condor_proc

base=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3_220103/test
out=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3_220103_jet_shaped_02_deepCSV/test/qcd

mkdir $out

#num=$(printf "%03d" $1)

num=$(printf "%02d" $1)

#file=${base}/${proc}/${proc}_${num}.root

file=${base}/qcd/qcd_${num}.root
echo "Processing $file"
# echo "python3 -u ${BTVHLTToolsDirectory}/scripts/convert_events_to_jets.py -i $file -o $out --key all"
python3 -u $BTVHLTToolsDirectory/scripts/convert_events_to_jets.py -i $file -o $out --key qcd --deepCSV
