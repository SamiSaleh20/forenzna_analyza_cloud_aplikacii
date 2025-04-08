import csv
import os
from idlelib.iomenu import encoding
from pathlib import Path

def amchacheParsing(result):
    current_directory = os.getcwd()
    amcache = os.path.join(result,"amcache.csv")  # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    if os.path.exists(amcache):
        os.remove(amcache)
    directory=Path(os.path.join(result,"parsAmcache"))
    for file in directory.rglob("*Amcache_Associated*"):
        print(file)
        associated = file
    for file in directory.rglob("*Amcache_Unassociated*"):
        print(file)
        unassociated = file
    with open(amcache, 'w', encoding='utf-8') as file:
        with open(associated, mode='r', encoding='utf-8') as file1, open(unassociated, mode='r',encoding='utf-8') as file2:
            reader1 = csv.DictReader(file1)
            reader2 = csv.DictReader(file2)
            print(reader1.fieldnames)
            fieldnames = reader1.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader1:
                if any(x in row['ApplicationName'] for x in ["Microsoft OneDrive", "Google Drive"]):
                    print(row['Name'])
                    writer.writerow(row)

            for row in reader2:
                if any(x in row['Name'] for x in ["Dropbox", "OneDrive", "DriveFS"]):
                    print(row['Name'])
                    writer.writerow(row)









