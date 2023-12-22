# Use a base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt  requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI apps into the container
COPY app1 /app


# Expose ports
EXPOSE 8000
EXPOSE 7000

# Start the first FastAPI app on port 8000
CMD ["./start.sh"]
