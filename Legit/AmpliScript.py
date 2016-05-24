# Author: Jared Knott
# This script automates the testing process required for testing the Amplistor
# Storage software. It will generate the required files and folders for the
# specified test cases.
# This script calls Paul Dunn's dss-test.sh script to instantiate several
# encoding loads. This information can be compiled for performance analysis.

# Things to automate:
# Creating folder for saving results
# Asking for SB and Stream Counts
# Gather up system information and configuration
#   mem usage, cpu usage, mem speed, cpu speed, swap used
# Calling the monitor function
# Calling Paul's function
# adding iostat and netstat to monitor function
# create summary of performance
# formatting results and presenting results

# Args: SB (-SBmi) min and (-SBma) max
# Stream count (-Cmi) min and (-Cma) max

import sys
import os
import datetime
import subprocess
import re
import time
import pprint
import multiprocessing as mp
import psutil

# add system arguments

minSB = 8
maxSB = 64
minStream = 8
maxStream = 32
sb_size = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# get
curDir = os.getcwd()

# constructors
now = datetime.datetime.now()

# create dictionaries
cpuInfoParsed = {}
memInfoParsed = {}


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return process


def subprocess_cmd_ret_list(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip().split()
    return proc_stdout

def subprocess_cmd_call(command):
    process = subprocess.check_output(command)
    return process


def check_cpu_usage():
    return subprocess_cmd("mpstat | grep all |awk {'print $4'}")


def check_power_usage():
    try:
        return subprocess_cmd("ipmitool power status")
    except:
        return "power unavailable"

# try to read user input, and use defaults if none
print("select a value within available size:",)
for i in sb_size:
    print (i,)
print("")

try:
    minSB = int(input("min Super Block size? (default: %sMB) " % minSB))
    if minSB in sb_size:
        minSB = minSB
    else:
        minSB = 8
        print ("value not in range, using default")
except:
    print("using default")

try:
    maxSB = int(input("max Super Block size? (default: %sMB) " % maxSB))
    if maxSB < minSB:
        print("maxSB too small, doing single SB size")
        maxSB = minSB
    if maxSB in sb_size:
        maxSB = maxSB
    else:
        maxSB = 64
        print ("value not in range, using default")
except:
    print("using default")

print ("select an integer value from 1 to 100 (can go higher, but expect to wait)")

try:
    minStream = int(input("min Stream count? (default: %s) " % minStream))
except:
    print("using default")

try:
    maxStream = int(input("max Stream count? (default: %s) " % maxStream))
    if maxStream < minStream:
        print("maxSB too small, doing single SB size")
        maxStream = minStream
except:
    print("using default")


# make folder structure in current directory
folderName = str(input("folder name for results: "))    # must be raw_input for python 2.7
if folderName == "":
    print("using date and time")
    folderName = "blank"

if folderName == "blank":
    print("creating directory for results in %s..." % curDir)
    try:
        os.mkdir("PerfRes-%s" % now.strftime("%Y-%m-%d_%H-%M"))
        putDir = "PerfRes-%s" % now.strftime("%Y-%m-%d_%H-%M")
        print("done, directory is: %s" % putDir)
    except:
        print("directory already exists, please delete it")
        sys.exit()
else:
    print("creating directory for results in %s..." % curDir)
    try:
        os.mkdir("PerfRes-%s" % folderName)
        putDir = "PerfRes-%s" % folderName
        print("done, directory is: %s" % putDir)
    except:
        print("directory already exists, please delete it")
        sys.exit()

# create files
summaryFile = open("%s/%s/summary.txt" % (curDir, putDir), 'w')
summaryFile.write('Created by AmpliScript.py, author: Jared Knott (jared.knott@hgst.com) \n')

# ###look into using substring to get the infos### #

# get mem info
memInfo = str(subprocess_cmd('cat /proc/meminfo')).replace(" ", "")    # must be root in linux
memInfoList = re.split('\\\\n|:| ', memInfo)

i = 0
for word in memInfoList:
    if word == "MemTotal" or word == "MemFree" or word == "SwapFree":
        memInfoParsed[word] = memInfoList[i + 1]
    i += 1

# get mem clock info
memClkInfo = str(subprocess_cmd('dmidecode --t memory')).replace(" ", "")     # must be root in linux
memClkList = re.split('\\\\t|\\\\n|:| ', memClkInfo)

j = 0
for word in memClkList:
    if word == "ConfiguredClockSpeed" or word == "Manufacturer" or word == "NumberOfDevices"\
            or word == "MaximumCapacity":
        if memClkList[j + 1] != "Unknown":
            memInfoParsed[word] = memClkList[j + 1]
    j += 1

# get cpu info
cpuInfo = str(subprocess_cmd('dmidecode -t processor')).replace(" ", "")
cpuInfoList = re.split('\\\\t|\\\\n|:', cpuInfo)

i = 0
for word in cpuInfoList:
    if word == "CoreCount" or word == "ThreadCount" or word == "CurrentSpeed"\
            or word == "CoreEnabled" or word == "Version":
        if cpuInfoList[i + 1] != "Unknown":
            cpuInfoParsed[word] = cpuInfoList[i + 1]
    i += 1

# write system info to file
#summaryFile.write("Processor: %s - CPU Clock: %s - Mem Vendor: %s - DIMM Count: %s - Mem Capacity: %s - Mem Speed: %s\n"
#                  % (cpuInfoParsed['Version'], cpuInfoParsed['CurrentSpeed'], memInfoParsed['Manufacturer'],
#                     memInfoParsed['NumberOfDevices'], memInfoParsed['MaximumCapacity'],
#                     memInfoParsed['ConfiguredClockSpeed']))


print("starting main testing with %s workers in..." % mp.cpu_count())
for t in range(3, 0, -1):
    print (" %s " % t)
    time.sleep(1)

summaryFile.write("streams,Block Size")
streamsBySB = [[" " for m in range(0, maxStream-minStream+1)] for g in range((sb_size.index(maxSB)-sb_size.index(minSB)*3)+1)]

cpuBind = 0
g = 0
for sb in sb_size[sb_size.index(minSB):sb_size.index(maxSB)+1]:
    actualSB = sb*1024*1024
    print('block size (MB/s): %s' % sb)
    m = 0
    for stream in range(minStream, maxStream+1):
        procs = []
        checked = False
        sumOfThruput = 0.0
        callList = []
        print('streams: %s' % stream)
        for num in range(0, stream):
            if cpuBind == mp.cpu_count() - 1:
                cpuBind = 0
            else:
                cpuBind += 1
            # p = subprocess.Popen(['./hello.sh'], stdout=subprocess.PIPE, shell=True)  # use this for testing
            # p = subprocess.Popen(['/opt/qbase3/bin/dss --encoder-perf-test %s --spread-width 18\
            # --safety 5 --test-repeat 1 &' % actualSB], stdout=subprocess.PIPE, shell=True)   # use this normally
            callList.append(['taskset', '-c', '%s' % cpuBind, '/opt/qbase3/bin/dss', '--encoder-perf-test', '%s'\
                            % actualSB, '--spread-width', '18', '--safety', '5', '--test-repeat', '1'])
        p = mp.Pool(16)
        results = p.map(subprocess_cmd_call, callList)
        cpuUse = psutil.cpu_percent(percpu=True)
        p.close()
        p.join()
        for lines in results:
            line = str(lines, "utf-8").strip("\n")
            print (line)
            thruput = line.split()
            sumOfThruput += float(thruput[16])
        print('total throughput: %s' % round(sumOfThruput, 4), "total cpu usage: ", cpuUse)
#        print(g, m)
#        streamsBySB[g + 1][m] = round(sumOfThruput, 2)
#        streamsBySB[g + 1][m * 3] = check_power_usage()
# close files
summaryFile.close()
print ("closed")
