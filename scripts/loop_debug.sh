#!/bin/bash
n=0
total=50

for i in {1..50}
    do
        python3 scripts/debug_uproot_tree_writing.py && n=$((n+1))
    done

echo "Script worked $n/$total times!"
