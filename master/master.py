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

        results = []

        for index in range(len(worker_urls)):

            vehicles = prepare_vehicles(data_chunks[index])

            result = await send_to_worker(
                session,
                worker_urls[index],
                vehicles
            )

            results.append(result)

            print()
            print(f"Rezultat Workera {index + 1}:")
            print(result)


asyncio.run(main())