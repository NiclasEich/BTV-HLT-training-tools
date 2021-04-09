# List of input files


## Offline/MINIAOD

### Phase II

#### From Max Neukum, tagged deepntuplizer_11_2_pv3d_newTrackCollection
```shell
/eos/cms/store/group/phys_btag/HLTRetraining/PhaseII/Offline/Max_deepntuplizer_11_2_pv3d_newTrackCollection/
```
Description of files and names goes here.



## Online/HLT

### Phase II

#### HLT TDR samples, tagged HLTTDR_February2021
```shell
/eos/cms/store/group/phys_btag/HLTRetraining/PhaseII/Online/HLTTDR_February2021/
```
Description of names:
`TRKv00` = Offline-like tracking reconstruction
`TRKv06p1` = HLT TDR baseline tracking reconstruction
`TRKv07p2` = HLT TDR alternative tracking reconstruction, including skimming of tracks

`TICL` = the iterative clustering - reconstruction for HGCal, not used in current Offline/MINIAOD. If omitted, standard simPF based offline reconstruction is used

`_cutsV0`-`_cutsV2`/`_default` correspond to different optimisations for the BTV HLT sequence. `deftault`=Offline, `cutsV2`= HLT TDR default

`NoPU`, `PU140`, `PU200` indicate the pile-up scenario of the sample
