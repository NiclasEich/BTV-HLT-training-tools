#!/bin/sh

echo "Your path:"
echo "$base"
base=$1
dir=`basename $1`
echo "Base: $dir"
processes=$(ls $base)

echo "Files in process-paths"
for d in $processes; do
    working_dir=$base/$d
    if [[ -d $working_dir ]]; then
        echo
        echo "Starting Process: $d $(ls $1/$d | wc -l) Files"
        ls $1/$d/*.root | sort > "/tmp/${d}_source_files.txt"
        #echo -e "Executing command:\nhadd ${working_dir}_${dir} $(< /tmp/${d}_source_files.txt)"  | sed 's/^/    /'
        hadd ${working_dir}_${dir}.root $(< /tmp/${d}_source_files.txt)
        rm "/tmp/${d}_source_files.txt" 
    fi
done
