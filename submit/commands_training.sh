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
python3 $BTVHLTToolsDirectory/DeepJet/Train/train_DeepCSV.py $OfflineTrainingFiles $TrainingOutput/$Training_Version
