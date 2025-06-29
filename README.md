# Chatbot Application Helm Chart

This repository contains the Helm chart for deploying a simple Gradio-based chatbot application on OpenShift (or any Kubernetes cluster). The chatbot uses LangChain to interact with an LLM model, configurable via environment variables, typically from an OpenShift AI vLLM deployment.

## Application Overview

The chatbot is a Python application built with `Gradio` for the web UI and `LangChain` for interfacing with a Large Language Model (LLM). It is designed to be deployed as a containerized application.

### Key Features

- Simple chat interface.
- Configurable LLM endpoint and API key via environment variables.
- Containerized for easy deployment.

## Local Development Setup

To run the application locally for development or testing:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd my_chatbot_app
    ```

2.  **Create a Python Virtual Environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root of your `my_chatbot_app` directory with the following content. Replace the placeholder values with your actual vLLM API endpoint, model name, and API key.

    ```env
    VLLM_API_URL="http://localhost:8000/v1" # Example: your OpenShift vLLM API endpoint
    VLLM_API_KEY="YOUR_API_KEY_IF_REQUIRED" # Your API key (can be empty if not needed)
    VLLM_MODEL_NAME="YOUR_MODEL_NAME_ON_VLLM" # Example: "llama-2-7b-chat"
    ```

5.  **Run the Gradio Application Locally:**
    ```bash
    python app.py
    ```
    This will start the Gradio server, and you can access the chatbot in your web browser, usually at `http://127.0.0.1:7860`.

## Containerization

The `Containerfile` (or `Dockerfile`) defines how to build the application into a container image.

### Building the Container Image

1.  **Ensure a container engine is Running:** Make sure Docker or Podman is active.

2.  **Navigate to the Application Root:**
    ```bash
    cd my_chatbot_app
    ```

3.  **Build the Image:**
    ```bash
    docker build -t chatbot-app:latest .
    ```

### Push to a Registry

If deploying outside OpenShift's internal registry, you'll need to tag and push the image to a container registry accessible by your OpenShift cluster (e.g., Quay.io, Docker Hub, or your private registry).

```bash
docker tag chatbot-app:latest quay.io/your-username/chatbot-app:latest
docker push quay.io/your-username/chatbot-app:latest
```

If using OpenShift's internal registry (recommended for OpenShift deployments), you'll typically use `oc new-build` as described in the Helm deployment section.

## Deployment on OpenShift using Helm

This Helm chart simplifies the deployment of your chatbot application to an OpenShift 4.16+ cluster.

### Prerequisites

- **OpenShift Cluster:** Access to an OpenShift 4.16+ cluster.
- **`oc` CLI:** OpenShift Command Line Interface installed and configured.
- **`helm` CLI:** Helm CLI (v3) installed.
- **Built Image:** Your application's container image built and pushed to a registry accessible by OpenShift (see "Containerization" above). If using OpenShift's internal registry, the Deployment will pull from the `ImageStreamTag` created by `oc new-build`.

### Helm Chart Configuration

The `chatbot-app-chart/values.yaml` file contains the default configuration. You can override these values during installation using `--set` flags or by providing a custom `values.yaml` file.

Key values to configure in `values.yaml` or via `--set`:

- `image.repository`: The full path to your container image in the registry. For OpenShift internal registry, it will typically be `image-registry.openshift-image-registry.svc:5000/your-openshift-project/chatbot-app`.
- `image.tag`: The tag of your image (e.g., `latest`, `v1.0.0`).
- `llm.apiUrl`: The full API endpoint URL for your vLLM model.
- `llm.modelName`: The name of the model served by your vLLM.
- `llm.apiKey`: The API key for your vLLM endpoint. This will be stored in a Kubernetes Secret. Leave empty (`""`) if no API key is required.
- `route.host`: (Optional) Specify a custom hostname for your application's route. If left empty, OpenShift will generate one.
- `resources`: Adjust requests and limits for CPU and memory as needed.

### Deployment Steps

1.  **Log in to your OpenShift Cluster:**
    ```bash
    oc login --token=<your_token> --server=<your_openshift_api_url>
    ```

2.  **Switch to your Target OpenShift Project/Namespace:**
    ```bash
    oc project your-openshift-project
    ```
    *(Replace `your-openshift-project` with the actual name.)*

3.  **Ensure ImageStream Exists (for OpenShift internal registry):**
    If you built your image using `oc new-build` as suggested, an `ImageStream` named `chatbot-app` will be created automatically. If not, you might need to create it or point `image.repository` to an external registry.

4.  **Install the Helm Chart:**
    Navigate to the `chatbot-app-chart` directory:
    ```bash
    cd chatbot-app-chart
    ```
    Then, install the chart, overriding values from `values.yaml` as necessary:
    ```bash
    helm install my-chatbot-release . \
      --namespace your-openshift-project \
      --set llm.apiUrl="YOUR_OPENSHIFT_VLLM_API_ENDPOINT" \
      --set llm.modelName="YOUR_MODEL_NAME_ON_VLLM" \
      --set llm.apiKey="YOUR_API_KEY_IF_REQUIRED" \
      --set image.repository="image-registry.openshift-image-registry.svc:5000/your-openshift-project/chatbot-app"
    ```
    Remember to replace all placeholder values.

### Verify the Deployment

Check the status of your deployed Kubernetes resources:
```bash
oc get all -l app.kubernetes.io/instance=my-chatbot-release -n your-openshift-project
```
Ensure pods are running and the deployment is healthy.

### Access the Chatbot Application

Get the URL of the OpenShift Route:
```bash
oc get route my-chatbot-release-chatbot-app-chart -n your-openshift-project -o jsonpath='{.spec.host}'
```
Open the URL in your web browser to access the chatbot.

## Chart Customization

You can customize the deployment by modifying `values.yaml` or by passing `--set` flags during `helm install` or `helm upgrade`.

**Example:** To update the replica count:
```bash
helm upgrade my-chatbot-release . --namespace your-openshift-project --set replicaCount=2
```

## Uninstalling the Chart

To uninstall the deployed release:
```bash
helm uninstall my-chatbot-release --namespace your-openshift-project
```
