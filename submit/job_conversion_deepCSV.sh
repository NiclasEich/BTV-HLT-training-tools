#!/bin/bash
#this is a singularity problem only fixed recently
echo "Pythonpath:"
echo $PYTHONPATH
unset LD_LIBRARY_PATH
unset PYTHONPATH
sing=`which singularity`
unset PATH
echo "BTVHLTToolesdirectory:"
echo $BTVHLTToolsDirectory
echo $(pwd)
echo "If you see the following error: \"container creation failed: mount /proc/self/fd/10->/var/singularity/mnt/session/rootfs error ...\" please just try again"
$sing run -B /nfs \
          --bind /proc/fs/openafs/afs_ioctl:/proc/fs/openafs/afs_ioctl \
          --nv \
          /nfs/dust/cms/user/sewuchte/public/deepjetcore3_latest.sif \
           ${BTVHLTToolsDirectory}/submit/commands_conversion_deepCSV.sh
