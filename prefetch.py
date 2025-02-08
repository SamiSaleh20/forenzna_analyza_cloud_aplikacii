import os
import csv

#hodnoty ktore urcuju ci sa nachadza aplikacia v zariadeni
current_directory = os.getcwd()#cesta k projektu
vysledok=os.path.join(current_directory, "vysledok.csv")#csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme

if os.path.exists(vysledok):
    os.remove(vysledok)
def isthere():
    ONEDRIVE: bool = False
    GOOGLEDRIVE: bool = False
    DROPBOX: bool = False
    oVersion,gVersion,dVersion,oLastRun,gLastRun,dLastRun= [""] * 6
    pathToPrefetchOutput = os.path.join(current_directory,r"parsPrefetch\ProgramExecution")  # cesta k priecinku  kapu prefetch
    files = os.listdir(pathToPrefetchOutput)  # list nazvou suborou v priecinku priecinku vystupu prefech
    filtered_files = [f for f in files if f.endswith("PECmd_Output.csv")]  # filtrujeme aby sme mali subor co chceme
    if filtered_files:
        selected_file = filtered_files[0]
        file_path = os.path.join(pathToPrefetchOutput, selected_file)
        print(f"Vybraný súbor: {file_path}")
        csv.field_size_limit(10 * 1024 * 1024)
        with open(vysledok, 'w', encoding='utf-8') as file:
            with open(file_path, mode='r', encoding='utf-8') as file1:
                reader = csv.DictReader(file1)
                print(reader.fieldnames)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['ExecutableName'] == "ONEDRIVE.EXE":
                        if ONEDRIVE==False:
                            oVersion=row['Version']
                            oLastRun=row['LastRun']
                        ONEDRIVE = True
                        if row['Version']>oVersion:
                            oVersion = row['Version']
                        if row['LastRun']>oLastRun:
                            oLastRun = row['LastRun']
                        writer.writerow(row)
                    if row['ExecutableName'] == "DROPBOX.EXE":
                        if DROPBOX==False:
                            dVersion=row['Version']
                            dLastRun=row['LastRun']
                        DROPBOX = True
                        if row['Version']>dVersion:
                            dVersion = row['Version']
                        if row['LastRun']>dLastRun:
                            dLastRun = row['LastRun']

                        writer.writerow(row)
                    if row['ExecutableName'] == "GOOGLEDRIVEFS.EXE":
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
isthere()






#vypiseme ci sa nachadza nenachadza



