import time,sys,traceback,os,shutil,configparser,docker,subprocess,yaml,threading


def parse_docker_compose(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_ports(ports_list):
    if ports_list is None : 
        return {} 
    return {port.split(':')[0]: int(port.split(':')[1]) for port in ports_list}

def containerLog(container,service_name):
    log_generator = container.logs(stream=True)
    for log in log_generator:
        print("log " + service_name + " : " +log.decode('utf-8'), end="")  # Print each log line

def parse_resources(resources):
    if not resources:
        return {
            'cpu_quota': None,
            'cpu_period': None,
            'mem_limit': None,
            'mem_reservation': None
        }

    limits = resources.get('limits', {})
    reservations = resources.get('reservations', {})

    # Initialize default values
    cpu_quota = None
    cpu_period = 100000  # Default to 100 milliseconds
    mem_limit = None
    mem_reservation = None

    # Convert CPU limits
    if 'cpus' in limits:
        cpu_quota = int(float(limits['cpus']) * 100000)
    if 'cpus' in reservations:
        cpu_quota_res = int(float(reservations['cpus']) * 100000)
        cpu_quota = cpu_quota_res if cpu_quota_res < cpu_quota else cpu_quota

    # Convert memory limits
    mem_limit = limits.get('memory')
    mem_reservation = reservations.get('memory')

    return {
        'cpu_quota': cpu_quota,
        'cpu_period': cpu_period,
        'mem_limit': mem_limit,
        'mem_reservation': mem_reservation
    }



compose_data = parse_docker_compose('docker-compose.yml')

try:
    container = None

    FOLDERS_PATH = "/home/ubuntu/dump/migrations/db2/controller"

    client = docker.from_env()

    experimentId = "MigrationEngine-" + "self.loggingId"

    volumes = {
        f"{FOLDERS_PATH}/data": {"bind": "/app/data", "mode": "rw"},
        f"{FOLDERS_PATH}/configs": {"bind": "/app/configs", "mode": "rw"},
    }
    labels = {
    'loggingId': "self.loggingId",
    }

    '''container = None
    existing_containers = client.containers.list(all=True)
    container_exists = any(container.name == container_name for container in existing_containers)

    if container_exists:
        container = client.containers.get(container_name)
        container.restart()
    else:'''

        # Create networks
    for network_name, network_config in compose_data.get('networks', {}).items():
        client.networks.create(network_name, **network_config)

    # Create volumes
    for volume_name, volume_config in compose_data.get('volumes', {}).items():
        client.volumes.create(name=volume_name, **volume_config)

    containers = []
    loggingThreads = []
    
    # Create and start containers (services)
    for service_name, service_config in compose_data.get('services', {}).items():
        print(service_config.get('volumes'))
        additional_volume = f"{FOLDERS_PATH}/configs:/app/configs:rw"

        if service_config.get('volumes') is None:
            service_config['volumes'] = [additional_volume]
        elif isinstance(service_config['volumes'], list):
            service_config['volumes'].append(additional_volume)
        container_name =  "MigrationEngine_"+ service_name  + "-" + "self.loggingId"
        try:
            oldContainer = client.containers.get(container_name)
            oldContainer.stop()
            oldContainer.remove()
        except docker.errors.NotFound:
            pass
        resources = parse_resources(service_config.get('deploy', {}).get('resources', {}))
        print(resources) 
        container = client.containers.run(
            image=service_config['image'],
            name=container_name,
            environment=service_config.get('environment'),
            ports=parse_ports(service_config.get('ports')),
            volumes=service_config.get('volumes'),
            network=service_config.get('network'),
            command=service_config.get('command'),
            privileged=service_config.get('privileged'),
            cpu_quota=resources['cpu_quota'],
            cpu_period=resources['cpu_period'],
            mem_limit=resources['mem_limit'],
            mem_reservation=resources['mem_reservation'],
            detach=True  # Run in the background
        )
        log_thread = threading.Thread(target=containerLog, args=(container,service_name))

        # Start the thread
        loggingThreads.append(log_thread.start())

        containers.append(container)

    for container in containers: 
        container.wait()

finally:
    for container in containers:
        if container is not None:
            container.stop()
            container.remove()