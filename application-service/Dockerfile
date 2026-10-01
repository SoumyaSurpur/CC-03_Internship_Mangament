FROM python:3.12-slim
<<<<<<< HEAD
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8000
=======

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

>>>>>>> 01d1120c3fac282ed78a005fe358dd09e7350d03
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
