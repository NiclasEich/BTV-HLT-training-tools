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
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/predict.py $TrainingOutput/out_01/KERAS_model.h5 /afs/cern.ch/work/n/neich/public/offline_djdc_files/files_04/dataCollection.djcdc /eos/cms/store/group/phys_btag/HLTRetraining/offline_training_files/offline_training_test_filelist.txt $TrainingOutput/out_01_pred
