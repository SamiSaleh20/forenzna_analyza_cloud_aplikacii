import os
import shutil
from contextlib import nullcontext
from importlib.metadata import metadata
from pathlib import Path
import csv
import sqlite3
from parsers import dbparser

current_directory = os.getcwd()#cesta k projektu
if not os.path.exists(os.path.join(current_directory, "googledriveMetadataparsed")):
    os.makedirs(os.path.join(current_directory, "googledriveMetadataparsed"))
pathToParsed=os.path.join(current_directory, "googledriveMetadataparsed")#cesta ku extrahovanym metadatam googledrive
#directory=Path(os.path.join(current_directory, "googledriveMetadata"))
if not os.path.exists(os.path.join(pathToParsed, "metadata_sqlite_db")):
    os.makedirs(os.path.join(pathToParsed, "metadata_sqlite_db"))
matedata_sqlite_db_parsed=os.path.join(pathToParsed, "metadata_sqlite_db")
directory=Path("C:\\Users\\sami\\OneDrive - UPJŠ\\SS-BP\\googledrive\\googlebox_metadata")
metadata_sqlite=nullcontext
for file in directory.rglob("metadata_sqlite_db"):
    metadata_sqlite=file
    print(file)
# parsovanie suboru
dbparser(metadata_sqlite,matedata_sqlite_db_parsed)
for file in directory.rglob("mirror_sqlite.db"):
    metadata_sqlite=file
    print(file)
if not os.path.exists(os.path.join(pathToParsed, "mirror_sqlite")):
    os.makedirs(os.path.join(pathToParsed, "mirror_sqlite"))
matedata_sqlite_db_parsed=os.path.join(pathToParsed, "mirror_sqlite")
dbparser(metadata_sqlite,matedata_sqlite_db_parsed)
if not os.path.exists(os.path.join(pathToParsed, "logfiles")):
    os.makedirs(os.path.join(pathToParsed, "logfiles"))

for file in directory.rglob("*drive_fs*"):
    print(file)
    shutil.copy(file,os.path.join(pathToParsed, "logfiles"))