import os
import csv
from pathlib import Path




def isthere(result):
    # csv subor kde budu vsetky riadky co nas zaujimaju z prefetchou ak existuje vymazeme
    prefetch = os.path.join(result,"prefetch.csv")
    # cesta k priecinku  kde su sparsovane prefetche
    pathToPrefetchOutput = Path(os.path.join(result, "parsPrefetch"))
    if os.path.exists(prefetch):
        os.remove(prefetch)
    #booleane ci sa nachadzaju apky
    ONEDRIVE: bool = False
    GOOGLEDRIVE: bool = False
    DROPBOX: bool = False
    #zakladne info o apkach ktore vypiseme do konzoly ak su v systeme
    oVersion,gVersion,dVersion,oLastRun,gLastRun,dLastRun= [""] * 6
    # najdeme output parsovanych prefetchov
    files = os.listdir(pathToPrefetchOutput)
    filtered_files = [f for f in files if f.endswith("PECmd_Output.csv")]
    if filtered_files:
        #ak sme nasli output otvorime hona citanie a otvorime aj prefetch.csv na pisanie
        selected_file = filtered_files[0]
        file_path = os.path.join(pathToPrefetchOutput, selected_file)
        print(f"Vybraný súbor: {file_path}")
        csv.field_size_limit(10 * 1024 * 1024)
        with open(prefetch, 'w', encoding='utf-8') as file:
            with open(file_path, mode='r', encoding='utf-8') as file1:
                reader = csv.DictReader(file1)
                print(reader.fieldnames)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                #ak sa nachadza v outpute jedna z apiek ktore hladame nachadza sa automaticky v systeme nastavajume zakaldne info
                for row in reader:
                    if "ONEDRIVE" in row['ExecutableName']:
                        print(row['ExecutableName'])
                        if ONEDRIVE==False:
                            oVersion=row['Version']
                            oLastRun=row['LastRun']
                        ONEDRIVE = True
                        if row['Version']>oVersion:
                            oVersion = row['Version']
                        if row['LastRun']>oLastRun:
                            oLastRun = row['LastRun']
                        writer.writerow(row)
                    if "DROPBOX" in row['ExecutableName']:
                        if DROPBOX==False:
                            dVersion=row['Version']
                            dLastRun=row['LastRun']
                        DROPBOX = True
                        if row['Version']>dVersion:
                            dVersion = row['Version']
                        if row['LastRun']>dLastRun:
                            dLastRun = row['LastRun']

                        writer.writerow(row)
                    if "GOOGLEDRIVEFS" in row['ExecutableName']:
                        if GOOGLEDRIVE==False:
                            gVersion=row['Version']
                            gLastRun=row['LastRun']
                        GOOGLEDRIVE = True
                        if row['Version']>gVersion:
                            gVersion = row['Version']
                        if row['LastRun']>gLastRun:
                            gLastRun = row['LastRun']
                        writer.writerow(row)
    #kratky vypis do konzoly co sme nasli v systeme
    print("Nachadza sa Onedrive: {}, verzia: {}, posledne otvorenie: {}".format(ONEDRIVE, oVersion, oLastRun))
    print("Nachadza sa Dropbox: {}, verzia: {}, posledne otvorenie: {}".format(DROPBOX, dVersion, dLastRun))
    print("Nachadza sa Googledrive: {}, verzia: {}, posledne otvorenie: {}".format(GOOGLEDRIVE, gVersion, gLastRun))
    #uz len vypis ci sa nachadza alebo nie v prefetch.csv
    return ONEDRIVE,GOOGLEDRIVE,DROPBOX










