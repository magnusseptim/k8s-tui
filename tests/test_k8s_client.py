from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

print("Listing pods with Kubernetes Python client:")
pods = v1.list_pod_for_all_namespaces(watch=False)

for pod in pods.items:
    print(f"Pod Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}")
