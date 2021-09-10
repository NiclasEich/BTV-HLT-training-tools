#!/bin/bash

#declare -a array=("GluGluToHHTo4B_cHHH1" "QCD_Pt120to170_flat" "QCD_Pt20to30_flat" "QCD_Pt50to80_flat" "GluGluToHHTo4B_cHHH2p45"  "QCD_Pt15to7000_pu0to80"  "QCD_Pt300to470_flat"  "QCD_Pt600toInf_flat" "TTbar_14TeV")
declare -a array=("QCD_Pt300to470_flat"  "QCD_Pt600toInf_flat" "TTbar_14TeV")

arraylength=${#array[@]}

base=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3files
out=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/jet_shaped
logfile=$out/conversion.log

for  (( i=0; i<${arraylength}; i++ ));
do
    proc=${array[$i]}
    for f in $(ls $base/$proc/*.root)
    do
        echo "Processing $f"
        python3 -u scripts/convert_events_to_jets.py -i $f -o $out | tee -a $logfile
    done
done
