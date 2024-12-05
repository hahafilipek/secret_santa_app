# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8501

# Run the Streamlit app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


