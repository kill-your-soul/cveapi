FROM python:3.11

COPY . .
RUN pip install poetry
RUN poetry install


ENTRYPOINT ["python3", "app/main.py"]