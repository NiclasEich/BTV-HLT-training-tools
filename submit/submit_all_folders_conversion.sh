#!/bin/bash

base=/nfs/dust/cms/user/neich/BTV/nTuple-Producer/files/merged

for proc in $base/*;
do
   proc_name=$(basename $proc)
   if [ $proc_name != "jet_shaped" ] && [ $proc_name != "plots" ];then
       export condor_proc=$proc_name
       condor_submit /nfs/dust/cms/user/neich/BTV/BTV-HLT-training-tools/submit/submit_batch_conversion.sub  
   fi
done
