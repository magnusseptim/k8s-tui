 # Kubernettes TUI with OpenTelemetry
 
 A terminal-based UI for visualising Kubernetes resources with OpenTelemetry observability.
 
 ## Setup
 
 1. Install dependencies:
 ``` bash
 uv add kubernetes opentelemetry-sdk
 ```
 
 2. Start Minikube:
 ```bash
 minikube start
 ```
 
 3. Run the OpenTelemetry test:
 
 ```bash
 python otel_logging.py
 ```
 
 ## Features
 
 - Kubernetes resource visualisation
 - OpenTelemetry logging
 - Pixel-art TUI (coming soon ;) )