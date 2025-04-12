import csv
import os
from pathlib import Path
current_directory = os.getcwd()
#metoda na vybranie informacii z jumplistov
def jumplistParsing(result):
    # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    jumplist = os.path.join(result,"jumplist.csv")
    if os.path.exists(jumplist):
        os.remove(jumplist)
    directory = Path(os.path.join(result, "parsJumplists"))
    #hladame output kape modelu
    for file in directory.rglob("*AutomaticDestinations.csv"):
        print(file)
        automaticDestinations = file
    #otvorime output na citanie a jumplist csv na pisanie
    with open(jumplist, 'w', encoding='utf-8') as file:
        with open(automaticDestinations, mode='r', encoding='utf-8') as file1:
            reader = csv.DictReader(file1)
            print(reader.fieldnames)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            #ak sa nachadza v outpute riadok ktory v sebe ma dropbox,onedrive alebo my Drive tak ho zapiseme
            for row in reader:
                if any(x in row['Path'] for x in ["\\Dropbox\\", "\\OneDrive\\", "\\My Drive\\"]):
                    print(row['Path'])
                    writer.writerow(row)








