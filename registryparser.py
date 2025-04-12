from pathlib import Path
import csv
from parsers import regparser
import os
#metoda na vybranie zaujimavych informacii z registrov
def function(result):
    current_directory = os.getcwd()
    # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme plus registri kde dame output celeho registra v csv
    registry = os.path.join(result,"registry.csv")
    registri = os.path.join(current_directory, "registri.csv")
    if os.path.exists(registry):
        os.remove(registry)
    directory = Path(os.path.join(current_directory, "exRegistry\\C\\Users"))
    #hladame output z registry targetu
    for file in directory.rglob("NTUSER.DAT"):
            NTUSER = file
    print(file)
    #obsah .dat suboru registrou hodime cely do registri.csv
    regparser(NTUSER, registri)
    #otvorime registri na citanie a registry na pisanie
    with open(registry, 'w', encoding='utf-8') as file:
        with open(registri, mode='r', encoding='utf-8') as file1:
            reader = csv.DictReader(file1)
            print(reader.fieldnames)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            #zapisujeme do registry informacie o aplikaciach  z registrov
            for row in reader:
                if any(x in row['Key Path'] for x in ["OneDrive", "Dropbox", "DriveFS"]):
                    print(row['Key Path'])
                    writer.writerow(row)
    os.remove(registri)



