import os
import shutil
from contextlib import nullcontext
from pathlib import Path

from parsers import dbparser
import pandas as pd
from datetime import datetime

#vybranie dat o dropboxe
def parsing(result):
    current_directory = os.getcwd()
    # vytvorenie priecinka pre data
    pathToParsed = os.path.join(result, "dropboxMetadataparsed")
    if os.path.exists(pathToParsed):
        shutil.rmtree(pathToParsed)
    os.makedirs(pathToParsed)
    directory = Path(os.path.join(current_directory,"dropboxMetadata"))
    if not os.path.exists(os.path.join(pathToParsed, "home_db")):
        os.makedirs(os.path.join(pathToParsed, "home_db"))
    home_db_parsed = os.path.join(pathToParsed, "home_db")
    metadata_sqlite = nullcontext

    # hladanie home.db
    for file in directory.rglob("home.db"):
        metadata_sqlite = file
        print(file)
    #jeho parsovanie do csv formatu
    dbparser(metadata_sqlite, home_db_parsed)


    if not os.path.exists(os.path.join(pathToParsed, "sync_history_db")):
        os.makedirs(os.path.join(pathToParsed, "sync_history_db"))
    sync_history_db_parsed = os.path.join(pathToParsed, "sync_history_db")
    metadata_sqlite = nullcontext
    # hladanie sync_history.db
    for file in directory.rglob("sync_history.db"):
        metadata_sqlite = file
        print(file)
    #jeho parsovanie do csv formatu
    dbparser(metadata_sqlite, sync_history_db_parsed)

    #hladanie info.json a jeho vypis do vysledku
    for file in directory.rglob("info.json"):
        metadata_sqlite = file
        print(file)
        shutil.copy(file, os.path.join(result, "dropboxMetadataparsed"))
        vysledok = os.path.join(result, "vysledok.txt")

    #zapisujeme zakladne info o dropboxe do vysledok.txt
    with open(vysledok, "a", encoding="utf-8") as file1:
        file1.write("DROPBOX:\n")

        # prefetch udaje
        file1.write("PREFETCH UDAJE:\n")
        file = os.path.join(result, "prefetch.csv")
        df = pd.read_csv(file)
        filtered_rows = df[df['ExecutableName'].astype(str).str.contains(r'DROPBOX.EXE', case=False)]
        last_run_row = filtered_rows.loc[filtered_rows['LastRun'].idxmax()]
        first_run_row = filtered_rows.loc[filtered_rows['SourceCreated'].idxmin()]
        file1.write(f"Posledne zapnutie Dropbox: {last_run_row['LastRun']} \n")
        file1.write(f"Prve zapnutie Dropbox: {first_run_row['SourceCreated']}  \n")


        #amcache udaje
        file = os.path.join(result, "amcache.csv")
        file1.write("AMCACHE UDAJE:\n")
        df = pd.read_csv(file)
        filtered_rows = df[df['Name'].astype(str).str.contains(r'Dropbox.exe', case=False)]
        version_row = filtered_rows.loc[filtered_rows['Version'].idxmax()]
        file1.write(f"Cesta k exe suboru: {version_row['FullPath']}  \n")
        file1.write(f"Verzia Dropbox: {version_row['Version']}  \n")


        #zapis z databazovych tabuliek
        df = pd.read_csv(os.path.join(sync_history_db_parsed, "sync_history.csv"))
        file1.write("UDAJE ZO SYNC_HISTORY DATABAZI:\n")
        df = df.nlargest(10, 'timestamp')
        file1.write(f"10 POSLEDNYCH AKCII NA SUBOROCH NA DROPBOXE: \n")
        for index, hodnota in df.iterrows():
            filename = hodnota['local_path'].replace("\\", "/").split("/")[-1]
            file1.write(
                f"nazov suboru: {filename} druh akcie: {hodnota['file_event_type']} cas akcie: {datetime.fromtimestamp(hodnota['timestamp'])} \n")



        #jumplist udaje
        df = pd.read_csv(os.path.join(result, "jumplist.csv"))
        df = df[df['Path'].str.contains(r'\\Dropbox\\', na=False, case=False)]
        df = df.sort_values(by='TargetAccessed', ascending=False)
        top5 = df.iloc[:5, :].copy()
        top5['Path'] = top5['Path'].apply(lambda x: str(x).split('\\')[-1])
        file1.write("Z JUMPLISTOV 5 SUBOROV Z DROPBOXU: \n")
        for _, row in top5.iterrows():
            file1.write(
                f"nazov suboru: {row['Path']} cas posledneho otvorenia:{row['TargetAccessed']} cas vytvorenia suboru:{row['TargetCreated']} \n")
