# This is a sample Python script.
import argparse
import sys
from xmlrpc.client import boolean

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import subprocess
import os

from pandas.io.formats.format import return_docstring

import Googledriveparser
import Prefetchparser
import os
import Onedriveparser
import registryparser
from Amcacheparser import amchacheParsing
from Jumplistparser import jumplistParsing

parser = argparse.ArgumentParser(description="Program, ktorý spracováva dve absolútne cesty.")
parser.add_argument("kape_path", type=str, help="Cesta k exe súboru kapu.")
parser.add_argument("target_path", type=str, help="Cesta k cieľovému priečinku.")
parser.add_argument("result_path", type=str, help="Cesta k výsledkovému priečinku.")
args = parser.parse_args()

# Overenie, či kape_path je existujúci exe súbor
if not (os.path.isfile(args.kape_path) and args.kape_path.lower().endswith(".exe")):
    print("Chyba: Očakáva sa cesta k existujúcemu exe súboru KAPE.")
    sys.exit(1)

# Overenie, či target_path a result_path sú existujúce priečinky
if not (os.path.isdir(args.target_path) and os.path.isdir(args.result_path)):
    print("Chyba: target_path alebo result_path nie je platný priečinok.")
    sys.exit(1)

kape_path = args.kape_path
target_path=args.target_path
result_path=args.result_path
#hodnoty ktore urcuju ci sa nachadza aplikacia v zariadeni
current_directory = os.getcwd()#cesta k projektu
if not os.path.exists(os.path.join(current_directory, "exPrefetch")):
    os.makedirs(os.path.join(current_directory, "exPrefetch"))
exPrefetch=os.path.join(current_directory,"exPrefetch")
if not os.path.exists(os.path.join(result_path, "parsPrefetch")):
    os.makedirs(os.path.join(result_path, "parsPrefetch"))
parsPrefetch=os.path.join(result_path, "parsPrefetch")
#vytorenie priecinkou pre vysledky kapu


cmd = [kape_path, "--tsource", target_path, "--tdest",exPrefetch,"--tflush", "--target", "Prefetch"]
subprocess.run(cmd)
cmd1 = [kape_path, "--msource", exPrefetch, "--mdest",parsPrefetch,"--tflush", "--module", "PECmd"]
subprocess.run(cmd1)
#volanie kapu na prefetch subory
ONEDRIVE,GOOGLEDRIVE,DROPBOX= Prefetchparser.isthere(result_path)#zapiseme ci sa nachadzaju dane apky z metody
if(ONEDRIVE or GOOGLEDRIVE or DROPBOX==True): #ak sa nachadza nejaka cloudova apka analyzujeme dalej jumplisty a amcache
    if not os.path.exists(os.path.join(current_directory, "exJumplists")):
        os.makedirs(os.path.join(current_directory, "exJumplists"))
    exJumplists=os.path.join(current_directory, "exJumplists")
    if not os.path.exists(os.path.join(result_path, "parsJumplists")):
        os.makedirs(os.path.join(result_path, "parsJumplists"))
    parsJumplists=os.path.join(result_path, "parsJumplists")

    if not os.path.exists(os.path.join(current_directory, "exAmcache")):
        os.makedirs(os.path.join(current_directory, "exAmcache"))
    exAmcache=os.path.join(current_directory, "exAmcache")
    if not os.path.exists(os.path.join(result_path, "parsAmcache")):
        os.makedirs(os.path.join(result_path, "parsAmcache"))
    parsAmcache=os.path.join(result_path, "parsAmcache")
    if not os.path.exists(os.path.join(current_directory, "exRegistry")):
        os.makedirs(os.path.join(current_directory, "exRegistry"))
    exRegistry=os.path.join(current_directory, "exRegistry")


    cmd = [kape_path, "--tsource",target_path, "--tdest", exJumplists, "--tflush",
           "--target", "LNKFilesAndJumpLists"]
    subprocess.run(cmd)
    cmd1 = [kape_path, "--msource", exJumplists, "--mdest", parsJumplists, "--tflush",
            "--module", "JLECmd"]
    subprocess.run(cmd1)
    jumplistParsing(result_path)

    cmd = [kape_path, "--tsource", target_path, "--tdest",exAmcache, "--tflush",
           "--target", "Amcache"]
    subprocess.run(cmd)
    cmd1 = [kape_path, "--msource",exAmcache, "--mdest",parsAmcache, "--tflush",
           "--module", "AmcacheParser"]
    subprocess.run(cmd1)
    amchacheParsing(result_path)
    cmd = [kape_path, "--tsource", target_path, "--tdest", exRegistry, "--tflush",
           "--target", "RegistryHivesUser"]
    subprocess.run(cmd)
    registryparser.function(result_path)


    if ONEDRIVE==True:#ak sa nachadza onedrive analyzujeme jeho metadata
        file = os.path.join(result_path, "registry.csv")
        df = pd.read_csv(file)
        print(df.columns)
        vysledok = os.path.join(result_path, "vysledok.txt")
        df = df[df['Key Path'].str.contains(r'OneDrive', na=False, case=False)]
        with open(vysledok, "a", encoding="utf-8") as file1:
            if df.loc[df['Value Name'] == 'FirstRunSignInOrigin', 'Value Data'].empty:
                file1.write("ONEDRIVE NEBOL PREPOJENY NA ZARIADENI \n")
                freeversion = 0
            else:
                if df.loc[df['Value Name'] == 'OneDriveDeviceId', 'Value Data'].empty:
                    freeversion = 1
                else:
                    freeversion = 2
        if freeversion==1:
            if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
                os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
            onedriveMetadata=os.path.join(current_directory, "onedriveMetadata")
            cmd = [kape_path, "--tsource", target_path, "--tdest", onedriveMetadata,
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
            subprocess.run(cmd)
            Onedriveparser.parsing(freeversion, result_path)
        if freeversion==2:
            if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
                os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
            onedriveMetadata = os.path.join(current_directory, "onedriveMetadata")
            cmd = [kape_path, "--tsource", target_path, "--tdest", onedriveMetadata,
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
            Onedriveparser.parsing(freeversion,result_path)
            subprocess.run(cmd)



    if GOOGLEDRIVE==True:#ak sa nachadza googledrive analyzujeme jeho metadata
        if not os.path.exists(os.path.join(current_directory, "googledriveMetadata")):
            os.makedirs(os.path.join(current_directory, "googledriveMetadata"))
        googledriveMetadata=os.path.join(current_directory, "googledriveMetadata")
        cmd = [kape_path, "--tsource",target_path, "--tdest", googledriveMetadata, "--tflush",
               "--target", "GoogleDrive_Metadata"]
        subprocess.run(cmd)
        Googledriveparser.parsing(result_path)


    if DROPBOX==True:#ak sa nachadza dropbox analyzujeme jeho metadata
        if not os.path.exists(os.path.join(current_directory, "dropboxMetadata")):
            os.makedirs(os.path.join(current_directory, "dropboxMetadata"))
        dropboxMetadata=os.path.join(current_directory, "dropboxMetadata")
        cmd = [kape_path, "--tsource",target_path, "--tdest", dropboxMetadata, "--tflush",
               "--target", "Dropbox_Metadata"]
        subprocess.run(cmd)









# See PyCharm help at https://www.jetbrains.com/help/pycharm/
