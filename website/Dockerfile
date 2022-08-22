FROM python:3.7
WORKDIR /usr/src/app

# Kopioi kaiken docker kontin /usr/src/app sijaintiin
COPY . .

# Asentaa requirements.txt tiedostossa olevat kirjastot esim. flask
RUN pip install --no-cache-dir -r requirements.txt


CMD python3 -m flask run --host=0.0.0.0 --port=$PORT