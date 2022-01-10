#!/bin/bash

echo "Starting deepCSV model-conversion"
tmp_path=$1/json_conversion
mkdir $tmp_path 
cp $TrainingOutput/${TrainingVersion}_deepCSV/KERAS_check_best_model.h5 $tmp_path/model.h5
ln -s $OnlineTrainingFilesDeepCSV $tmp_path/trainsamples.djdc
for i in ${OnlineDataConvertedDeepCSV}/train_file_*;
do 
    ln -s $i $tmp_path/$(basename $i)
done
python3 $BTVHLTToolsDirectory/DeepCSV_conversion/save_architecture.py $tmp_path/model.h5 -o $tmp_path
python3 $BTVHLTToolsDirectory/DeepCSV_conversion/load_dc.py $tmp_path/trainsamples.djdc -o $tmp_path
python3 $BTVHLTToolsDirectory/DeepCSV_conversion/lwtnn/converters/keras2json.py $tmp_path/DeepCSV_arch.json $tmp_path/DeepCSV_var.json $tmp_path/DeepCSV_weights.h5 > $tmp_path/DeepCSV_model.json
source $BTVHLTToolsDirectory/DeepCSV_conversion/rename.sh $tmp_path/DeepCSV_model.json