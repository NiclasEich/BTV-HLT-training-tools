#!/bin/bash
echo "Pythonpath:"
echo $PYTHONPATH
echo "Sourcing DeepJet env"
source ${BTVHLTToolsDirectory}/setup.sh
echo "Starting Training"
echo "Pythonpath:"
echo $PYTHONPATH
echo "current path:"
pwd
python3 $BTVHLTToolsDirectory/DeepJet/Train/train_DeepCSV.py $OnlineTrainingFiles $TrainingOutput/${TrainingVersion}_deepCSV/
