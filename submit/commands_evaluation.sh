#!/bin/bash
echo "Pythonpath:"
echo $PYTHONPATH
echo "Sourcing DeepJet env"
source /afs/cern.ch/work/n/neich/private/BTV-HLT-training-tools/setup.sh
echo "Starting Training"
echo "Pythonpath:"
echo $PYTHONPATH
echo "current path:"
pwd
#echo "python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_model.h5 $OnlineTrainingfiles $OnlineDirectory/training_filelist.txt $TrainingOutput/${Training_Version}_pred"
#python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py -h
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_model.h5 $OnlineTrainingFiles $OnlineDirectory/training_filelist.txt $TrainingOutput/${Training_Version}_pred
