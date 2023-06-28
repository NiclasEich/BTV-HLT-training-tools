#!/bin/bash
# echo "Pythonpath:"
# echo $PYTHONPATH
# echo "Sourcing DeepJet env"
#source ${BTVHLTToolsDirectory}/setup.sh
# echo "Pythonpath:"
# echo $PYTHONPATH
#echo "current path:"
#pwd
echo "Starting Training"
python3 $BTVHLTToolsDirectory/DeepJet/Train/train_DeepFlavour.py $OnlineTrainingFiles $TrainingOutput/$TrainingVersion/
