FROM fedora:40

WORKDIR /app

COPY . /app/

RUN dnf update -vy
RUN dnf install -vy python3 python3-pip libpq-devel python-devel postgresql-devel rpm-build gcc g++

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=src.app:app

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0", "--port", "3000" ]