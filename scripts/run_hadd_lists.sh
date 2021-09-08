#!/bin/bash

declare -a array=("GluGluToHHTo4B_cHHH1" "QCD_Pt120to170_flat" "QCD_Pt20to30_flat" "QCD_Pt50to80_flat" "GluGluToHHTo4B_cHHH2p45"  "QCD_Pt15to7000_pu0to80"  "QCD_Pt300to470_flat"  "QCD_Pt600toInf_flat" "TTbar_14TeV")

arraylength=${#array[@]}

for  (( i=0; i<${arraylength}; i++ ));
do
    proc=${array[$i]}
    echo "Creating directory for $proc"
    mkdir /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3files/$proc
    python3 scripts/hadd_root_dir.py -n $proc -p $proc -o /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/run3files/$proc -d /nfs/dust/cms/user/neich/BTV/nTuple-Producer/CMSSW_12_0_0_pre6/src/RecoBTag/PerformanceMeasurements/test/condor
done

