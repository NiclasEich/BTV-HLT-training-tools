#!/bin/bash

for dir in /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/debuggingDefaults_01/*; 
do
    if [ $(basename $dir) != "jet_shaped" ] && [ $(basename $dir) != "plots" ] && ! [ -f $dir ];then
        export condor_proc=$(basename $dir)
        echo "proc = $condor_proc"
        first_file=$(find $dir -type "f" -name "*.root" -print -quit)
        echo "plotting $first_file"
        python3 plotting/plot_tree.py --file $first_file --target /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/debuggingDefaults_01/plots/$condor_proc --process $condor_proc 
    fi
done

