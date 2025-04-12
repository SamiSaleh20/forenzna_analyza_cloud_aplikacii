#hlavny subor ktory sa zapina
# importy
import argparse
import sys
import pandas as pd
import subprocess

import Dropboxparser
import Googledriveparser
import Prefetchparser
import os
import Onedriveparser
import registryparser
from Amcacheparser import amchacheParsing
from Jumplistparser import jumplistParsing

# cesty ktore treba na vstupe pre kod
parser = argparse.ArgumentParser(description="Program, ktorý spracováva dve absolútne cesty.")
parser.add_argument("kape_path", type=str, help="Cesta k exe súboru kapu.")
parser.add_argument("PECmd_path", type=str, help="Cesta k prefetch parseru.")
parser.add_argument("target_path", type=str, help="Cesta k cieľovému priečinku.")
parser.add_argument("result_path", type=str, help="Cesta k výsledkovému priečinku.")
args = parser.parse_args()

# overenie, ze kape_path a PECmd_path su cesty k exe subory
if not (os.path.isfile(args.kape_path) and args.kape_path.lower().endswith(".exe")):
    print("Chyba: Očakáva sa cesta k existujúcemu exe súboru KAPE.")
    sys.exit(1)
if not (os.path.isfile(args.PECmd_path) and args.kape_path.lower().endswith(".exe")):
    print("Chyba: Očakáva sa cesta k existujúcemu exe súboru PECmd.")
    sys.exit(1)

# overenie, ze target_path a result_path su cesty k priecinkom
if not (os.path.isdir(args.target_path) and os.path.isdir(args.result_path)):
    print("Chyba: target_path alebo result_path nie je platný priečinok.")
    sys.exit(1)

#hodime vstupy do premennych
kape_path = args.kape_path
target_path=args.target_path
result_path=args.result_path
PECmd_path=args.PECmd_path
current_directory = os.getcwd()#cesta k projektu
#vytvorenie priecinkou pre extrahovane prefetch subory a spracovane prefetch subory
if not os.path.exists(os.path.join(current_directory, "exPrefetch")):
    os.makedirs(os.path.join(current_directory, "exPrefetch"))
exPrefetch=os.path.join(current_directory,"exPrefetch")
if not os.path.exists(os.path.join(result_path, "parsPrefetch")):
    os.makedirs(os.path.join(result_path, "parsPrefetch"))
parsPrefetch=os.path.join(result_path, "parsPrefetch")
#vytorenie priecinkou pre vysledky kapu

