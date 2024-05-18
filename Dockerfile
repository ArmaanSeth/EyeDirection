FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app","--reload", "--host","0.0.0.0", "--port","8000"]
