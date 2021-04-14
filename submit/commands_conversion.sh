#!/bin/bash
echo "Pythonpath:"
echo $PYTHONPATH
echo "Sourcing DeepJet env"
source /afs/cern.ch/work/n/neich/private/BTV-HLT-training-tools/DeepJet/env.sh
echo "Starting Training"
echo "Pythonpath:"
echo $PYTHONPATH
echo "current path:"
pwd
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/convertFromSource.py -i $OfflineDirectory/training_filelist.txt -o $OfflineDirectory/djdc_files/out_01 -c TrainData_DeepCSV
