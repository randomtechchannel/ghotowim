import subprocess
import os
import linecache
vhddir = input("Enter dir of VHD: ")
vhddir = vhddir[0] + ":\\"
dirfile = open('vhddir.txt', 'w') 
dirfile.write(vhddir)
dirfile.close()
ghostdir = input("Enter dir of ghost file: ")
diskfile = open("disk.txt", "w")
if os.path.exists(vhddir + "disk.vhd"):
  diskfile1 = open("disk.bat", "w+")
  diskfile1.write("python vhdmount.py -unmount -source " + vhddir + "disk.vhd")
  diskfile1.close()
  subprocess.check_output(["disk.bat"])
  os.remove(vhddir + "disk.vhd")
  diskfile.write("select vdisk file=" + "\"" + vhddir + "disk.vhd" +"\"" + "\n" + "attach vdisk\n" "convert mbr")
else:
  diskfile.write("create vdisk file=" + "\"" + vhddir + "disk.vhd" +"\"" + " maximum=102400 type=expandable\n" + "select vdisk file=" + "\"" + vhddir + "disk.vhd" +"\"" + "\n" + "attach vdisk\n" "convert mbr")

diskfile.close() 
subprocess.check_output(["C:\\Windows\\System32\\diskpart.exe", "/s", "disk.txt"])
output = open('shell_output.txt', 'w+') 
subprocess.run('powershell disk', shell=True, stdout=output) 
output.close() 
file1 = open('shell_output.txt', 'r')
Lines = file1.readlines()
diskindex =0  
count = 0
for line in Lines:
    count += 1
    if "Msft" in line.strip():
    	diskindex = int(line.strip()[0]) + 1
      

ghost = "-clone,mode=load,src=" + str(ghostdir) + ",dst=" + str(diskindex) + " -sure"
subprocess.run(["ghost.exe", ghost])
output2 = open('shell_output2.txt', 'w+') 
subprocess.run('powershell Get-Partition -DiskNumber ' + str(diskindex -1), shell=True, stdout=output2) 
output2.close() 
windir = linecache.getline(r"shell_output2.txt", 7)[17]
wimdir = input("Enter dir of install.wim file: ")
if (wimdir[len(wimdir) -1] != '\\'):
    wimdir += "\\"
diskfile = open("dism1.bat", "w")
dism = "dism /Capture-Image" + " /ImageFile:" + "\"" +  wimdir + "" + "install.wim" + "\"" + " /CaptureDir:" + windir + ":"+ " /Name:" + "\"" + "Windows 10 Pro" + "\""
diskfile.write("@echo off \n" + dism)
diskfile.close()
subprocess.run(["dism1.bat"])
dirstr = vhddir + "disk.vhd"
diskfile = open("disk.bat", "w+")
diskfile.write("python vhdmount.py -unmount -source " + dirstr)
diskfile.close()
subprocess.check_output(["disk.bat"])
if os.path.exists(dirstr):
  os.remove(dirstr)
