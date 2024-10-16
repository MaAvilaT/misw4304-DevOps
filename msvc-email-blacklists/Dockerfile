FROM fedora:40

WORKDIR /app

COPY . /app/

RUN dnf update -vy
RUN dnf install -vy python3 python3-pip libpq-devel python-devel postgresql-devel rpm-build gcc g++

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

ENV FLASK_APP=src/main.py

ENTRYPOINT [ "pipenv", "run", "flask", "run", "--host", "0.0.0.0", "--port", "3000" ]
