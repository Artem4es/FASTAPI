FROM python:3.9-slim
WORKDIR /app/src/
COPY requirements.txt .
RUN apt-get update
# RUN apt install libcairo2-dev pkg-config python3.9-dev gcc ffmpeg -y
RUN apt-get install libcairo2-dev pkg-config gcc ffmpeg -y
RUN pip install -r requirements.txt --no-cache-dir

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY . .

RUN mkdir /app/uploads/
RUN mkdir /app/uploads/mp3/
RUN mkdir /app/uploads/wav/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]