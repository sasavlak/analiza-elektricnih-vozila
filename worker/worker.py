from aiohttp import web


# Funkcija koja provjerava radi li Worker
async def health(request):
    return web.json_response(
        {
            "status": "radi",
            "servis": "worker"
        }
    )


# Kreiranje aplikacije
app = web.Application()

# Registracija HTTP rute
app.router.add_get("/health", health)

# Pokretanje servera
if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8081)