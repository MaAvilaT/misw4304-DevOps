FROM fedora:37

WORKDIR /app

COPY . /app/

# Update the package manager and install necessary packages
RUN dnf update -y && \
    dnf install -y python3 python3-pip libpq-devel python3-devel postgresql-devel gcc gcc-c++

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Install the New Relic Python agent and gunicorn
RUN pip install --no-cache-dir newrelic gunicorn

ENV FLASK_APP=/app/src/app.py

EXPOSE 5000

# Set New Relic environment variables
ENV NEW_RELIC_APP_NAME="msvc_email_blacklists"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=1653a7c83fbce0c72ac4aa35a093bb62FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

# Use New Relic to run the application with gunicorn
ENTRYPOINT ["newrelic-admin", "run-program", "gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]