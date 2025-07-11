# AI Chatbot with Streamlit and LangChain

This is a simple chatbot application that uses Streamlit for the user interface and LangChain with a backend LLM service (like vLLM) for generating responses.

## Features

*   **Interactive UI**: A clean, conversational user interface built with Streamlit.
*   **Stateful Conversations**: Remembers conversation history for a given session.
*   **LangChain Integration**: Utilizes LangChain for seamless interaction with a large language model.
*   **Containerized**: Comes with a `Containerfile` for building a portable container image.
*   **Helm Chart**: Includes a Helm chart for easy deployment to Kubernetes or OpenShift.

---

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python**: Version 3.9 or higher.
*   **Podman** or **Docker**: For building and running the container image.
*   **OpenShift CLI (`oc`)** or **Kubernetes CLI (`kubectl`)**: If deploying to a cluster.
*   **Helm**: For deploying with the provided chart.
*   Access to a running **vLLM (or compatible OpenAI API) endpoint**.

---

## 1. Local Development Setup

Follow these steps to run the chatbot on your local machine.

### a. Clone the Repository

If you haven't already, clone the repository to your local machine.

### b. Create a Virtual Environment

Navigate to the `chatbot-app` directory and create a Python virtual environment. This isolates the project dependencies.

```bash
cd chatbot-app
python3 -m venv venv
source venv/bin/activate
```

### c. Configure Environment Variables

The application requires API credentials for the LLM. Create a `.env` file in the `chatbot-app` directory by copying the example:

```bash
# It's good practice to have an example file in your repo
# For now, create it manually:
touch .env
```

Open the `.env` file and add the following, replacing the placeholder with your actual vLLM endpoint URL:

```plaintext
# .env
VLLM_API_URL="http://your-vllm-api-endpoint.com/v1"
VLLM_API_KEY="your-api-key" # Can be any string, as required by vLLM
VLLM_MODEL_NAME="your-model" # The model name your vLLM is serving
```

### d. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### e. Run the Application

Launch the Streamlit application:

```bash
streamlit run app.py
```

Your default web browser should open a new tab at `http://localhost:8501` with the chatbot interface.

---

## 2. Building and Running with a Container

You can build a container image for the application using the provided `Containerfile`.

### a. Build the Image

Run the following command from the `chatbot-app` directory to build the image. Replace `your-image-name:latest` with a name and tag of your choice.

```bash
# Using Podman
podman build -t your-image-name:latest .

# Or using Docker
docker build -t your-image-name:latest .
```

### b. Run the Container

Run the container, making sure to pass the `.env` file and map the port.

```bash
# Using Podman
podman run --env-file .env -p 8501:8501 your-image-name:latest

# Or using Docker
docker run --env-file .env -p 8501:8501 your-image-name:latest
```

You can now access the chatbot in your browser at `http://localhost:8501`.

---

## 3. Deployment to OpenShift/Kubernetes with Helm

The included Helm chart simplifies deployment to a cluster.

### a. Configure Helm Values

Before deploying, you must edit `helm/values.yaml` to match your environment.

Key values to update:
*   `image.repository`: The full path to your container image in a registry that your cluster can access (e.g., `quay.io/your-user/chatbot-app`).
*   `llm.apiUrl`: The **in-cluster URL** for your vLLM service.
*   `llm.modelName`: The model name your vLLM is serving.
*   `llm.apiKey`: The API key for your vLLM service. This will be stored in a Kubernetes secret.
*   `route.host`: (OpenShift specific) If you want a specific hostname for your route, specify it here.

### b. Install the Helm Chart

Navigate to the `chatbot-app` directory and run the following Helm command.

```bash
# Replace 'chatbot-release' with a release name of your choice
helm install chatbot-release ./helm
```

This command will:
1.  Create a Kubernetes Secret to store your `VLLM_API_KEY`.
2.  Create a Deployment to run your chatbot container.
3.  Create a Service to expose the application within the cluster.
4.  Create an OpenShift Route (if `route.enabled` is `true`) for external access.

### c. Check the Deployment Status

You can check the status of your deployment by running:

```bash
# Using kubectl
kubectl get pods -l app=chatbot-release-chatbot-app-chart

# Or using oc
oc get pods -l app=chatbot-release-chatbot-app-chart
```

Once the pod is running, you can find the external URL by checking the routes:

```bash
# OpenShift
oc get route chatbot-release-chatbot-app-chart
``` 