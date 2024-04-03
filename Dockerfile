FROM python:3.11

COPY . .
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
RUN poetry install --no-root

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]