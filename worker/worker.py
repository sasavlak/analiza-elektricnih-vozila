from aiohttp import web


# Funkcija koja provjerava radi li Worker
async def health(request):
    return web.json_response(
        {
            "status": "radi",
            "servis": "worker"
        }
    )

# Funkcija koja obrađuje primljene podatke
async def analyze(request):
    data = await request.json()

    vehicles = data["vehicles"]

    vehicle_count = len(vehicles)

    range_sum = 0
    maximum_range = 0

    for vehicle in vehicles:
        electric_range = vehicle["electric_range"]

        range_sum += electric_range

        if electric_range > maximum_range:
            maximum_range = electric_range

    return web.json_response(
        {
            "vehicle_count": vehicle_count,
            "range_sum": range_sum,
            "maximum_range": maximum_range
        }
    )

# Kreiranje aplikacije
app = web.Application()

# Registracija HTTP rute
app.router.add_get("/health", health)
app.router.add_post("/analyze", analyze)

# Pokretanje servera
if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8081)