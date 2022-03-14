#!/bin/bash
echo "Pythonpath:"
echo $PYTHONPATH
echo "Sourcing DeepJet env"
# source ${BTVHLTToolsDirectory}/setup.sh
echo "Starting Training"
echo "Pythonpath:"
echo $PYTHONPATH
echo "current path:"
pwd
echo "$BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/$TrainingVersion/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred -b 1000"
mkdir $TrainingOutput/${TrainingVersion}_pred

python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles_QCD $TrainingOutput/${TrainingVersion}_pred/QCD -b 1000
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --input_dir $TrainingOutput/${TrainingVersion}_pred/QCD
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_pred/QCD -o $TrainingOutput/${TrainingVersion}_pred --tag QCD


python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles_ttbar $TrainingOutput/${TrainingVersion}_pred/ttbar -b 1000
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --input_dir $TrainingOutput/${TrainingVersion}_pred/ttbar
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_pred/ttbar -o $TrainingOutput/${TrainingVersion}_pred --tag ttbar

python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/${TrainingVersion}/KERAS_check_best_model.h5 $OnlineTrainingFiles $OnlineEvaluationFiles $TrainingOutput/${TrainingVersion}_pred/all -b 1000
python3 $BTVHLTToolsDirectory/DeepJet/scripts/plot_roc.py --input_dir $TrainingOutput/${TrainingVersion}_pred/all
python3 $BTVHLTToolsDirectory/plotting/plot_roc.py -i $TrainingOutput/${TrainingVersion}_pred/all -o $TrainingOutput/${TrainingVersion}_pred --tag all

python3 $BTVHLTToolsDirectory/plotting/plot_history.py
python3 $BTVHLTToolsDirectory/plotting/plot_efficiency_along_axis.py -i $TrainingOutput/${TrainingVersion}_pred -o $TrainingOutput/${TrainingVersion}_pred/plots
python3 $BTVHLTToolsDirectory/scripts/convert_to_onnx.py --infile $TrainingOutput/$TrainingVersion/KERAS_check_best_model.h5 --outfile $TrainingOutput/${TrainingVersion}_pred/DeepJet_model.onnx
