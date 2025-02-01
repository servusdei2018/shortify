FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/
EXPOSE 8080
CMD ["python3", "app.py"]