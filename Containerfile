# Dockerfile for Gradio Chatbot on OpenShift

# Use a Universal Base Image (UBI) with Python 3.9 from Red Hat
# UBI images are recommended for OpenShift deployments.
FROM registry.access.redhat.com/ubi8/python-39

# Set a working directory inside the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to avoid storing cache data in the image,
# and --upgrade pip to ensure pip is up-to-date.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application source code into the working directory
# This includes app.py, config.py, llm_service.py, and ui.py
COPY app.py .
COPY config.py .
COPY llm_service.py .
COPY ui.py .

# Expose the port Gradio runs on (default is 7860)
EXPOSE 7860

# Define the command to run the Gradio application
# This will start the Gradio server when the container launches.
CMD ["python", "app.py"]