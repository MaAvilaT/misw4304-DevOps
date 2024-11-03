FROM fedora:40

WORKDIR /app

COPY . /app/

RUN dnf update -vy
RUN dnf install -vy python3 python3-pip libpq-devel python-devel postgresql-devel rpm-build gcc g++

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN pip install gunicorn

ENV FLASK_APP=/app/src/app.py

# Use Gunicorn to serve the application
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:3000", "src.app:app"]
