FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["gunicorn", "payment_gateway.wsgi", "--bind", "0.0.0.0:8000"]