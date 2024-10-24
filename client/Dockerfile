FROM python:3.12.0-bookworm

WORKDIR /server
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "client.py"]
