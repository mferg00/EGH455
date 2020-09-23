#!/bin/bash

# arg 1: folder name (without trailing /), arg 2: image name in folder (no .png)
preprocess() 
{
    python3 create_bg_file.py ../neg
    python3 rescaler.py ../"$1/$2.png"
    python3 grayScaler.py ../"$1/$2resized.jpg"
}

# arg 1: folder name (without trailing /), arg 2: image name in folder (no .png)
createsamples() 
{
    echo "CREATE SAMPLES"
    mkdir -p "$1"/pos
    opencv_createsamples -img "$1/$2"resizedgray.jpg -bg bg.txt -info "$1"/pos/info.lst -pngoutput "$1"/pos -maxxangle 0.3 -maxyangle 0.3 -maxzangle 0.3 -bgcolor 150 -bgthresh 1 -num 200
    opencv_createsamples -info "$1"/pos/info.lst -num 200 -w 20 -h 20 -vec "$1"/positives.vec
}

# arg 1: folder name (without trailing /), arg 2: num stages (optional, default 3)
dotraining()
{   
    stages_var=$2
    stages=${stages_var:-3}

    echo "DO TRAINING"
    mkdir -p "$1"/stages
    rm -rf "$1"/stages/*
    opencv_traincascade -data "$1"/stages -vec "$1"/positives.vec -bg bg.txt -numPos 200 -numNeg 100 -numStages "$stages" -maxFalseAlarmRate 0.1 -w 20 -h 20
    cp "$1"/stages/cascade.xml ../"$1"-"$stages".xml
}

currdir="${PWD##*/}"

if [ "$currdir" != "scripts" ]; then 
    echo "not in scripts folder"
    exit 1
fi;

# NOTE: training gets exponentially slower the more stages you have
# 3 stages took a few seconds, but 15 stages took about 10-40 minutes for me 

# cwd = training/scripts
preprocess corrosive corrosive
preprocess dangerous MDG9
cd ../

# cwd = training
createsamples corrosive corrosive
createsamples dangerous MDG9
dotraining corrosive 3
dotraining dangerous 3
