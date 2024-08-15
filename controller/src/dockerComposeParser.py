import yaml
class DockerComposeParser():

    def __init__(self, filepath):
        self.filepath = filepath

    def parseFile(self):
        with open(self.filepath, 'r') as file:
            return yaml.safe_load(file)

    def parsePorts(self,ports_list):
        if ports_list is None : 
            return {} 
        return {port.split(':')[0]: int(port.split(':')[1]) for port in ports_list}

    def parseResources(self,resources):
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
