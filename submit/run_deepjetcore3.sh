#/bin/bash

SINGULARITY_CACHEDIR="/afs/cern.ch/work/n/neich/private/BTV/singularity/"

#this is a singularity problem only fixed recently
unset LD_LIBRARY_PATH
unset PYTHONPATH
sing=`which singularity`
unset PATH
cd 
echo "If you see the following error: \"container creation failed: mount /proc/self/fd/10->/var/singularity/mnt/session/rootfs error ...\" please just try again"
$sing run -B /eos -B /afs --bind /etc/krb5.conf:/etc/krb5.conf --bind /proc/fs/openafs/afs_ioctl:/proc/fs/openafs/afs_ioctl --bind /usr/vice/etc:/usr/vice/etc  --nv /eos/home-j/jkiesele/singularity/images/deepjetcore3_latest.sif


echo "Sourcing DeepJet env"
source /afs/cern.ch/work/n/neich/private/BTV/DeepJet/env.sh
cd /afs/cern.ch/work/n/neich/private/BTV
echo "Starting Training"
python3 DeepJet/Train/train_DeepCSV.py /afs/cern.ch/work/n/neich/public/offline_djdc_files/files_04/dataCollection.djcdc offline_results/new_preprocessing_06
