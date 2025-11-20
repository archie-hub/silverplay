FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    GOLDHOLDINGS=1 \
    SILVERHOLDINGS=1 \
    MYHOLDINGSSTRING="my new string"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]