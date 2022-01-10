UPDATED: 2021_02_04

This recipe shows how to convert DeepCSV Keras model (.h5) trained in DeepJetCore to a json used in CMSSW.
The recipe works but there might be unnecessary code lines due to time restrictions..

Note: scripts have been updated and do not work with the previous recipe (pre djc2) anymore. Please look at an older version of the repo for that, 2020 or earlier.

Needed: model.h5 file, DeepJetCore container, the dataCollection.djcdc file, training .root files (links are enough)

1. clone this repo and work in DeepCSV_conversion directory

2. clone: https://github.com/lwtnn/lwtnn.git (commit I used was f1ab0fab883a1ffb1dcd12a960a9662b7b899a56, so if in doubt try with that commit)

3. get all necessary files:
```
cp <your_training_dir>/KERAS_model.h5 ./model.h5
ln -s <dir_with_training_root_files>/dataCollection.djcdc trainsamples.djcdc
for i in <dir_with_training_root_files>/ntuple_merged_*; do ln -s $i ./`basename $i`; done
```

Following steps have to be executed in the DJC container to access tensorflow, etc.

4. write the weights to 'DeepCSV_weights.h5' and the architecture to 'DeepCSV_arch.json', this is done with the command: 
```
python3 save_architecture.py model.h5
```

Note here, that the architecture of DeepCSV is hard coded in this script, because keras2json.py does not work with the functional API of keras. So one needs to check, that it is actually correct. (By default it has to agree with DeepJet.modules.models.dense.dense_model)

5. write out the offsets and stddevs from the datacollection to DeepCSV_var.json and the default values for each variable to defaults.json, using:
```
python3 load_dc.py trainsamples.djcdc
```
The names of the output classes are hard coded in this script to ['probb', 'probbb', 'probc', 'probudsg'].

6. Finally do the conversion with:
```
python3 lwtnn/converters/keras2json.py  DeepCSV_arch.json  DeepCSV_var.json  DeepCSV_weights.h5 > DeepCSV_Phase2.json
```

7. Somehow the defaults of the variables are not written to DeepCSV_Phase2.json, therefore in DeepCSV_Phase2.json one needs to navigate to the line reading "defaults : {}"
And replace the curly brackets with the content of defaults.json (which is created when running load_dc.py).

8. run `. rename.sh DeepCSV_Phase2.json` 
This replaces the names of the variables with the ones used in CMSSW. (Need to check whether jetEta or jetAbsEta was used -> it is jetEta)

The model is now converted.

9. optional: check that the converted model gives same result in training environment and BTA
I suggest extracting ~100 events from a MiniAOD file, run DeepNTuplizer and prediction for the prediction ntuple. Also run BTA with the converted model on the same sample.

Then you can run the script "match_it.py" in this directory. It is a simple script that loops over jets, matches them and prints tagger values. Feel free to change it to your needs.
