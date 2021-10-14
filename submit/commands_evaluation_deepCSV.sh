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
echo "$BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_CSV/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred -b 1000"
#python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_deepCSV/KERAS_check_best_model.h5 $OnlineTrainingFilesDeepCSV $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_deepCSV_pred -b 1000
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --deepCSV
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_deepCSV_pred -o $TrainingOutput/${TrainingVersion}_deepCSV_pred
python3 $BTVHLTToolsDirectory/plotting/plot_history.py -i $TrainingOutput/${TrainingVersion}_deepCSV/ -o $TrainingOutput/${TrainingVersion}_deepCSV_pred

