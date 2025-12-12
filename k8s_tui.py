# final_k8s_tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, TabbedContent, TabPane
from kubernetes import client, config
import sys


class KubernetesTUI(App):
    """"Terminal UI for viewing Kubernetes resources"""

    CSS_PATH = "styles.css"

    def __init__(self):
        super().__init__()
        self.data = {tab: "Loading..." for tab in ["pods", "services", "deployments"]}
        self.load_data()

    def load_data(self):
        """Load all Kubernetes data before the app starts"""
        try:
            print("Loading Kubernetes configuration...", file=sys.stderr)
            config.load_kube_config()
            print("Configuration loaded successfully", file=sys.stderr)

            # Initialize API clients
            v1 = client.CoreV1Api()
            apps_v1 = client.AppsV1Api()

            # Fetch pods
            print("Fetching pods...", file=sys.stderr)
            pods = v1.list_pod_for_all_namespaces(watch=False)
            self.data["pods"] = "\n".join([f"📦 {p.metadata.name} ({p.status.phase})"
                                           for p in pods.items])
            print(f"Found {len(pods.items)} pods", file=sys.stderr)

            # Fetch services
            print("Fetching services...", file=sys.stderr)
            services = v1.list_service_for_all_namespaces(watch=False)
            self.data["services"] = "\n".join([f"🌐 {s.metadata.name}"
                                               for s in services.items])
            print(f"Found {len(services.items)} services", file=sys.stderr)

            # Fetch deployments
            print("Fetching deployments...", file=sys.stderr)
            deployments = apps_v1.list_deployment_for_all_namespaces(watch=False)
            self.data["deployments"] = "\n".join([f"📦 {d.metadata.name}"
                                                  for d in deployments.items])
            print(f"Found {len(deployments.items)} deployments", file=sys.stderr)

        except Exception as e:
            error_msg = f"Error loading Kubernetes data: {str(e)}"
            for key in self.data:
                self.data[key] = error_msg
            print(error_msg, file=sys.stderr)
            import traceback
            traceback.print_exc()

    def compose(self) -> ComposeResult:
        """Compose the TUI with all the data"""
        yield Header()
        with TabbedContent(initial="pods"):
            for tab, data in self.data.items():
                with TabPane(tab.title(), id=tab):
                    yield Label(data, classes="resource-view")
        yield Footer()


if __name__ == "__main__":
    print("Starting Kubernetes TUI...", file=sys.stderr)
    app = KubernetesTUI()
    app.run()
