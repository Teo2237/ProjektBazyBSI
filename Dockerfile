# Dockerfile

# Krok 1: Wybranie obrazu python'a
FROM python:3.9-slim

# Krok 2: Ustawienie foldera roboczego w kontenerze
WORKDIR /app

# Krok 3: Skopiowanie folder z zależnościami i zastosowanie ich
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Krok 4: Skopiowanie kodu aplikacji do folderu roboczego
COPY ./backend /app

# Krok 5: Komenda, która uruchamia aplikację
CMD ["flask", "run", "--host=0.0.0.0"]