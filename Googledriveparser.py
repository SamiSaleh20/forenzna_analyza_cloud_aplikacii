import os
import shutil
from contextlib import nullcontext
from importlib.metadata import metadata
from pathlib import Path
import csv
import sqlite3
from parsers import dbparser
import pandas as pd
from datetime import datetime
from protobuf_decoder.protobuf_decoder import Parser
import json

#vybranie dat o googledrive
def parsing(result):
    current_directory = os.getcwd()
    #vytvorenie priecinka pre data
    pathToParsed = os.path.join(result, "googledriveMetadataparsed")
    if os.path.exists(pathToParsed):
        shutil.rmtree(pathToParsed)
    os.makedirs(pathToParsed)
    if not os.path.exists(os.path.join(pathToParsed, "metadata_sqlite_db")):
        os.makedirs(os.path.join(pathToParsed, "metadata_sqlite_db"))
    metadata_sqlite_db_parsed = os.path.join(pathToParsed, "metadata_sqlite_db")
    directory = Path(os.path.join(current_directory, "googledriveMetadata"))
    metadata_sqlite = nullcontext

    #hladanie metadata_sqlite_db
    for file in directory.rglob("metadata_sqlite_db"):
        metadata_sqlite = file
        print(file)
    # jeho parsovanie do csv formatu
    dbparser(metadata_sqlite, metadata_sqlite_db_parsed)

    #hladanie mirror_sqlite.db
    for file in directory.rglob("mirror_sqlite.db"):
        metadata_sqlite = file
        print(file)
    if not os.path.exists(os.path.join(pathToParsed, "mirror_sqlite")):
        os.makedirs(os.path.join(pathToParsed, "mirror_sqlite"))
    mirror_sqlite_parsed = os.path.join(pathToParsed, "mirror_sqlite")
    # jeho parsovanie do csv formatu
    dbparser(metadata_sqlite, mirror_sqlite_parsed)


    if not os.path.exists(os.path.join(pathToParsed, "logfiles")):
        os.makedirs(os.path.join(pathToParsed, "logfiles"))
    #zapisovanie logov googledrive do vysledku
    for file in directory.rglob("*drive_fs*"):
        print(file)
        shutil.copy(file, os.path.join(pathToParsed, "logfiles"))
        vysledok = os.path.join(result, "vysledok.txt")

    #zapisujeme zakladne info o googledrive do vysledok.txt
    with open(vysledok, "a", encoding="utf-8") as file1:
        file1.write("GOOGLEDRIVE:\n")


        #prefetch udaje
        file1.write("PREFETCH UDAJE:\n")
        file = os.path.join(result, "prefetch.csv")
        df = pd.read_csv(file)
        filtered_rows = df[df['ExecutableName'].astype(str).str.contains(r'GOOGLEDRIVEFS.EXE', case=False)]
        last_run_row = filtered_rows.loc[filtered_rows['LastRun'].idxmax()]
        first_run_row = filtered_rows.loc[filtered_rows['SourceCreated'].idxmin()]
        file1.write(f"Posledne zapnutie GoogleDrive: {last_run_row['LastRun']} \n")
        file1.write(f"Prve zapnutie GoogleDrive: {first_run_row['SourceCreated']}  \n")


        #registry udaje
        file = os.path.join(result, "registry.csv")
        file1.write(f"INFORMACIE Z REGISTRY: \n")
        df = pd.read_csv(file)
        data = df.loc[df['Value Name'] == 'SyncTargets', 'Value Data'].values
        parsed_data = Parser().parse(data[0])
        parsed_data_dict = parsed_data.to_dict()
        user_id = parsed_data_dict['results'][0]['data']['results'][0]['data']['results'][0]['data']
        file1.write(f"User ID: {user_id} \n")
        paths = [
            entry['data']
            for entry in parsed_data_dict['results'][0]['data']['results']
            if entry['field'] == 3
        ]
        file1.write(f"Synchronizovane priecinky: {', '.join(paths)} \n")


        # amcache udaje
        file = os.path.join(result, "amcache.csv")
        file1.write("AMCACHE UDAJE:\n")
        df = pd.read_csv(file)
        googledriveexes = df[df['Name'].astype(str).str.contains(r'GoogleDriveFS.exe', case=False)]
        googledriveexe = googledriveexes.loc[googledriveexes['Version'].idxmax()]
        file1.write(f"Cesta k exe suboru: {googledriveexe['FullPath']}  \n")
        file1.write(f"Verzia GoogleDrive: {googledriveexe['Version']}  \n")


        #zapis z databazovych tabuliek
        file1.write(f"UDAJE Z METADATA_SQLITE_DB:\n")
        df = pd.read_csv(os.path.join(metadata_sqlite_db_parsed, "properties.csv"))
        data = df.loc[df['property'] == 'driveway_account', 'value'].values
        parsed_data = Parser().parse(data[0])
        parsed_data_dict = parsed_data.to_dict()
        user_name = parsed_data_dict['results'][1]['data']['results'][0]['data']['results'][2]['data']
        file1.write(f"meno pouzivatela na googledrive: {user_name} \n")
        email = parsed_data_dict['results'][1]['data']['results'][0]['data']['results'][4]['data']
        file1.write(f"emailova adresa pouzivatela: {email} \n")
        driveway_account_parsed = os.path.join(pathToParsed, "driveway_account.json")
        with open(driveway_account_parsed, "w", encoding="utf-8") as file2:
            json.dump(parsed_data_dict, file2, indent=4)

        data = df.loc[df['property'] == 'account_settings', 'value'].values
        parsed_data = Parser().parse(data[0])
        parsed_data_dict = parsed_data.to_dict()
        account_settings_parsed = os.path.join(pathToParsed, "account_settings.json")
        with open(account_settings_parsed, "w", encoding="utf-8") as file2:
            json.dump(parsed_data_dict, file2, indent=4)

        df = pd.read_csv(os.path.join(metadata_sqlite_db_parsed, "items.csv"))
        df = df[df['is_folder'] == 0]
        starred = df[df['starred'] == 1]
        file1.write(f"OBLUBENE SUBORY: \n")
        file1.write(starred['local_title'].to_string(index=False) + "\n")
        trashed = df[df['trashed'] == 1]
        file1.write(f"VYMAZANE SUBORY: \n")
        file1.write(trashed['local_title'].to_string(index=False) + "\n")
        top_10 = df.nlargest(10, 'viewed_by_me_date')
        file1.write(f"10 NAPOSLEDY OTVORENYCH SUBOROV: \n")
        for index, hodnota in top_10.iterrows():
            cas = hodnota['viewed_by_me_date'] / 1000
            file1.write(
                f"nazov suboru:{hodnota['local_title']} cas posledneho otvorenia:{datetime.fromtimestamp(cas)} \n")
        top_10 = df.nlargest(10, 'modified_date')
        file1.write(f"10 NAPOSLEDY UPRAVOVANYCH SUBOROV: \n")
        for index, hodnota in top_10.iterrows():
            cas = hodnota['modified_date'] / 1000
            file1.write(
                f"nazov suboru:{hodnota['local_title']} cas posledneho otvorenia:{datetime.fromtimestamp(cas)} \n")

        df = pd.read_csv(os.path.join(mirror_sqlite_parsed, "mirror_item.csv"))
        file1.write(f"UDAJE Z MIRROR_SQLITE: \n")
        top_10 = df.nlargest(10, 'cloud_version')
        file1.write(f"10 SUBOROV KTORE BOLI NAJVIAC UPRAVOVANE: \n")
        for index, hodnota in top_10.iterrows():
            file1.write(f"nazov suboru:{hodnota['local_filename']} pocet uprav:{hodnota['cloud_version']} \n")
        file1.write(f"10 ROZDIELNYCH PRIECINKOV/SUBOROV CLOUDU OD LOKALNYCH: \n")
        idx = 0
        for index, hodnota in df.iterrows():
            if (hodnota['local_filename'] != hodnota['cloud_filename'] or hodnota['local_mtime_ms'] != hodnota[
                'cloud_mtime_ms'] or hodnota['local_size'] != hodnota['cloud_size'] or hodnota['local_version'] !=
                    hodnota[
                        'cloud_version'] or hodnota['local_type'] != hodnota['cloud_type']):

                file1.write(hodnota['local_filename'] + "\n")
                if (hodnota['local_filename'] != hodnota['cloud_filename']):
                    file1.write(
                        f"rozdiel v nazve lokalne: {hodnota['local_filename']} v cloude: {hodnota['cloud_filename']} \n")
                if (hodnota['local_mtime_ms'] != hodnota['cloud_mtime_ms']):
                    lokaltime = hodnota['local_mtime_ms'] / 1000
                    cloudtime = hodnota['cloud_mtime_ms'] / 1000
                    file1.write(
                        f"rozdiel v case modifikacie lokalne: {datetime.fromtimestamp(lokaltime)} v cloude: {datetime.fromtimestamp(cloudtime)} \n")
                if (hodnota['local_size'] != hodnota['cloud_size']):
                    file1.write(
                        f"rozdielna velkost lokalne: {hodnota['local_size']} v cloude: {hodnota['cloud_size']} \n")
                if (hodnota['local_version'] != hodnota['cloud_version']):
                    file1.write(
                        f"rozdielny pocet zmien lokalne: {hodnota['local_version']} v cloude: {hodnota['cloud_version']} \n")
                if (hodnota['local_type'] != hodnota['cloud_type']):
                    file1.write(
                        f"rozdielny typ suboru lokalne: {hodnota['local_type']} v cloude: {hodnota['cloud_type']} \n")
                file1.write("\n")

                idx = idx + 1
                if idx == 10:
                    break

