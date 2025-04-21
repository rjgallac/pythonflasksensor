python3 -m venv .venv

source .venv/bin/activate
source env/bin/activate


flask --app hello run
python -m flask --app ./src/hello run -h 0.0.0.0
kill $(pgrep -f flask)


docker build -t pythontest:latest . 


docker run -p5001:5000 pythontest:latest


docker run -p 5432:5432 -e POSTGRES_PASSWORD=password --name sensor-postgres postgres 
docker exec -it -u postgres sensor-postgres sh
psql
CREATE DATABASE sensors;

\c sensors

CREATE TABLE sensor_data (
    id serial PRIMARY KEY,
    reading_datetime TIMESTAMP,
    temp_reading NUMERIC(5,2),
    humidity_reading NUMERIC(5,2)
);

gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app

http://localhost:8000/