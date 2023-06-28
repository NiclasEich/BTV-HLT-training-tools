#!/bin/bash
#this is a singularity problem only fixed recently
echo "Pythonpath:"
echo $PYTHONPATH
# unset LD_LIBRARY_PATH
unset PYTHONPATH
sing=`which singularity`
# apptainer=`which apptainer`
# unset PATH
MYCUDAVERSION="cuda-10.0"

# export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/$MYCUDAVERSION/lib64:/usr/local/$MYCUDAVERSION/extras/CUPTI/lib64"
# export CUDA_HOME="/usr/local/$MYCUDAVERSION"
echo "If you see the following error: \"container creation failed: mount /proc/self/fd/10->/var/singularity/mnt/session/rootfs error ...\" please just try again"
# $sing run -B /work \
    #   /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cernml4reco/deepjetcore3:3.3.0
apptainer run \
          -B /net/scratch_cms3a/eich \
          --nv \
         /net/scratch_cms3a/eich/BTV/deepjetcore3_latest.sif

