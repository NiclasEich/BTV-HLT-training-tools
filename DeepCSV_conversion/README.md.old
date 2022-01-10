How to convert a DeepCSV Keras model to a json used in CMSSW:

Needed: model.h5 file and the DataCollection.dc file. 

1. clone: https://github.com/lwtnn/lwtnn.git (commit I used was f1ab0fab883a1ffb1dcd12a960a9662b7b899a56, so if in doubt try with that commit)

2. write the weights to 'DeepCSV_weights.h5' and the architecture to 'DeepCSV_arch.json', this is done with the command: 
```
python save_architecture.py model.h5
```

Note here, that the architecture of DeepCSV is hard coded in this script, because keras2json.py does not work with the functional API of keras. So one needs to check, that it is actually correct. (By default it has to agree with DeepJet.modules.models.dense.dense_model)

3. write out the offsets and stddevs from the datacollection to DeepCSV_var.json and the default values for each variable to defaults.json, using:
```
python load_dc.py Datacollection.dc
```
The names of the output classes are hard coded in this script to ['probb', 'probbb', 'probc', 'probudsg'].

4. Finally do the conversion with:
```
python3 lwtnn/converters/keras2json.py  DeepCSV_arch.json  DeepCSV_var.json  DeepCSV_weights.h5 > DeepCSV_Phase2.json
```

Somehow the defaults of the variables are not written to DeepCSV_Phase2.json, therefore in DeepCSV_Phase2.json one needs to navigate to the line reading "defaults : {}"
And replace the curly brackets with the content of defaults.json (which is created when running load_dc.py).

5. run ./rename.sh 
This replaces the names of the variables with the ones used in CMSSW. (Need to check whether jetEta or jetAbsEta was used)
