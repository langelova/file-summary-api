FROM python:3.10-slim as base

ARG PROJECT=api

# Create a non-root user to run the app with.
RUN groupadd --gid 1000 user &&  adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
USER user

WORKDIR /home/user
# prevent Python from writting .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure Python output is sent to the terminal
ENV PYTHONBUFFERED 1

ENV \
    PATH="/home/user/.local/bin:/home/user/.venv/bin:${PATH}"

COPY --chown=user:user requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM base as dev

COPY --chown=user:user ./$PROJECT /home/user/$PROJECT
COPY --chown=user:user ./run_server.sh /home/user/run_server.sh

RUN chmod +x run_server.sh
CMD bash ./run_server.sh
