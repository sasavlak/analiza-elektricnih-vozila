import pandas as pd


# Putanja do CSV datoteke
file_path = "podaci/elektricna_vozila.csv"


# Učitavanje podataka iz CSV datoteke
data = pd.read_csv(file_path)


# Ispis svih učitanih podataka
print("Učitani podaci:")
print(data)


# Ispis broja vozila
vehicle_count = len(data)

print()
print("Ukupan broj vozila:", vehicle_count)