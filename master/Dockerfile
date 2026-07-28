FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY master/master.py .
COPY podaci/elektricna_vozila.csv podaci/elektricna_vozila.csv

RUN mkdir -p rezultati

CMD ["python", "master.py"]