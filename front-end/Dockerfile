FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flask must know where the app is
ENV FLASK_APP=app.py

# expose port Flask listens on
EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
