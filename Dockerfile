FROM python:3.12-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir poetry

# Copy dependency files first
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the application code
COPY . /app

ENV PYTHONPATH=/app/src

# Make port 8083 available for the app
EXPOSE 8083

# Run the command to start the Flask app
CMD ["python", "src/main.py"]



