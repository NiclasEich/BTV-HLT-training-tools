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
echo "python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_model.h5 $OnlineTrainingFiles $OnlineDirectory/training_filelist.txt $TrainingOutput/${TrainingVersion}_pred"
#python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py -h
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred -b 1000
python3 DeepJet/scripts/plot_roc.py
python3 plotting/plot_roc.py
python3 plotting/plot_history.py
