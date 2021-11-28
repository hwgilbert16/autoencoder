# detect when drive is input
# find output dir from env file
# use handbrake cli to begin encoding all chapters

import ctypes
import os
import subprocess
import time
import wmi
import sys

c = wmi.WMI()

command = sys.argv[0]
outputDir = sys.argv[1]
handbrakePath = os.path.join(sys.argv[2])
sys.argv = sys.argv[3:]

for cdrom in c.Win32_CDROMDrive():
    status = cdrom.MediaLoaded
    drive = cdrom.Drive

checkForFile = os.path.join(drive)
testForFile = os.path.exists(checkForFile)

while testForFile == False:
    print("Waiting for drive to be inserted")
    time.sleep(10)
    testForFile = os.path.exists(checkForFile)

print("Drive has been inserted")

args = [handbrakePath, "-i", drive, "-o", outputDir]

while len(sys.argv) > 0:
    args.append(sys.argv[0])
    sys.argv.pop(0)

subprocess.call(args)

ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)

os.execv(sys.argv[0], sys.argv)