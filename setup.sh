# get basedirectory
export BTVHLTToolsDirectory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# source DeepJet env

source $BTVHLTToolsDirectory/DeepJet/env.sh

export PYTHONPATH=$BTVHLTToolsDirectory:$PYTHONPATH
export PYTHONPATH=$BTVHLTToolsDirectory/DeepJetCore:$PYTHONPATH
export PYTHONPATH=$BTVHLTToolsDirectory/DeepJetCore/compiled:$PYTHONPATH
export PYTHONPATH=$BTVHLTToolsDirectory/DeepJetCore/conversion:$PYTHONPATH
export PYTHONPATH=$BTVHLTToolsDirectory/DeepJet/modules:$PYTHONPATH
export PYTHONPATH=$BTVHLTToolsDirectory/DeepJet/modules/models:$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/afs/desy.de/user/n/neich/.local/lib/python3.6/site-packages/
export PYTHONPATH=$PYTHONPATH:/lib/python3.6/site-packages/
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/

export LD_LIBRARY_PATH=/usr/share/DJC/DeepJetCore/compiled:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=$BTVHLTToolsDirectory/DeepJetCore/compiled:$LD_LIBRARY_PATH

if test -f "$BTVHLTToolsDirectory/local_setup.sh";
then
    source $BTVHLTToolsDirectory/local_setup.sh
else
    echo "No local_setup.sh found! Using defaults for env vars"
fi


if [ -z "$TrainingOutput" ]
then
      echo "\$TrainingOutput is empty"
      export TrainingOutput="${BTVHLTToolsDirectory}/training_output"
      if [[ -d $TrainingOutput ]];then
          echo "$TrainingOutput already exists!"
      else
          echo "Creating training-output directory!"
          mkdir -p $TrainingOutput
      fi
      echo "\$TrainingOutput set to ${TrainingOutput}"
fi
