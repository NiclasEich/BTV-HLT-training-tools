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
python3 /afs/cern.ch/work/n/neich/private/BTV-HLT-training-tools/DeepJetCore/bin/convertFromSource.py -i /eos/cms/store/group/phys_btag/HLTRetraining/offline_training_files/offline_training_all_filelist.txt -o /afs/cern.ch/work/n/neich/public/offline_djdc_files/new_version_01 -c TrainData_DeepCSV
