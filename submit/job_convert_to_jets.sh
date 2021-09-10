base=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3files
out=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/jet_shaped
logfile=$out/conversion.log

proc="TTbar_14TeV"
num=$(printf "%03d" $1)
file=${base}/${proc}/${proc}_${num}.root
echo "Processing $f"
python3 -u scripts/convert_events_to_jets.py -i $file -o $out
