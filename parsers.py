import os
import csv
import sqlite3
import subprocess

def dbparser(pathTofile,pathToexport):
    db_file = pathTofile

    # Pripojenie k databáze
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Načítanie zoznamu tabuliek
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(tables)

    # Export každej tabuľky do CSV
    for table in tables:
        table_name = table[0]
        csv_file = os.path.join(pathToexport, f"{table_name}.csv")  # Uloženie do priečinka

        # Načítanie údajov z tabuľky
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Načítanie názvov stĺpcov
        column_names = [description[0] for description in cursor.description]

        # Zápis údajov do CSV
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Hlavička
            writer.writerows(rows)  # Dáta

        print(f"Tabuľka {table_name} bola exportovaná do {csv_file}.")


