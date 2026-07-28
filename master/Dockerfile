FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY master/master.py .
COPY podaci/Electric_Vehicle_Population_Data.csv podaci/Electric_Vehicle_Population_Data.csv

RUN mkdir -p rezultati

CMD ["python", "master.py"]