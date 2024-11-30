FROM python:3.9.14-alpine3.16

WORKDIR /app

COPY . /app/

#RUN dnf update -vy
#RUN dnf install -vy python3 python3-pip libpq-devel python-devel postgresql-devel rpm-build gcc g++

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#RUN pip install gunicorn
ENV FLASK_APP=/app/src/app.py

EXPOSE 5000

#CMD ["python3", "src/app.py"]

# Install the New Relic Python agent
RUN pip install --no-cache-dir newrelic


ENV NEW_RELIC_APP_NAME="msvc_email_blacklists"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=1653a7c83fbce0c72ac4aa35a093bb62FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

# Use Gunicorn to serve the application
# ENTRYPOINT ["newrelic-admin", "run-program", "gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
# ENTRYPOINT [ "newrelic-admin", "run-program" ]
#CMD ["newrelic-admin", "run-program", "flask", "run", "--host=0.0.0.0:5000"]
ENTRYPOINT [ "newrelic-admin", "run-program", "python3", "src/app.py" ]