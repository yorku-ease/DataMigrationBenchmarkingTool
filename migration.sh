#!/bin/bash

#echo "what's the file's path ? (include the file name)"

#read filename


#echo "What's the limit ?"

#read limit

#echo "are you doing compression ? (yes/no)"

#read compressionResponse

#echo "How many times would like to repeat the transfer ?"
#read numberOfTransfers

#filesize=$(ls -lh ${filename} | awk '{print $5}')
#echo "the size of the file is "$filesize

#if [[ "$compressionResponse" == "yes" ]]; then
#    echo "1. gzip"
#    echo "2. lz4"
#    read compressionTypeResponse
#    if [[ "$compressionTypeResponse" == "1" ]]; then
#         compressionType="gzip"
 #   else
 #        compressionType="lz4"
#    fi
#fi


function transferfile()
{
    filename=$1
    limit=$2
    compressionResponse=$3
    compressionType=$4
#clear RAM Cache as well as Swap Space at local machine
echo $USERPASSWORD | ./clearcache.sh

echo "on local machine" 
#clear RAM Cache as well as Swap Space at remote machine

echo $REMOTE1PASSWORD | ssh remote1 './clearcache.sh'

echo "on remote machine" 
if [[ "$compressionResponse" == "yes" ]]; then
    outputfilename="output-file.${filename}.${limit}.${compressionType}"
    tempoutputfilename="temp."$outputfilename
    
    cat ${filename} | pv -fL $limit  2>> $tempoutputfilename | $compressionType | ssh remote1 "cat > /home/casuser/test/${filename}.${limit}.${compressionType}" > /dev/null 2>&1
else
    outputfilename="output-file.${filename}.${limit}"
    tempoutputfilename="temp."$outputfilename

    cat ${filename} | pv -fL $limit  2>> $tempoutputfilename | ssh remote1 "cat > /home/casuser/${filename}.${limit}" > /dev/null 2>&1
fi


tr '\r' '\n' < $tempoutputfilename  >> temp

#remove the last line because it's empty then we take the last line and trim it to remove spaces.
sed '$d' temp | tail -1 | awk '{$1=$1};1'> temp1

runningtime=$(cut -d' ' -f2 temp1)

}


function calculateAveragePerTransfer()
{
numberOfTransfers=$1
filename=$2
limit=$3
compressionResponse=$4
compressionType=$5

i=1
averagetime=0
while [ $i -le $numberOfTransfers ]; 
do 
transferfile $filename $limit $compressionResponse $compressionType
echo "transfer :" $i >> $outputfilename

seconds=$(echo $runningtime | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')

echo "total time for transfer " $i ":" $seconds >> $outputfilename

currenttime=$(printf '%.3f\n' $(echo "scale=3;$seconds / $numberOfTransfers" | bc -l))
averagetime=$(printf '%.3f\n' $(echo "scale=3;$averagetime + $currenttime" | bc -l))
((i++))
echo "current averageTime: " $averagetime "seconds">> $outputfilename ;

done

filesize=$(ls -lh ${filename} | awk '{print $5}')

echo "Final averageTime: " $averagetime "seconds for a file of size " $filesize >> $outputfilename 

rm $tempoutputfilename
rm temp
rm temp1
}

#only for testing
numberOfTransfers=1

#files=(customer.ddl DS_001.csv DS_002.csv customer.csv )
#limits=( 1g 500m 50m 5m)
#compressionTypes=(None gzip lz4)

files=(data/test1.pdf )
limits=( 1024b)
compressionTypes=(gzip)

for p in "${files[@]}"
do
	for j in "${limits[@]}"
    do
        for k in "${compressionTypes[@]}"
        do
        gfilename=$p
        glimit=$j
        gcompressionType=$k
        if [ "$k" = None ]
        then
          gcompressionResponse=no
        else
          gcompressionResponse=yes
        fi
        echo $filename " " $glimit " " $gcompressionResponse " " $gcompressionType
        calculateAveragePerTransfer $numberOfTransfers $gfilename $glimit $gcompressionResponse $gcompressionType
        sleep 5m
        done

    done

done

#calculateAveragePerTransfer $gcompressionResponse $gfilename $glimit $gnumberOfTransfers