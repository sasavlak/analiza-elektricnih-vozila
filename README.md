Distribuirana analiza podataka o električnim vozilima pomoću Master/Worker arhitekture preko HTTP-a.

Analiza električnih vozila – Master/Worker arhitektura preko HTTP-a

Opis projekta

Ovaj projekt izrađen je u sklopu kolegija Raspodijeljeni sustavi.

Cilj projekta je prikazati rad Master/Worker arhitekture korištenjem HTTP komunikacije između servisa.

Master učitava veliku CSV datoteku s podacima o električnim vozilima, dijeli podatke na više dijelova te ih paralelno šalje Worker servisima. Svaki Worker obrađuje svoj dio podataka i vraća parcijalne rezultate. Master zatim spaja rezultate i izračunava završnu statistiku.

Korištene tehnologije

- Python 3.10
- aiohttp
- asyncio
- pandas
- Docker
- Docker Compose

Struktura projekta
```
ANALIZA-ELEKTRICNIH-VOZILA
│
├── master/
│   ├── master.py
│   └── Dockerfile
│
├── worker/
│   ├── worker.py
│   └── Dockerfile
│
├── podaci/
│   └── Electric_Vehicle_Population_Data.csv
│
├── rezultati/
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```
1. Master učitava CSV datoteku.
2. Podaci se očiste od neispravnih zapisa.
3. Podaci se ravnomjerno podijele između četiri Workera.
4. Master paralelno šalje podatke Workerima preko HTTP-a.
5. Svaki Worker obrađuje svoj dio podataka.
6. Worker vraća parcijalne rezultate.
7. Master spaja rezultate i izračunava završnu statistiku.

Statistika koja se izračunava

- ukupan broj vozila
- prosječni električni domet
- najveći električni domet
- najmanji električni domet
- Top 10 proizvođača prema broju vozila
- vrijeme izvršavanja

Rezultat

Nakon završetka izvođenja ispisuju se rezultati u terminal, a završna statistika sprema se u datoteku.