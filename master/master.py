import asyncio
import pandas as pd
from aiohttp import ClientSession


# Učitavanje CSV datoteke
data = pd.read_csv("podaci/elektricna_vozila.csv")


async def send_to_worker():

    vehicles = []

    # Pretvaranje DataFramea u listu rječnika
    for _, row in data.iterrows():

        vehicles.append(
            {
                "manufacturer": row["manufacturer"],
                "electric_range": int(row["electric_range"])
            }
        )

    async with ClientSession() as session:

        async with session.post(
            "http://127.0.0.1:8081/analyze",
            json={"vehicles": vehicles}
        ) as response:

            result = await response.json()

            print()
            print("Rezultat koji je vratio Worker:")
            print(result)


asyncio.run(send_to_worker())