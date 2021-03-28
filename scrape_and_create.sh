#!/bin/bash

echo Get links...
ts-node NhkEasyScrape.ts > links.txt
sort -u links.txt -o links.txt

echo Turning links into cards...
rm cards.tsv
for x in $(cat links.txt)
do
  echo "$x"
  python3 NhkEasy2Srs.py "$x"
done
