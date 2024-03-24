# Use an official Python runtime as the parent image
FROM python:3.9.6-slim-buster AS builder

# Set the working directory in the container
WORKDIR /app

# Install any needed packages in requirements.txt
COPY ./docker/requirements.txt .
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Use a second stage to minimize the final image size
FROM python:3.9.6-slim-buster AS final

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container at /app
COPY ./src ./src

# Copy installed packages from the builder stage
COPY --from=builder /app/dependencies ./dependencies

# Add installed dependencies to PYTHONPATH
ENV PYTHONPATH=/app/dependencies

# Set an environment variable for the default data path
ENV PROCESSED_DATA_PATH=/app/data

# Set the default entrypoint to Python
ENTRYPOINT ["python"]