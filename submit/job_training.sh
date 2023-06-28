#!/bin/bash
#this is a singularity problem only fixed recently
echo ${BTVHLTToolsDirectory}/setup.sh
source ${BTVHLTToolsDirectory}/setup.sh
echo ""
echo "Pythonpath:"
echo $PYTHONPATH | sed "s/:/\n/g"
echo "Path:"
echo $PATH | sed "s/:/\n/g"
echo "LDLIbrarypath:"
echo $LD_LIBRARY_PATH | sed "s/:/\n/g"

#unset PATH
echo "If you see the following error: \"container creation failed: mount /proc/self/fd/10->/var/singularity/mnt/session/rootfs error ...\" please just try again"
apptainer run \
          -B /net/scratch_cms3a/eich \
          -B /usr/lib \
          --nv \
          /net/scratch_cms3a/eich/BTV/deepjetcore3_latest.sif
          $BTVHLTToolsDirectory/submit/commands_training.sh
