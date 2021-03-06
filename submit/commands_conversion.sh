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
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/convertFromSource.py -i $OnlineDirectory/training_filelist.txt -o $OnlineDirectory/djdc_files/$TrainingVersion -c TrainData_DeepCSV
