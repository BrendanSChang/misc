#!/bin/bash

for i in `seq 1 10`
do
	echo Iteration $i
	python ./ovnbandwidthtest.py > ./output/output_$i
done
