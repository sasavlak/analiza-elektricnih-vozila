import asyncio
import pandas as pd
from aiohttp import ClientSession


# Adrese Worker servisa
worker_urls = [
    "http://127.0.0.1:8081/analyze",
    "http://127.0.0.1:8082/analyze"
]


# Učitavanje CSV datoteke
data = pd.read_csv("podaci/elektricna_vozila.csv")


# Funkcija pretvara jedan dio DataFramea u listu rječnika
def prepare_vehicles(data_chunk):
    vehicles = []

    for _, row in data_chunk.iterrows():
        vehicles.append(
            {
                "manufacturer": row["manufacturer"],
                "electric_range": int(row["electric_range"])
            }
        )

    return vehicles


# Funkcija šalje jedan dio podataka jednom Workeru
async def send_to_worker(session, worker_url, vehicles):
    async with session.post(
        worker_url,
        json={"vehicles": vehicles}
    ) as response:

        result = await response.json()

        return result


async def main():

    # Podjela podataka na dva približno jednaka dijela
    data_chunks = [
        data.iloc[::2],
        data.iloc[1::2]
    ]

    async with ClientSession() as session:

        # Lista zadataka za oba Workera
        tasks = []

        for index in range(len(worker_urls)):

            vehicles = prepare_vehicles(data_chunks[index])

            task = send_to_worker(
                session,
                worker_urls[index],
                vehicles
            )

            tasks.append(task)

        # Paralelno slanje zahtjeva i čekanje svih odgovora
        results = await asyncio.gather(*tasks)

        # Ispis parcijalnih rezultata
        for index, result in enumerate(results):

            print()
            print(f"Rezultat Workera {index + 1}:")
            print(result)

            # Spajanje parcijalnih rezultata svih Workera
    total_vehicle_count = 0
    total_range_sum = 0
    overall_maximum_range = 0

    for result in results:
        total_vehicle_count += result["vehicle_count"]
        total_range_sum += result["range_sum"]

        if result["maximum_range"] > overall_maximum_range:
            overall_maximum_range = result["maximum_range"]

    # Izračun prosječnog električnog dometa
    average_range = total_range_sum / total_vehicle_count

    print()
    print("Završni rezultat:")
    print("Ukupan broj vozila:", total_vehicle_count)
    print("Ukupan zbroj električnog dometa:", total_range_sum)
    print("Prosječni električni domet:", average_range)
    print("Najveći električni domet:", overall_maximum_range)


asyncio.run(main()) 