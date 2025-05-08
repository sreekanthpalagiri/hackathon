# Use an official Python runtime as a parent image
FROM python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # Set the working directory in the container
# WORKDIR /app

COPY . .

WORKDIR /app

RUN chmod 777 deploy.sh
# Make sure the script is executable
RUN chmod 777 /deploy.sh

RUN pwd
RUN ls -l


RUN ls -l /




EXPOSE 8080

# Run app.py when the container launches
CMD ["sh", "deploy.sh"]