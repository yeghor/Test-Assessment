FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install --no-cache-dir .

COPY . /app/

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app" ]