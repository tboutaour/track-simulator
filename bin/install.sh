#!/bin/bash
TRACKSIMULATORPATH=${HOME}/track-simulator/
CONFIGPATH=${TRACKSIMULATORPATH}/config
DBPATH=${TRACKSIMULATORPATH}/db
ANALYSISPATH=${TRACKSIMULATORPATH}/analysis
SIMULATIONPATH=${TRACKSIMULATORPATH}/simulation

# Make directories if do not exist.
mkdir -p ${DBPATH}
mkdir -p ${ANALYSISPATH}
mkdir -p ${ANALYSISPATH}/statistics
mkdir -p ${}

# Download docker-compose file from github.
wget https://raw.githubusercontent.com/tboutaour/track-simulator/master/bin/install.sh -P ${CONFIGPATH}