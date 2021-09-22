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
echo "$BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred -b 1000"
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred -b 1000
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py
python3 $BTVHLTToolsDirectory/plotting/plot_history.py
