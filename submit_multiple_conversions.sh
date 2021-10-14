#!/bin/bash

dirpath=

for dir in /nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged/*;
do
    if [ $(basename $dir) != "jet_shaped" ];then
        export condor_proc=$(basename $dir)
        echo "proc = $condor_proc"
        condor_submit ./submit/submit_batch_conversion.sub
    fi
done
    
