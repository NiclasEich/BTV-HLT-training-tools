#!/bin/bash
#this is a singularity problem only fixed recently
echo "Pythonpath:"
echo $PYTHONPATH
unset LD_LIBRARY_PATH
unset PYTHONPATH
sing=`which singularity`
unset PATH
echo "If you see the following error: \"container creation failed: mount /proc/self/fd/10->/var/singularity/mnt/session/rootfs error ...\" please just try again"
$sing exec -B /eos \
           -B /afs \
           --bind /etc/krb5.conf:/etc/krb5.conf \
           --bind /proc/fs/openafs/afs_ioctl:/proc/fs/openafs/afs_ioctl \
           --bind /usr/vice/etc:/usr/vice/etc  \
           --nv \
           /eos/home-j/jkiesele/singularity/images/deepjetcore3_latest.sif \
           ${BTVHLTToolsDirectory}/submit/commands_conversion.sh

