import csv
import os
from pathlib import Path
import getpass
import csv
from parsers import regparser
import pandas as pd
import os
from datetime import datetime
def function(result):
    current_directory = os.getcwd()
    registry = os.path.join(result,"registry.csv")  # csv subor kde budu vsetky riadky co nas zaujimaju ak existuje vymazeme
    registri = os.path.join(current_directory, "registri.csv")
    if os.path.exists(registry):
        os.remove(registry)
    directory = Path(os.path.join(result, "exRegistry\\C\\Users"))
    for file in directory.rglob("NTUSER.DAT"):
            NTUSER = file
    print(file)
    regparser(NTUSER, registri)
    with open(registry, 'w', encoding='utf-8') as file:
        with open(registri, mode='r', encoding='utf-8') as file1:
            reader = csv.DictReader(file1)
            print(reader.fieldnames)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if any(x in row['Key Path'] for x in ["OneDrive", "Dropbox", "DriveFS"]):
                    print(row['Key Path'])
                    writer.writerow(row)
    os.remove(registri)



