import os
import csv
import sqlite3
import subprocess
from Registry import Registry
#metoda na parsovanie databazovych suborov do csv formatu
def dbparser(pathTofile,pathToexport):
    db_file = pathTofile

    # Pripojenie k databaze
    connection = sqlite3.connect(db_file, timeout=10)
    cursor = connection.cursor()

    # nacitanie zoznamu tabuliek
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # export tabulike do csv
    for table in tables:
        table_name = table[0]
        #ulozenie do priecinka databazy
        csv_file = os.path.join(pathToexport, f"{table_name}.csv")

        # nacitanie udajov z tabulky
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        # nacitanie nazvov stlpcov
        column_names = [description[0] for description in cursor.description]
        processed_rows = []
        for row in rows:
            processed_row = []
            for item in row:
                # ak je binarna hodnota zapis ju v hexadecimalnom formate
                if isinstance(item, bytes):
                    processed_row.append(item.hex())
                else:
                    processed_row.append(item)
            processed_rows.append(processed_row)

        # zapis udajov do csv
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)

            writer.writerows(processed_rows)



        print(f"Tabuľka {table_name} bola exportovaná do {csv_file}.")
    connection.close()

#metoda na parsovanie registrov v dat formate na csv
def regparser(ntuser_file,output_file):
    # funkcia na prechadzanie hive suboru pouzivajuca rekurziu
    def walk_registry(key, writer, parent_key=""):
        for subkey in key.subkeys():
            # aktualna cesta kluca
            full_key = f"{parent_key}\\{subkey.name()}"
            # zsiaknie vsetkcyh hodnot pre kuc
            for value in subkey.values():
                # spracovanie hodnot pred jej zapisom do csv
                processed_value = value.value()
                #ak binarna hodnota preved do hexadecimalneho formatu
                if isinstance(processed_value, bytes):
                    processed_value = processed_value.hex()
                #zapis do csv cesta,nazov,hodnota,typ
                writer.writerow([full_key, value.name(), str(processed_value), value.value_type_str()])

                # rekurzivne volanie pre podkluce
            walk_registry(subkey, writer, full_key)

    # hlavna logika
    try:
        # nacitanie NTUSER.DAT
        reg = Registry.Registry(ntuser_file)

        # otvorenie csv suboru
        with open(output_file, "w", newline='', encoding="utf-8", errors="replace") as csvfile:
            writer = csv.writer(csvfile)
            # hlavicka csv suboru
            writer.writerow(["Key Path", "Value Name", "Value Data", "Value Type"])
            # prechadzanie a zapisovanie do do csv suboru
            walk_registry(reg.root(), writer)

        print(f"Dáta boli úspešne exportované do {output_file}.")

    except Exception as e:
        print(f"Chyba: {e}")




