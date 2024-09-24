import docker
import time
import os

def is_container_live(client, container_name):
    try:
        container = client.containers.get(container_name)
        return container.status == 'running'
    except docker.errors.NotFound:
        return False

def wait_for_container(client, container_name):
    while True:
        try:
            container = client.containers.get(container_name)
            print(f"{container_name} container has appeared.")
            return container
        except docker.errors.NotFound:
            print(f"Waiting for {container_name} container to appear...")
            time.sleep(5)  # Check every 5 seconds

def main():
    client = docker.from_env()
    container_name = 'controller'
    check_interval = 10  # seconds

    # Wait for the container to appear
    wait_for_container(client, container_name)

    while True:
        if not is_container_live(client, container_name):
            print(f"{container_name} container is not live. Running 'docker compose down'.")
            os.system('docker compose down')
            break
        else:
            print(f"{container_name} container is still running.")
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
