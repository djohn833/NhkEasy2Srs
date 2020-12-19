#!/bin/bash

echo Get links...
ts-node NhkEasyScrape.ts >> links.txt

echo Turning links into cards...
rm cards.tsv
for x in $(sort -u links.txt)
do
  echo "$x"
  python3 NhkEasy2Srs.py "$x"
done
