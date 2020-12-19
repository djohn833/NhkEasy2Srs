#!/bin/bash

# echo Get links...
# ts-node NhkEasyScrape.ts | tee links.txt

echo Turning links into cards...
rm cards.tsv
for x in $(cat links.txt)
do
  echo "$x"
  python3 NhkEasy2Srs.py "$x"
done
