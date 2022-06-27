#!/bin/sh

max=2
#create a csv file
python3 ./performance/create_csv.py

for i in `seq 1 $max`
do
    var=$(time python3 test.py $i $i)
    z=$(echo "$var" | awk '{print $3}')
    t=$(echo "$var" | awk -F '/0m/ {print $2}')
    python3 ./performance/add_row.py $i $i 'dualoc' "${z}" "${t}" 
done

#    python3 test.py $i $i > /dev/null
