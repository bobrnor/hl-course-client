FROM arm32v6/python:alpine

COPY ./.app/ /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["python", "-u", "/app/main.py"]