#!/bin/bash

stressurl="http://192.168.49.2:31267/stress"
loadurl="http://192.168.49.2:31267/cpu"

out="$(basename $0).txt"

# Baseline
for i in $(seq 20); do 
	curl -s $loadurl >> $out
	sleep 1
done
# Generate Load	
curl -s ${stressurl} >/dev/null 2>&1 &

# Measure
for i in $(seq 20); do 
	curl -s $loadurl >> $out
	sleep 1
done

