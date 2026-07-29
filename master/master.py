import asyncio
import time
import json
import pandas as pd
from aiohttp import ClientSession


# Adrese Worker servisa
worker_urls = [
    "http://worker1:8081/analyze",
    "http://worker2:8082/analyze",
    "http://worker3:8083/analyze",
    "http://worker4:8084/analyze"
]


# Učitavanje i čišćenje podataka
data = pd.read_csv("podaci/Electric_Vehicle_Population_Data.csv")
data = data.dropna(subset=["Make", "Electric Range"])
data = data[data["Electric Range"] > 0]

if data.empty:
    raise ValueError("Nakon filtriranja nema podataka za obradu.")


# Pretvaranje dijela tablice u listu vozila
def prepare_vehicles(data_chunk):
    vehicles = []

    for _, row in data_chunk.iterrows():
        vehicle = {
            "manufacturer": str(row["Make"]),
            "electric_range": int(row["Electric Range"])
        }

        vehicles.append(vehicle)

    return vehicles


# Slanje podataka jednom Workeru preko HTTP-a
async def send_to_worker(session, worker_url, vehicles):
    async with session.post(
        worker_url,
        json={"vehicles": vehicles}
    ) as response:

        response.raise_for_status()
        return await response.json()


async def main():
    start_time = time.perf_counter()

    worker_count = len(worker_urls)
    data_chunks = []

    # Podjela podataka između Workera
    for index in range(worker_count):
        data_chunk = data.iloc[index::worker_count]
        data_chunks.append(data_chunk)

    print()
    print("Broj Workera:", worker_count)
    print("Ukupan broj vozila:", len(data))

    for index, data_chunk in enumerate(data_chunks):
        print(
            f"Worker {index + 1} dobiva "
            f"{len(data_chunk)} vozila."
        )

    # Paralelno slanje podataka Workerima
    async with ClientSession() as session:
        tasks = []

        for index in range(worker_count):
            vehicles = prepare_vehicles(data_chunks[index])

            task = send_to_worker(
                session,
                worker_urls[index],
                vehicles
            )

            tasks.append(task)

        results = await asyncio.gather(*tasks)

    print()

    for index, result in enumerate(results):
        print(
            f"Worker {index + 1} obradio je "
            f"{result['vehicle_count']} vozila."
        )

    # Početne vrijednosti za spajanje rezultata
    total_vehicle_count = 0
    total_range_sum = 0
    maximum_range = 0
    minimum_range = None
    manufacturer_counts = {}

    # Spajanje rezultata svih Workera
    for result in results:
        total_vehicle_count += result["vehicle_count"]
        total_range_sum += result["range_sum"]

        if result["maximum_range"] > maximum_range:
            maximum_range = result["maximum_range"]

        if (
            minimum_range is None
            or result["minimum_range"] < minimum_range
        ):
            minimum_range = result["minimum_range"]

        for manufacturer, count in result["manufacturer_counts"].items():
            if manufacturer not in manufacturer_counts:
                manufacturer_counts[manufacturer] = 0

            manufacturer_counts[manufacturer] += count

    # Izračun statistike
    average_range = total_range_sum / total_vehicle_count

    top_10_manufacturers = sorted(
        manufacturer_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    execution_time = time.perf_counter() - start_time

    # Ispis rezultata
    print()
    print("ZAVRŠNI REZULTAT")
    print("----------------")
    print("Ukupan broj vozila:", total_vehicle_count)
    print("Prosječni električni domet:", round(average_range, 2))
    print("Najveći električni domet:", maximum_range)
    print("Najmanji električni domet:", minimum_range)

    print()
    print("TOP 10 PROIZVOĐAČA")

    for position, manufacturer_data in enumerate(
        top_10_manufacturers,
        start=1
    ):
        manufacturer = manufacturer_data[0]
        count = manufacturer_data[1]

        print(
            f"{position}. {manufacturer} "
            f"- {count} vozila"
        )

    print()
    print(
        "Vrijeme izvršavanja:",
        round(execution_time, 4),
        "sekundi"
    )

    # Priprema Top 10 liste za JSON
    top_10_json = []

    for manufacturer, count in top_10_manufacturers:
        top_10_json.append({
            "proizvodac": manufacturer,
            "broj_vozila": count
        })

    # Završni rezultat
    final_result = {
        "broj_workera": worker_count,
        "ukupan_broj_vozila": total_vehicle_count,
        "prosjecni_domet": round(average_range, 2),
        "najveci_domet": maximum_range,
        "najmanji_domet": minimum_range,
        "top_10_proizvodaca": top_10_json,
        "vrijeme_izvrsavanja": round(execution_time, 4)
    }

    # Spremanje rezultata u JSON datoteku
    with open(
        "rezultati/rezultat.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            final_result,
            file,
            ensure_ascii=False,
            indent=4
        )

    print()
    print(
        "Rezultat je spremljen u "
        "rezultati/rezultat.json"
    )


if __name__ == "__main__":
    asyncio.run(main())