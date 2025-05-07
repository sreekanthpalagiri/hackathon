# Use an official Python runtime as a parent image
FROM python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # Set the working directory in the container
# WORKDIR /app

COPY . .

WORKDIR /app





# # Set the working directory in the container
# WORKDIR /app


# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]