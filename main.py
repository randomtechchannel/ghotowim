import subprocess
import os
import linecache
import tkinter
import customtkinter
import threading
import ctypes
from tkinter import filedialog
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("720x480")
app.title("GhoToWIM")
vhddir = ""
wimdir = ""
ghostdir = ""
def start():
  threading.Thread(target=run).start()
def choosevhd():
  vhddir = filedialog.askdirectory()
  vhdbrowse2.configure(text=vhddir)
def choosewim():
  wimdir = filedialog.asksaveasfilename(filetypes=[('Windows Imaging Format (*.wim)', '*.wim')], defaultextension='.wim',initialfile = "install")
  wimbrowse2.configure(text=wimdir)  
def choosegho():
  ghostdir = filedialog.askopenfilename(filetypes=[('Norton Ghost (*.gho)', '*.gho')], defaultextension='.gho')
  ghobrowse2.configure(text=ghostdir) 
def run():
  vhddir= vhdbrowse2.cget("text")
  vhddir = vhddir.replace("/", "\\")
  vhddir = vhddir +"\\"
  temp.configure(text="See the progress when running in the command window!")
  title.configure(text="Preparing")
  diskfile = open("disk.txt", "w+")
  if os.path.exists(vhddir + "disk.vhd"):
    diskfile1 = open("disk.bat", "w+")
    diskfile1.write("python vhdmount.py -unmount -source " + vhddir + "disk.vhd")
    diskfile1.close()
    subprocess.check_output(["disk.bat"])
    os.remove(vhddir + "disk.vhd")
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
  progressBar.set(0.15)
  title.configure(text="Ghosting to VHD (Click to Yes and when successfully click to Continue)")
  ghostdir= ghobrowse2.cget("text")
  ghost = "-clone,mode=load,src=" + str(ghostdir) + ",dst=" + str(diskindex) + " -sure"
  subprocess.check_output(["ghost.exe", ghost])
  progressBar.set(0.45)
  title.configure(text="Checking the Windows Version in the ghost file")
  output2 = open('shell_output2.txt', 'w+') 
  subprocess.run('powershell Get-Partition -DiskNumber ' + str(diskindex -1), shell=True, stdout=output2) 
  output2.close()
  windir = linecache.getline(r"shell_output2.txt", 7)[17]
  wimdir= wimbrowse2.cget("text")
  wimdir = wimdir.replace("/", "\\")
  subprocess.check_output(["C:\\Windows\\System32\\reg.exe", "load", "HKLM\\SoftTemp", windir + ":\\Windows\\System32\\config\\software"])
  output3 = open('shellver.txt', 'w+') 
  subprocess.run(["C:\\Windows\\System32\\reg.exe", "query", "hklm\\softtemp\\microsoft\\windows nt\\currentversion", "/v", "ProductName"], shell=True, stdout=output3)
  subprocess.check_output(["C:\\Windows\\System32\\reg.exe", "unload", "HKLM\\SoftTemp"])
  output3.close()
  ver = linecache.getline(r"shellver.txt", 3)
  ver = ver[29:len(ver) -1]
  progressBar.set(0.60)
  title.configure(text="Making install.wim image")
  diskfile = open("dism1.bat", "w+")
  dism = "dism /Capture-Image" + " /ImageFile:" + "\"" +  wimdir + "\"" + " /CaptureDir:" + windir + ":"+ " /Name:" + "\"" + ver + "\""
  diskfile.write("@echo off\n" + dism)
  diskfile.close()
  subprocess.run(["dism1.bat"])
  dirstr = vhddir + "disk.vhd"
  diskfile = open("disk.bat", "w+")
  diskfile.write("python vhdmount.py -unmount -source " + dirstr)
  diskfile.close()
  subprocess.check_output(["disk.bat"])
  if os.path.exists(dirstr):
    os.remove(dirstr) 
  progressBar.set(1)
  title.configure(text="Sucessfully convert GHO file to WIM file")
  ctypes.windll.user32.MessageBoxW(0, "Sucessfully convert GHO file to WIM file", "GhoToWIM", 0)
  print("Sucessfully convert GHO file to WIM file")
ctypes.windll.user32.MessageBoxW(0, "Temporarily disable your antivirus to improve speed and decrease errors", "GhoToWIM", 0)
vhdbrowse = customtkinter.CTkButton(app, text="Choose where temp folder (VHD) save", command=choosevhd)
vhdbrowse.pack(padx=10, pady=10)
vhdbrowse2 = customtkinter.CTkLabel(app, text="")
vhdbrowse2.pack(padx=10, pady=10)
ghobrowse = customtkinter.CTkButton(app, text="Choose GHO file", command=choosegho)
ghobrowse.pack(padx=10, pady=10)
ghobrowse2 = customtkinter.CTkLabel(app, text="")
ghobrowse2.pack(padx=10, pady=10)
wimbrowse = customtkinter.CTkButton(app, text="Choose where install.wim save", command=choosewim)
wimbrowse.pack(padx=10, pady=10)
wimbrowse2 = customtkinter.CTkLabel(app, text="")
wimbrowse2.pack(padx=10, pady=10)
title = customtkinter.CTkLabel(app, text="")
title.pack(padx=10, pady=10)
progressBar = customtkinter.CTkProgressBar(app,width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)
wimbrowse = customtkinter.CTkButton(app, text="Start", command=start)
wimbrowse.pack(padx=10, pady=10)
temp = customtkinter.CTkLabel(app, text="Made with ♥ by Random Tech Channel")
temp.pack(padx=10, pady=10)
app.mainloop()






