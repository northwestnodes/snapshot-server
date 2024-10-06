FROM python:3.12.7-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY * .
CMD ["python3", "snapshot_server.py"]