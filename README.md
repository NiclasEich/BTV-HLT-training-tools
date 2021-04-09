# BTV-HLT-training-tools
Collection of miscellaneous tools for the retraining of DeepCSV and DeepJet on online data for run 3 and phase 2.

## Instructions
Cloning the repo, including submodules:
```shell
git clone --recursive https://github.com/NiclasEich/BTV-HLT-training-tools
```

## Input files
List of input files with descriptions can be found in `FILES.md`

## Offline files

The offline training files were provieded by Max Neukum and can be found  on lxplus here:
```shell
/afs/cern.ch/work/n/neich/public/max_files
```


## Example

Comparing two datasets:

```shell
python3 scripts/plot_dataset_comparison.py -i ../BTV/new_trees/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root -o v05 -t /eos/home-s/sewuchte/www/BTV/NiclasPlayground/
```

Converting a root file from event on the first axis to single jets:

```shell
python3 scripts/convert_events_to_jets.py -i /eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv00_TICL/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root -o /afs/cern.ch/work/n/neich/public/online_files_test`
```

## Run Training

The Software setup for converting the files and training the model is provided in a singularity container (`/eos/home-j/jkiesele/singularity/images/deepjetcore3_latest.sif`)
that needs to be started first.

If you want everything to run locally.

```shell
source submit/run_deepjetcore3_lxplus.sh
```

Otherwise one should use the HTCondor-submission for this or start and interactive
condor-job with

```shell
condor_submit -interactive submit/sing_interactive.sub
```

This spawns a job on a machine with the singularity


### First convert Files to the DJDC-format

First you have to convert your root files, with their paths ins `/path/to/offline_training_filelist.txt`, to
the DJDC-dataformat.

```shell
python3 DeepJetCore/bin/convertFromSource.py -i /path/to/offline_training_filelist.txt -o /path/to/offline_djdc_files -c TrainData_DeepCSV
```

It might be possible that you need to raise your ulimit if there are too many files that need to be processed:

```shell
ulimit -n 4096
```

### Second run Training script

Then you can run the Training

```shell
python3 DeepJet/Train/train_DeepCSV.py offline_djdc_files/dataCollection.djcdc offline_results
```

### Evaluate Training


```shell
python3 DeepJetCore/bin/predict.py /KERAS_model.h5 offline_djdc_files/dataCollection.djcdc offline_training_files/offline_training_test_filelist.txt offline_results/prediction
```

Create ROC-curve

```shell
python3 DeepJet/scripts/plot_roc.py
```

Plot ROC-curve

```shell
python3 plotting/plot_roc.py
```
