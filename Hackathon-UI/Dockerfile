# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /src

# Set Python to not buffer output
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["streamlit", "run", "/src/everest-info-assist.py", "--server.port", "8080", "--server.headless", "true"]