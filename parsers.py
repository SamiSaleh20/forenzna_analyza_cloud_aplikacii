import os
import csv
import sqlite3
import subprocess
from Registry import Registry
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
        processed_rows = []
        for row in rows:
            processed_row = []
            for item in row:
                if isinstance(item, bytes):  # Ak je položka binárna
                    processed_row.append(item.hex())  # Uložíme ako hexadecimálny reťazec
                else:
                    processed_row.append(item)  # Necháme položku ako je
            processed_rows.append(processed_row)

        # Zápis údajov do CSV
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Hlavička
            #writer.writerows(rows)
            writer.writerows(processed_rows)

            # Dáta

        print(f"Tabuľka {table_name} bola exportovaná do {csv_file}.")

def regparser(ntuser_file,output_file):
    # Funkcia na prechádzanie kľúčov a export do CSV
    def walk_registry(key, writer, parent_key=""):
        for subkey in key.subkeys():
            # Aktuálna cesta kľúča
            full_key = f"{parent_key}\\{subkey.name()}"
            # Získanie všetkých hodnôt pre kľúč
            for value in subkey.values():
                # Spracovanie hodnôt pred zápisom do CSV
                processed_value = value.value()

                if isinstance(processed_value, bytes):  # Ak je hodnota binárna
                    processed_value = processed_value.hex()  # Preveď ju na hexadecimálny reťazec

                # Zápis do CSV: Kľúč, Názov hodnoty, Hodnota, Typ hodnoty
                writer.writerow([full_key, value.name(), str(processed_value), value.value_type_str()])

                # Rekurzívne prehľadávať podkľúče
            walk_registry(subkey, writer, full_key)

    # Hlavná logika

    try:
        # Načítanie NTUSER.DAT
        reg = Registry.Registry(ntuser_file)

        # Otvorenie CSV súboru
        with open(output_file, "w", newline='', encoding="utf-8", errors="replace") as csvfile:
            writer = csv.writer(csvfile)
            # Hlavička CSV súboru
            writer.writerow(["Key Path", "Value Name", "Value Data", "Value Type"])
            # Prechádzanie všetkých kľúčov a hodnôt
            walk_registry(reg.root(), writer)

        print(f"Dáta boli úspešne exportované do {output_file}.")

    except Exception as e:
        print(f"Chyba: {e}")




