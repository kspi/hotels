#!/bin/bash

rm site/img/h-*.png

for x in $(seq 10)
do
    convert -modulate 100,100,$((30 + 7 * x)) -resize $((70 + x * 3))% img/house.png site/img/h-$x.png
done


tilenames() {
    local active=$1
    local inactive=$((5 - active))
    for x in `seq $active`; do echo -n "img/star_active.svg "; done
    for x in `seq $inactive`; do echo -n "img/star_inactive.svg "; done
}

for x in `seq 1 5`
do
    convert -background None +append `tilenames $x` -resize x16 site/img/stars-$x.png
done
