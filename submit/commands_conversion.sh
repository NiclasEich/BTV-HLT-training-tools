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
python3 $BTVHLTToolsDirectory/DeepJetCore/bin/convertFromSource.py -i $OnlineDirectory/training_filelist.txt -o $OnlineDirectory/djdc_files/$TrainingVersion -c TrainData_DeepCSV