#kape target pre extrakciu prefetchou a nasledne kod pre ich parsovanie
cmd = [kape_path, "--tsource", target_path, "--tdest",exPrefetch,"--tflush", "--target", "Prefetch"]
subprocess.run(cmd)
cmd1 = [PECmd_path, "-d", exPrefetch, "--csv",parsPrefetch]
subprocess.run(cmd1)
#volame metodu z prefetchparser aby sme zistili ci sa onedrive,googledrive a dropbox nachadzaju v nich
ONEDRIVE,GOOGLEDRIVE,DROPBOX= Prefetchparser.isthere(result_path)
#ak sa nachadza nejaka cloudova apka analyzujeme dalej jumplisty,amcache a registry
if(ONEDRIVE or GOOGLEDRIVE or DROPBOX==True):
    #vytvorenie priecinkou pre extrahovane a parsovane hodnoty pre jumplisty amcache a registry
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

    #volanie kapu pre extrahovanie a parsovanie
    cmd = [kape_path, "--tsource",target_path, "--tdest", exJumplists, "--tflush",
           "--target", "LNKFilesAndJumpLists"]
    subprocess.run(cmd)
    cmd1 = [kape_path, "--msource", exJumplists, "--mdest", parsJumplists, "--tflush",
            "--module", "JLECmd"]
    subprocess.run(cmd1)
    #metoda na vybranie informacii z jumplistov
    jumplistParsing(result_path)

    cmd = [kape_path, "--tsource", target_path, "--tdest",exAmcache, "--tflush",
           "--target", "Amcache"]
    subprocess.run(cmd)
    cmd1 = [kape_path, "--msource",exAmcache, "--mdest",parsAmcache, "--tflush",
           "--module", "AmcacheParser"]
    subprocess.run(cmd1)
    #metoda na vybranie informacii z amcache
    amchacheParsing(result_path)

    cmd = [kape_path, "--tsource", target_path, "--tdest", exRegistry, "--tflush",
           "--target", "RegistryHivesUser"]
    subprocess.run(cmd)
    #metoda na prevod registrov v dat formate na csv a zobranie informacii
    registryparser.function(result_path)

    # ak sa nachadza onedrive analyzujeme jeho metadata
    if ONEDRIVE==True:
        file = os.path.join(result_path, "registry.csv")
        df = pd.read_csv(file)
        print(df.columns)
        vysledok = os.path.join(result_path, "vysledok.txt")
        df = df[df['Key Path'].str.contains(r'OneDrive', na=False, case=False)]
        with open(vysledok, "a", encoding="utf-8") as file1:
            #ak nebol aktivovany onedrive  cize FirstRunSignInOrigin je prazdny zapiseme to do vysledku
            if df.loc[df['Value Name'] == 'FirstRunSignInOrigin', 'Value Data'].empty:
                file1.write("ONEDRIVE NEBOL PREPOJENY NA ZARIADENI \n")
                freeversion = 0
            else:
                #zistujeme ci ide o onedrive for bussines alebo verzia zadarmo podla OneDriveDeviceId ktory ma len platena verzia
                if df.loc[df['Value Name'] == 'OneDriveDeviceId', 'Value Data'].empty:
                    freeversion = 1
                else:
                    freeversion = 2
        #ak ide o verziu zadarmo
        if freeversion==1:
            #vytvorime priecinok na kape output
            if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
                os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
            onedriveMetadata=os.path.join(current_directory, "onedriveMetadata")
            #volame kape target
            cmd = [kape_path, "--tsource", target_path, "--tdest", onedriveMetadata,
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
            subprocess.run(cmd)
            #metoda ktora berie informacie z onedrive
            Onedriveparser.parsing(freeversion, result_path)
        #ak ide o platenu verziu
        if freeversion==2:
            # vytvorime priecinok na kape output
            if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
                os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
            onedriveMetadata = os.path.join(current_directory, "onedriveMetadata")
            # volame kape target
            cmd = [kape_path, "--tsource", target_path, "--tdest", onedriveMetadata,
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
            subprocess.run(cmd)
            # metoda ktora berie informacie z onedrive
            Onedriveparser.parsing(freeversion,result_path)


    # ak sa nachadza googledrive
    if GOOGLEDRIVE==True:
        #vytvorime priecinok pre kape output
        if not os.path.exists(os.path.join(current_directory, "googledriveMetadata")):
            os.makedirs(os.path.join(current_directory, "googledriveMetadata"))
        googledriveMetadata=os.path.join(current_directory, "googledriveMetadata")
        #volanie kape targetu
        cmd = [kape_path, "--tsource",target_path, "--tdest", googledriveMetadata, "--tflush",
               "--target", "GoogleDrive_Metadata"]
        subprocess.run(cmd)
        #vybranie dat o googledrive
        Googledriveparser.parsing(result_path)

    # ak sa nachadza dropbox
    if DROPBOX==True:
        # vytvorime priecinok pre kape output
        if not os.path.exists(os.path.join(current_directory, "dropboxMetadata")):
            os.makedirs(os.path.join(current_directory, "dropboxMetadata"))
        dropboxMetadata=os.path.join(current_directory, "dropboxMetadata")
        # volanie kape targetu
        cmd = [kape_path, "--tsource",target_path, "--tdest", dropboxMetadata, "--tflush",
               "--target", "Dropbox_Metadata"]
        subprocess.run(cmd)
        # vybranie dat o dropboxe
        Dropboxparser.parsing(result_path)










