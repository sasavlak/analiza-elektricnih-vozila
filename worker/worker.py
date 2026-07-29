import sys
import asyncio
from aiohttp import web


# Provjera radi li worker servis
async def health(request):
    return web.json_response({
        "status": "radi",
        "servis": "worker"
    })


# Obrada podataka koje je poslao master
async def analyze(request):
    data = await request.json()

    # Simulacija obrade 2 skunde
    await asyncio.sleep(2)

    vehicles = data["vehicles"]

    vehicle_count = len(vehicles)
    range_sum = 0
    maximum_range = 0
    minimum_range = None
    manufacturer_counts = {}

    for vehicle in vehicles:
        manufacturer = vehicle["manufacturer"]
        electric_range = vehicle["electric_range"]

        range_sum += electric_range

        if electric_range > maximum_range:
            maximum_range = electric_range

        if minimum_range is None or electric_range < minimum_range:
            minimum_range = electric_range

        if manufacturer not in manufacturer_counts:
            manufacturer_counts[manufacturer] = 0

        manufacturer_counts[manufacturer] += 1

    return web.json_response({
        "vehicle_count": vehicle_count,
        "range_sum": range_sum,
        "maximum_range": maximum_range,
        "minimum_range": minimum_range,
        "manufacturer_counts": manufacturer_counts
    })

# Dopuštena veličina http zahtjeva povećana je na 100 MB, zbog greške
app = web.Application(
    client_max_size=100 * 1024 * 1024
)


# Registracija ruta
app.router.add_get("/health", health)
app.router.add_post("/analyze", analyze)


# Pokretanje worker servisa
if __name__ == "__main__":

    port = 8081

    # Provjerava je li prilikom pokretanja upisan broj porta
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print(f"Pokrećem worker na portu {port}")

    web.run_app(
        app,
        host="0.0.0.0",
        port=port
    )