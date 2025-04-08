import os
import subprocess

import pandas as pd
import Onedriveparser
import registryparser
kape_path = r"C:\Users\sami\OneDrive - UPJŠ\Pracovná plocha\kape\KAPE\kape.exe"
current_directory = os.getcwd()
if not os.path.exists(os.path.join(current_directory, "exRegistry")):
    os.makedirs(os.path.join(current_directory, "exRegistry"))
cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "exRegistry"), "--tflush",
           "--target", "RegistryHivesUser"]
subprocess.run(cmd)
registryparser.function()
file = os.path.join(current_directory, "registry.csv")
df = pd.read_csv(file)
print(df.columns)
df = df[df['Key Path'].str.contains(r'OneDrive', na=False, case=False)]
with open("vysledok.txt", "a", encoding="utf-8") as file1:
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
    cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "onedriveMetadata"),
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
    subprocess.run(cmd)
    Onedriveparser.parsing(1)
if freeversion==2:
    if not os.path.exists(os.path.join(current_directory, "onedriveMetadata")):
        os.makedirs(os.path.join(current_directory, "onedriveMetadata"))
    cmd = [kape_path, "--tsource", r"C:", "--tdest", os.path.join(current_directory, "onedriveMetadata"),
                   "--tflush",
                   "--target", "OneDrive_Metadata"]
    subprocess.run(cmd)
    Onedriveparser.parsing(2)




