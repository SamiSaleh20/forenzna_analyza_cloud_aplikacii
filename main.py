# This is a sample Python script.
from xmlrpc.client import boolean

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import subprocess
import os

import prefetch

#hodnoty ktore urcuju ci sa nachadza aplikacia v zariadeni
current_directory = os.getcwd()#cesta k projektu
if not os.path.exists(os.path.join(current_directory, "exPrefetch")):
    os.makedirs(os.path.join(current_directory, "exPrefetch"))
if not os.path.exists(os.path.join(current_directory, "parsPrefetch")):
    os.makedirs(os.path.join(current_directory, "parsPrefetch"))
#vytorenie priecinkou pre vysledky kapu

kape_path = r"C:\Users\sami\OneDrive - UPJŠ\Pracovná plocha\kape\KAPE\kape.exe"
cmd = [kape_path, "--tsource", r"C:", "--tdest",os.path.join(current_directory, "exPrefetch"),"--tflush", "--target", "Prefetch", "--gui"]
subprocess.run(cmd)
cmd1 = [kape_path, "--msource", os.path.join(current_directory, "exPrefetch"), "--mdest",os.path.join(current_directory, "parsPrefetch"),"--tflush", "--module", "PECmd", "--gui"]
subprocess.run(cmd1)
#volanie kapu na prefetch subory
ONEDRIVE,GOOGLEDRIVE,DROPBOX=prefetch.isthere()#zapiseme ci sa nachadzaju dane apky z metody
if(ONEDRIVE or GOOGLEDRIVE or DROPBOX==True): #ak sa nachadza nejaka cloudova apka analyzujeme dalej jumplisty a amcache
    if not os.path.exists(os.path.join(current_directory, "exJumplists")):
        os.makedirs(os.path.join(current_directory, "exJumplists"))
    if not os.path.exists(os.path.join(current_directory, "parsJumplists")):
        os.makedirs(os.path.join(current_directory, "parsJumplists"))
    if not os.path.exists(os.path.join(current_directory, "parsAmcache")):
        os.makedirs(os.path.join(current_directory, "parsAmcache"))
    cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "exJumplists"), "--tflush",
           "--target", "LNKFilesAndJumpLists", "--gui"]
    subprocess.run(cmd)
    cmd1 = [kape_path, "--msource", os.path.join(current_directory, "exJumplists"), "--mdest", os.path.join(current_directory, "parsJumplists"), "--tflush",
            "--module", "JLECmd", "--gui"]
    subprocess.run(cmd1)
    cmd = [kape_path, "--msource", r"C:\Windows\AppCompat\Programs", "--mdest", os.path.join(current_directory, "parsAmcache"), "--tflush",
           "--module", "AmcacheParser", "--gui"]
    subprocess.run(cmd)

    if ONEDRIVE==True:#ak sa nachadza onedrive analyzujeme jeho metadata
        if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
            os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
        cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "onedriveMetadata"), "--tflush",
               "--target", "OneDrive_Metadata", "--gui"]
        subprocess.run(cmd)


    if GOOGLEDRIVE==True:#ak sa nachadza googledrive analyzujeme jeho metadata
        if not os.path.exists(os.path.join(current_directory, "googledriveMetadata")):
            os.makedirs(os.path.join(current_directory, "googledriveMetadata"))
        cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "googledriveMetadata"), "--tflush",
               "--target", "GoogleDrive_Metadata", "--gui"]
        subprocess.run(cmd)


    if DROPBOX==True:#ak sa nachadza dropbox analyzujeme jeho metadata
        if not os.path.exists(os.path.join(current_directory, "dropboxMetadata")):
            os.makedirs(os.path.join(current_directory, "dropboxMetadata"))
        cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "dropboxMetadata"), "--tflush",
               "--target", "Dropbox_Metadata", "--gui"]
        subprocess.run(cmd)








# See PyCharm help at https://www.jetbrains.com/help/pycharm/
