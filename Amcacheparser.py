import csv
import os
from idlelib.iomenu import encoding
from pathlib import Path
#metoda na vyber informacii z amcache
def amchacheParsing(result):
    current_directory = os.getcwd()
    # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    amcache = os.path.join(result,"amcache.csv")
    if os.path.exists(amcache):
        os.remove(amcache)
    directory=Path(os.path.join(result,"parsAmcache"))
    #hladame output kape modelu pre amcache co su 2 subory
    for file in directory.rglob("*Amcache_Associated*"):
        print(file)
        associated = file
    for file in directory.rglob("*Amcache_Unassociated*"):
        print(file)
        unassociated = file
    #otvorime output na citanie a amcache.csv na pisanie
    with open(amcache, 'w', encoding='utf-8') as file:
        with open(associated, mode='r', encoding='utf-8') as file1, open(unassociated, mode='r',encoding='utf-8') as file2:
            reader1 = csv.DictReader(file1)
            reader2 = csv.DictReader(file2)
            print(reader1.fieldnames)
            fieldnames = reader1.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            #zapisujeme riadky do amcache.csv ktore nas zaujimaju z associated a unassociated
            for row in reader1:
                if any(x in row['ApplicationName'] for x in ["Microsoft OneDrive", "Google Drive"]):
                    print(row['Name'])
                    writer.writerow(row)

            for row in reader2:
                if any(x in row['Name'] for x in ["Dropbox", "OneDrive", "DriveFS"]):
                    print(row['Name'])
                    writer.writerow(row)









