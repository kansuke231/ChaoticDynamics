#!/bin/bash

for i in `seq .0 .5 10.0`; do
	./a.out 0.0 0.005 10000 ${i} 0.0 > output/Q4_b15/Q4_${i}.txt;
	./a.out 0.0 0.005 10000 -${i} 0.0 > output/Q4_b15/Q4_minus_${i}.txt;
done

for i in `seq 5.0 2.5 12.5`; do
	./a.out 0.0 0.005 10000 -10.0 ${i} > output/Q4_b15/Q4_vertical_${i}.txt;
	./a.out 0.0 0.005 10000 10.0 -${i} > output/Q4_b15/Q4_vertical_minus_${i}.txt;
done

# using GNU parallel.
#seq 20.0 1.0 25.0 | parallel ./a.out 0.0 0.005 10000 10.0 {} > output/Q3/Q3_vertical_{}.txt
#seq 20.0 1.0 25.0 | parallel ./a.out 0.0 0.005 10000 -10.0 -{} > output/Q3/Q3_vertical_minus_{}.txt
