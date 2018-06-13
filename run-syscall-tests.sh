#!/bin/bash
# Project Group 1 (A2)
# File Name: run-syscall-tests.sh
# Purpose: to run the system call test script a set number of times (for data gathering purposes)
# Script was inspired by data gathering script from previous course (CS410: Intro to Performance)

# Inspired by data gathering script written in a previous course
# Required Looping Variables
COUNT=1
MAX=31

# Output file
# Allows user to specify the path of the output file by passing it in as a paremeter
OUTFILE=$1

while [ $COUNT -lt $MAX ]; do
	# Run Test
	echo Run $COUNT:>> $OUTFILE
	python syscalls.py >> $OUTFILE
	echo  >> $OUTFILE

	# Increment test count
	let COUNT=COUNT+1
done
