# get basedirectory
export BTVHLTToolsDirectory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# source DeepJet env
source $BTVHLTToolsDirectory/DeepJet/env.sh

if test -f "$BTVHLTToolsDirectory/local_setup.sh";
then
    source local_setup.sh
else
    echo "No local_setup.sh found!\n Using defaults for env vars"
fi


if [ -z "$TrainingOutput" ]
then
      echo "\$TrainingOutput is empty"
      export TrainingOutput="${BTVHLTToolsDirectory}/training_output"
      echo "Creating training-output directory!"
      mkdir $TrainingOutput
      echo "\$TrainingOutput set to ${TrainingOutput}"
fi

