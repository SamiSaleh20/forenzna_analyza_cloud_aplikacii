import csv
import os
from pathlib import Path
current_directory = os.getcwd()
def jumplistParsing(result):
    jumplist = os.path.join(result,"jumplist.csv")  # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    if os.path.exists(jumplist):
        os.remove(jumplist)
    directory = Path(os.path.join(result, "parsJumplists"))
    for file in directory.rglob("*AutomaticDestinations.csv"):
        print(file)
        automaticDestinations = file
    with open(jumplist, 'w', encoding='utf-8') as file:
        with open(automaticDestinations, mode='r', encoding='utf-8') as file1:
            reader = csv.DictReader(file1)
            print(reader.fieldnames)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if any(x in row['Path'] for x in ["\\Dropbox\\", "\\OneDrive\\", "\\My Drive\\"]):
                    print(row['Path'])
                    writer.writerow(row)








