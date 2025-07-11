# Dockerfile for Gradio Chatbot on OpenShift

# Use a Universal Base Image (UBI) with Python 3.9 from Red Hat
# UBI images are recommended for OpenShift deployments.
FROM registry.access.redhat.com/ubi8/python-39

# Set a working directory inside the container
WORKDIR /app
USER root
# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
# Copy the requirements file into the working directory
COPY requirements.txt .
COPY pip.conf /etc/pip.conf
# Install Python dependencies
# and --upgrade pip to ensure pip is up-to-date.
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application source code into the working directory
# This includes app.py, config.py, and llm_service.py
COPY app.py .
COPY config.py .
COPY llm_service.py .

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /app /home/appuser

# Switch to non-root user
USER appuser

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Define the command to run the Streamlit application
# This will start the Streamlit server when the container launches.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]