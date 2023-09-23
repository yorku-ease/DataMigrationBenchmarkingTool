#!/bin/bash

sourcedatafilepath=$1
targetdatafilepath=$2

sourcedatafilepath="$sourcedatafilepath"
targetdatafilepath="$targetdatafilepath"


diff $sourcedatafilepath <(sshpass -p "RESEARCH1149project" ssh casuser@cas1149a1.fyre.ibm.com "cat $targetdatafilepath ")