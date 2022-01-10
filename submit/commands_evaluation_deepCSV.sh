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
echo "$BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_CSV/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFilesDeepCSV $TrainingOutput/${TrainingVersion}_pred -b 1000"

mkdir $TrainingOutput/${TrainingVersion}_deepCSV_pred

python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_deepCSV/KERAS_check_best_model.h5 $OnlineTrainingFilesDeepCSV $OnlineEvaluationFilesDeepCSV $TrainingOutput/${TrainingVersion}_deepCSV_pred/all -b 1000
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_deepCSV/KERAS_check_best_model.h5 $OnlineTrainingFilesDeepCSV $OnlineEvaluationFilesDeepCSV_QCD $TrainingOutput/${TrainingVersion}_deepCSV_pred/QCD -b 1000
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}_deepCSV/KERAS_check_best_model.h5 $OnlineTrainingFilesDeepCSV $OnlineEvaluationFilesDeepCSV_ttbar $TrainingOutput/${TrainingVersion}_deepCSV_pred/ttbar -b 1000

python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --deepCSV --input_dir $TrainingOutput/${TrainingVersion}_deepCSV_pred/all
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --deepCSV --input_dir $TrainingOutput/${TrainingVersion}_deepCSV_pred/QCD
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --deepCSV --input_dir $TrainingOutput/${TrainingVersion}_deepCSV_pred/ttbar

python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_deepCSV_pred/all -o $TrainingOutput/${TrainingVersion}_deepCSV_pred --deepCSV --tag all
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_deepCSV_pred/ttbar -o $TrainingOutput/${TrainingVersion}_deepCSV_pred --deepCSV --tag ttbar
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_deepCSV_pred/QCD -o $TrainingOutput/${TrainingVersion}_deepCSV_pred --deepCSV --tag QCD
python3 $BTVHLTToolsDirectory/plotting/plot_efficiency_along_axis.py -i $TrainingOutput/${TrainingVersion}_deepCSV_pred -o $TrainingOutput/${TrainingVersion}_deepCSV_pred/plots --deepCSV
python3 $BTVHLTToolsDirectory/plotting/plot_history.py -i $TrainingOutput/${TrainingVersion}_deepCSV/ -o $TrainingOutput/${TrainingVersion}_deepCSV_pred
./scripts/convert_deepCSV.sh ${TrainingOutput}/${TrainingVersion}_deepCSV_pred