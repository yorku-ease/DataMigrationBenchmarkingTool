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

    def parseResources(self, resources):
        if not resources:
            return {
                'cpu_quota': None,
                'cpu_period': None,
                'cpu_shares': None,
                'mem_limit': None,
                'mem_reservation': None
            }

        limits = resources.get('limits', {})
        reservations = resources.get('reservations', {})

        # Initialize default values
        cpu_quota = None
        cpu_period = 100000  # Default to 100 milliseconds
        cpu_shares = None
        mem_limit = None
        mem_reservation = None

        # Convert CPU limits
        if 'cpus' in limits:
            cpu_quota = int(float(limits['cpus']) * cpu_period)
        
        # Convert CPU reservations
        if 'cpus' in reservations:
            cpu_shares = int(float(reservations['cpus']) * 1024)
        
        # Convert memory limits and reservations
        mem_limit = limits.get('memory')
        mem_reservation = reservations.get('memory')

        return {
            'cpu_quota': cpu_quota,
            'cpu_period': cpu_period,
            'cpu_shares': cpu_shares,
            'mem_limit': mem_limit,
            'mem_reservation': mem_reservation
        }

