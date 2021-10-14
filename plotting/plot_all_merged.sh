#!/bin/bash

dirpath=

for dir in /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged/jet_shaped/*;
do
    if [ $(basename $dir) != "jet_shaped" ];then
        export condor_proc=$(basename $dir)
        echo "proc = $condor_proc"
        python3 plotting/plot_tree.py --file /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged/jet_shaped/${condor_proc}/ntuple_merged_0_default_0.root --target /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged/jet_shaped/plots/$condor_proc --process $condor_proc 

    fi
done

