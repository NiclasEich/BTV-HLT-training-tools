#!/bin/bash
echo "Reading in files and converting them"
python3 scripts/convert_events_to_jets.py -i /eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv00_TICL/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root  -o /afs/cern.ch/work/n/neich/public/online_files_test
python3 scripts/convert_events_to_jets.py -i /eos/home-s/sewuchte/BTV-Phase2/December_TDR/hadded/HLT_TRKv06p1_TICL/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv06p1_TICL_default.root -o /afs/cern.ch/work/n/neich/public/online_files_test

echo  "Starting to plot comparison"
python3 scripts/plot_dataset_comparison.py -i /afs/cern.ch/work/n/neich/public/online_files_test/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv00_default.root -o v01 -t /eos/home-s/sewuchte/www/BTV/NiclasPlayground/
python3 scripts/plot_dataset_comparison.py -i /afs/cern.ch/work/n/neich/public/online_files_test/Phase2HLTTDR_TTbar_14TeV_PU200_HLT_TRKv06p1_TICL_default.root -o v01 -t /eos/home-s/sewuchte/www/BTV/NiclasPlayground/
