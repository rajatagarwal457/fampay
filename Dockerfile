# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=run.py
ENV SECRET_KEY=your-secret-key
ENV DATABASE_URL="sqlite:///database.db"
ENV YOUTUBE_API_KEYS="<YOUR-KEYS-HERE>"

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
CMD ["python", "run.py"]