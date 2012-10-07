#!/bin/bash

rm site/img/h-*.png

for x in $(seq 10)
do
    convert -modulate 100,100,$((30 + 7 * x)) -resize $((70 + x * 3))% house.png site/img/h-$x.png
done
