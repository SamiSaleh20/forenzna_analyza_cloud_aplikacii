import os
import csv
from pathlib import Path




def isthere(result):
    prefetch = os.path.join(result,"prefetch.csv")  # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    pathToPrefetchOutput = Path(os.path.join(result, "parsPrefetch\\ProgramExecution")) # cesta k priecinku  kapu prefetch
    if os.path.exists(prefetch):
        os.remove(prefetch)
    ONEDRIVE: bool = False
    GOOGLEDRIVE: bool = False
    DROPBOX: bool = False
    oVersion,gVersion,dVersion,oLastRun,gLastRun,dLastRun= [""] * 6
    files = os.listdir(pathToPrefetchOutput)  # list nazvou suborou v priecinku priecinku vystupu prefech
    filtered_files = [f for f in files if f.endswith("PECmd_Output.csv")]  # filtrujeme aby sme mali subor co chceme
    if filtered_files:
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

    print("Nachadza sa Onedrive: {}, verzia: {}, posledne otvorenie: {}".format(ONEDRIVE, oVersion, oLastRun))
    print("Nachadza sa Dropbox: {}, verzia: {}, posledne otvorenie: {}".format(DROPBOX, dVersion, dLastRun))
    print("Nachadza sa Googledrive: {}, verzia: {}, posledne otvorenie: {}".format(GOOGLEDRIVE, gVersion, gLastRun))
    return ONEDRIVE,GOOGLEDRIVE,DROPBOX
#otvorime subor kde je vysledom prefetch a do vysledku zapiseme riadky ktore obsahuju googledrive dropbox alebo onedrive
#zmenime pravdivostnu hodnotu ak sa nachadza niektora z tych aplikacii







#vypiseme ci sa nachadza nenachadza



