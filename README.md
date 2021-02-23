# BTV-HLT-training-tools
Collection of miscellaneous tools for the retraining of DeepCSV and DeepJet on online data for run 3 and phase 2.


## Example

Comparing two datasets:

`python3 scripts/plot_dataset_comparison.py -i ../BTV/new_trees/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root -o v05 -t /eos/home-s/sewuchte/www/BTV/NiclasPlayground/`

Converting a root file from event on the first axis to single jets:

`python3 scripts/convert_events_to_jets.py -i /eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv00_TICL/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root -o /afs/cern.ch/work/n/neich/public/online_files_test`
