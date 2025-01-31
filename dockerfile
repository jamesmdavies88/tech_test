# Use a slim Python image
FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

WORKDIR /app

COPY Pipfile* ./

# Install Python dependencies using pipenv in system mode.
RUN pipenv install --deploy --system

# Copy the entire project
COPY . .

# Ensure entrypoint.sh has execute permissions
RUN chmod +x entrypoint.sh

# Set the shell script as the entrypoint
ENTRYPOINT ["./entrypoint.sh"]