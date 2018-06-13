#!/bin/bash
# Project Group 1 (A2)
# File Name: parse-data.sh
# Purpose: processes output from the run-syscall-tests bash script (which runs the python-based system call testing script a given number of times and outputs results to a file)

# Name of input file (containing the initial data) and output (contianing the filtered version of the data)
# $1 and $2 are strings recieved at the command line, so the user of the script can specify the input/output files of the command
INPUTFILEPATH=$1
OUTPUTFILENAME=$2

# System call name array (must match name printed on output of script)
# https://stackoverflow.com/questions/8880603/loop-through-an-array-of-strings-in-bash
SYSCALLS=(
    "fork"
    "kill" 
    "brk"
    "mmap"
    "munmap"
    "open"
    "close"
    "read"
    "write"
    "ioctl_random"
    "ioctl_tty"
    "getitimer"
    "read_urandom"
    "write_null"
    "getrusage"
    "stat"
    "statfs"
    "time"
    "clock_gettime"
    "gettimeofday_timed"
    "gettimeofday_two_direct_calls_with_nothing_in_between"
    "getpid"
    "getuid"
    "setuid"
    "getifaddrs"
    "create_socket"
    "connect"
    "send"
    "receive"
    "close_socket"
    )

# https://stackoverflow.com/questions/8880603/loop-through-an-array-of-strings-in-bash
# This part ended up getting a little bit out of hand, but it works (at least it should)!
for i in "${SYSCALLS[@]}"
do
    echo "$i" >> $OUTPUTFILENAME
    if [ "$i" == "close" ]; then
        (cat $INPUTFILEPATH | grep "$i" | grep -Eiv "socket" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    elif [ "$i" == "time" ]; then
        (cat $INPUTFILEPATH | grep "$i" | grep -Eiv "get" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    elif [ "$i" == "stat" ]; then
       (cat $INPUTFILEPATH | grep "$i" | grep -Eiv "fs" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    elif [ "$i" == "write" ]; then
       (cat $INPUTFILEPATH | grep "$i" | grep -Eiv "null" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    elif [ "$i" == "read" ]; then
       (cat $INPUTFILEPATH | grep "$i" | grep -Eiv "random" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    else
        (cat $INPUTFILEPATH | grep "$i" | grep -Eo "([-]?[0-9]+)|([0-9]+\.[0-9]+)") >> $OUTPUTFILENAME
    fi
    echo  >> $OUTPUTFILENAME
done

# Arrays and looping through them (this link was already mentioned)
# https://stackoverflow.com/questions/8880603/loop-through-an-array-of-strings-in-bash

# Regex
# Helped somewhat: https://stackoverflow.com/questions/35919103/how-do-i-use-a-regex-in-a-shell-script
# https://stackoverflow.com/questions/15814592/how-do-i-include-negative-decimal-numbers-in-this-regular-expression
# https://stackoverflow.com/questions/28399346/how-can-i-match-zero-or-more-instances-of-a-pattern-in-bash
# I didn't use this one, but I saw it so I decided to add it just in case: https://stackoverflow.com/questions/8402919/how-to-make-grep-select-only-numeric-values

# If-else statements in bash
# https://stackoverflow.com/questions/4277665/how-do-i-compare-two-string-variables-in-an-if-statement-in-bash
# https://stackoverflow.com/questions/16034749/if-elif-else-statement-issues-in-bash
