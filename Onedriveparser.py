import os
import shutil

from parsers import dbparser
from pathlib import Path
import pandas as pd
import os
from datetime import datetime
import subprocess
import sys



#metoda ktora berie informacie z onedrive
def parsing(freeversion,result):

    current_directory = os.getcwd()
    extracted_data = os.path.join(current_directory, "onedriveMetadata")
    python_executable = sys.executable
    #vytvorime vo vysledku priecinok na spracovane data z onedrive
    onedriveMetadataparsed = os.path.join(result, "onedriveMetadataparsed")
    current_directory = os.getcwd()
    pathToParsed = os.path.join(result, "onedriveMetadataparsed")
    if os.path.exists(pathToParsed):
        shutil.rmtree(pathToParsed)
    os.makedirs(pathToParsed)
    directory = Path(os.path.join(current_directory, "onedriveMetadata"))
    #vytvorime priecinok pre syncEngineDatabase_db
    if not os.path.exists(os.path.join(pathToParsed, "syncEngineDatabase_db")):
        os.makedirs(os.path.join(pathToParsed, "syncEngineDatabase_db"))
    syncEngineDatabase_db_parsed = os.path.join(pathToParsed, "syncEngineDatabase_db")

    #ak je to onedrive verzia zdarma
    if freeversion==1:
        #najdeme databazu
        for file in directory.rglob("*Personal_SyncEngineDatabase.db"):
            syncendinedatabase = file
            print(file)
        #spracujeme ju do csv suboru
        dbparser(syncendinedatabase, syncEngineDatabase_db_parsed)
        #najdeme a zapiseme profileServiceResponse.txt do vysledku
        for file in directory.rglob("*-profileServiceResponse.txt"):
            print(file)
            shutil.copy(file, os.path.join(result, "onedriveMetadataparsed"))

    # ak je to platena verzia onedrive
    else:
        # najdeme databazu
        for file in directory.rglob("*Business1_SyncEngineDatabase.db"):
            syncendinedatabase = file
            print(file)
            # spracujeme ju do csv suboru
        dbparser(syncendinedatabase, syncEngineDatabase_db_parsed)

    vysledok=os.path.join(result,"vysledok.txt")

    #zapisujeme zakladne info o onedrive do vysledok.txt
    with open(vysledok, "a", encoding="utf-8") as file1:
        #zapise o aku verziu ide
        if freeversion==1:
            file1.write("FREE ONEDRIVE: \n")
        else:
            file1.write("ONEDRIVE FOR BUSSINESS: \n")


        # prefetch udaje
        file = os.path.join(result, "prefetch.csv")
        df = pd.read_csv(file)
        filtered_rows = df[df['ExecutableName'].astype(str).str.contains(r'ONEDRIVE', case=False)]
        onedrive_rows = filtered_rows[filtered_rows['ExecutableName'].str.upper() == 'ONEDRIVE.EXE']
        last_run_row = onedrive_rows.loc[onedrive_rows['LastRun'].idxmax()]
        first_run_row = onedrive_rows.loc[onedrive_rows['SourceCreated'].idxmin()]
        file1.write(f"INFORMACIE Z PREFETCH: \n")
        file1.write(f"Posledne zapnutie OneDrive: {last_run_row['LastRun']} \n")
        file1.write(f"Prve zapnutie OneDrive: {first_run_row['SourceCreated']}  \n")


        # amcache udaje
        file = os.path.join(result, "amcache.csv")
        df = pd.read_csv(file)
        file1.write(f"INFORMACIE Z AMCHACHE: \n")
        print("amcache collums=", df.columns)
        oneDriveexes = df[df['Name'].astype(str).str.contains(r'OneDrive.exe', case=False)]
        oneDriveFileLaunchers = df[df['Name'].astype(str).str.contains(r'OneDriveFileLauncher.exe', case=False)]
        oneDriveexe = oneDriveexes.loc[oneDriveexes['Version'].idxmax()]
        if not oneDriveFileLaunchers.empty:
            oneDriveFileLauncher = oneDriveFileLaunchers.loc[oneDriveFileLaunchers['Version'].idxmax()]
            print(oneDriveFileLauncher['FileKeyLastWriteTimestamp'])
            file1.write(f"Posledne otvorenie suboru z OneDrivu: {oneDriveFileLauncher['FileKeyLastWriteTimestamp']}")
        file1.write(f"Cesta k exe suboru: {oneDriveexe['FullPath']} \n")
        file1.write(f"Verzia OneDrive: {oneDriveexe['Version']} \n")


        # registry udaje
        file = os.path.join(result, "registry.csv")
        file1.write(f"INFORMACIE Z REGISTRY: \n")
        df = pd.read_csv(file)
        print(df.columns)
        df = df[df['Key Path'].str.contains(r'OneDrive', na=False, case=False)]
        mail = df.loc[df['Value Name'] == 'UserEmail', 'Value Data']
        last_update = df.loc[df['Value Name'] == 'LastUpdate', 'Value Data']
        cid=df.loc[df['Value Name'] == 'cid', 'Value Data']
        if freeversion==1:
            prve_prihlasenie = df.loc[df['Value Name'] == 'ClientFirstSignInTimestamp', 'Value Data']
        else:
            prve_prihlasenie = df.loc[df['Value Name'] == 'FirstRunSignInOriginDateTime', 'Value Data']

        if df.loc[df['Value Name'] == 'FirstRunSignInOrigin', 'Value Data'].empty:
            file1.write("ONEDRIVE NEBOL PREPOJENY NA ZARIADENI \n")
        else:
            if df.loc[df['Value Name'] == 'OneDriveDeviceId', 'Value Data'].empty:
                file1.write(f"cas poslednej aktualizacie:{datetime.utcfromtimestamp(int(last_update.iloc[0]))} \n ")
                file1.write("emailova adresa pouzivatela:" + mail.to_string(index=False) + "\n")
                file1.write(f"cas prveho prihlasenia:{datetime.utcfromtimestamp(int(prve_prihlasenie.iloc[0]))} \n")
                file1.write(f"specialne id pouzivatela je {cid} \n")
            else:
                file1.write(f"cas prveho prihlasenia:{datetime.utcfromtimestamp(int(prve_prihlasenie.iloc[0]))} \n")
                file1.write(f"cas poslednej aktualizacie:{datetime.utcfromtimestamp(int(last_update.iloc[0]))} \n")
                file1.write("emailova adresa pouzivatela:" + mail.to_string(index=False) + "\n")

        #zapis z databazovych tabuliek
        df = pd.read_csv(os.path.join(syncEngineDatabase_db_parsed, "od_ClientFile_Records.csv"))
        top_10 = df.nlargest(10, 'lastChange')
        file1.write(f"INFORMACIE ZO SYNCENGINEDATABASE: \n")
        file1.write(f"10 NAPOSLEDY UPRAVOVANYCH SUBOROV: \n")
        for index, hodnota in top_10.iterrows():
            file1.write(
                f"nazov:{hodnota['fileName']} cas stiahnutia na disk:{datetime.fromtimestamp(hodnota['diskCreationTime'])} cas posledneho spustenia na zariadeni:{datetime.fromtimestamp(hodnota['diskLastAccessTime'])} stav zdielania:{hodnota['sharedItem']} \n")
        df = pd.read_csv(os.path.join(syncEngineDatabase_db_parsed, "od_ClientFolder_Records.csv"))
        df = df[df['sharedItem'] == 1]
        df = df.nlargest(10, 'sharedItem')
        file1.write(f"10 ZDIELANYCH PRIECINKOV NA ONEDRIVE: \n")
        file1.write(f"{df['folderName'].to_string(index=False)} \n")
        df = pd.read_csv(os.path.join(syncEngineDatabase_db_parsed, "od_GraphMetadata_Records.csv"))
        unique_creator = df['createdBy'].unique()
        unique_modifier = df['modifiedBy'].unique()
        unique_combined = set(unique_creator).union(set(unique_modifier))
        file1.write(f"KTO VYTVORIL/MENIL SUBORY V UCTE: {', '.join(unique_combined)} \n")


    #premenovanie kluca pre logy na general.keystore
    if freeversion == 1:
        for filename in os.listdir(extracted_data):
            if "Personal_general.keystore" in filename:
                old_path = os.path.join(extracted_data, filename)
                new_path = os.path.join(extracted_data, "general.keystore")
                # Premenovanie súboru
                os.rename(old_path, new_path)
                print(f"Premenovaný: {filename} -> general.keystore")
    else:
        for filename in os.listdir(extracted_data):
            if "Business1_general.keystore" in filename:
                old_path = os.path.join(extracted_data, filename)
                new_path = os.path.join(extracted_data, "general.keystore")
                # Premenovanie súboru
                os.rename(old_path, new_path)
                print(f"Premenovaný: {filename} -> general.keystore")
                break
    #volanie kodu pre dekodovanie a vypis informacii z logov o onedrive
    cmd = [
        python_executable, "odl.py", "-o",
        os.path.join(onedriveMetadataparsed, "logs"), "-k",
        extracted_data
    ]

    subprocess.run(cmd)













