import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

class ContainerDataProcessor:
    def __init__(self, log_file, final_folder='final',additional_containers = []):
        self.log_file = log_file
        self.final_folder = final_folder
        self.additional_containers = additional_containers
        os.makedirs(self.final_folder, exist_ok=True)
        self.combined_data = defaultdict(lambda: defaultdict(list))
        self.variables = [
            ('cpu.usage.total', 'Total CPU Usage', 'cpu_usage_total.png', 'Usage (nanoseconds)'),
            ('cpu.usage.per_cpu_usage', 'Per-CPU Usage', 'cpu_per_cpu_usage.png', 'Usage (nanoseconds)', True),
            ('diskio.io_service_bytes[0].stats.Total', 'Disk I/O Service Bytes', 'diskio_io_service_bytes.png', 'Bytes'),
            ('diskio.io_serviced.stats.Total', 'Disk I/O Serviced', 'diskio_io_serviced.png', 'Operations'),
            ('memory.usage', 'Memory Usage', 'memory_usage.png', 'Bytes'),
            ('memory.max_usage', 'Memory Max Usage', 'memory_max_usage.png', 'Bytes'),
            ('memory.cache', 'Memory Cache', 'memory_cache.png', 'Bytes'),
            ('network.rx_bytes', 'Network RX Bytes', 'network_rx_bytes.png', 'Bytes'),
            ('network.rx_packets', 'Network RX Packets', 'network_rx_packets.png', 'Packets'),
            ('network.tx_bytes', 'Network TX Bytes', 'network_tx_bytes.png', 'Bytes'),
            ('network.tx_packets', 'Network TX Packets', 'network_tx_packets.png', 'Packets')
        ]
    
    def load_data_from_file(self):
        with open(self.log_file, 'r') as f:
            self.data = [json.loads(line) for line in f]

    def filter_migration_data(self):
        self.migration_data = [entry for entry in self.data if entry['container_Name'].startswith('MigrationEngine')]
        experimentsStartTime = ( self.migration_data[0]['timestamp'].rstrip('Z')[:26] if self.migration_data and self.migration_data[0] is not None else "0001-01-01T00:00:00.000000")
        experimentsEndTime = ( self.migration_data[-1]['timestamp'].rstrip('Z')[:26] if self.migration_data and self.migration_data[-1] is not None else "9999-12-31T23:59:59.999999")        
        format = "%Y-%m-%dT%H:%M:%S.%f"
        dt1 = datetime.strptime(experimentsStartTime, format)
        dt2 = datetime.strptime(experimentsEndTime, format)

        for container in self.additional_containers : 
            self.migration_data = self.migration_data + [entry for entry in self.data if( entry['container_Name'] == container and dt1 <= datetime.strptime(entry['timestamp'].rstrip('Z')[:26],format) <= dt2 ) ]
        
        
    def process_container_data(self, full_process):
        for container_name, container_entries in pd.DataFrame(self.migration_data).groupby('container_Name'):
            output_folder = "output/" + container_name
            if full_process:
                os.makedirs(output_folder, exist_ok=True)
            
            timestamps = [self.parse_timestamp(entry['timestamp']) for entry in container_entries.to_dict('records')]
            container_stats = container_entries.to_dict('records')
            experimentsStartTS = timestamps[0]
            experimentsEndTS = timestamps[-1]
            additional_container_stats = []
            format = "%Y-%m-%dT%H:%M:%S.%f"
            for container in self.additional_containers :
                additional_container_stats = additional_container_stats + [entry for entry in self.migration_data if( entry['container_Name'] == container and experimentsStartTS <= datetime.strptime(entry['timestamp'].rstrip('Z')[:26],format) <= experimentsEndTS ) ]

            if full_process:
                self.save_container_data(container_stats + additional_container_stats, output_folder)

            self.create_plots(container_name, container_stats, timestamps, output_folder, full_process)

    def save_container_data(self, container_stats, output_folder):
        with open(os.path.join(output_folder, 'data.json'), 'w') as f:
            json.dump(container_stats, f, indent=4)
    
    def create_plots(self, container_name, container_stats, timestamps, output_folder, full_process):
        for var_path, title, filename, ylabel, *is_list in self.variables:
            keys = var_path.split('.')
            if is_list and is_list[0]:
                if full_process:
                    num_cpus = len(container_stats[0]['container_stats']['cpu']['usage']['per_cpu_usage'])
                    for cpu_idx in range(num_cpus):
                        y_values = [entry['container_stats']['cpu']['usage']['per_cpu_usage'][cpu_idx] for entry in container_stats]
                        self.create_plot(
                            timestamps,
                            y_values,
                            f'{title} (CPU {cpu_idx})',
                            'Time',
                            ylabel,
                            os.path.join(output_folder, f'cpu_{cpu_idx}_{filename}')
                        )
            else:
                y_values = []
                filtered_timestamps = []
                for i, entry in enumerate(container_stats):
                    try:
                        value = entry['container_stats']
                        for key in keys:
                            value = value[key]
                        y_values.append(value)
                        filtered_timestamps.append(timestamps[i])
                    except (KeyError, TypeError):
                        y_values.append(None)
                if full_process:
                    self.create_plot(
                        filtered_timestamps,
                        y_values,
                        title,
                        'Time',
                        ylabel,
                        os.path.join(output_folder, filename)
                    )

                # Store data for combined plot
                self.combined_data[var_path][container_name] = (filtered_timestamps, y_values)

    def create_combined_plots(self):
        for var_path, title, filename, ylabel, *is_list in self.variables:
            if is_list and is_list[0]:
                # Skip per-CPU usage for combined plots
                continue

            self.create_combined_plot(
                self.combined_data[var_path],
                title,
                'Time',
                ylabel,
                os.path.join(self.final_folder, filename)
            )

    @staticmethod
    def parse_timestamp(timestamp):
        timestamp = timestamp.rstrip('Z')[:26]
        format = "%Y-%m-%dT%H:%M:%S.%f"
        datetime.strptime(timestamp, format)
        return datetime.strptime(timestamp, format)

    @staticmethod
    def scale_values(values, unit):
        values = [v for v in values if v is not None]
        if not values:
            return values, unit  # Return as is if empty
        if unit == 'Bytes':
            if max(values) > 1e9:
                return [v / 1e9 for v in values], 'GB'
            elif max(values) > 1e6:
                return [v / 1e6 for v in values], 'MB'
            elif max(values) > 1e3:
                return [v / 1e3 for v in values], 'KB'
            else:
                return values, 'Bytes'
        return values, unit

    def create_plot(self, x, y, title, xlabel, ylabel, output_file):
        y, unit = self.scale_values(y, ylabel)
        if not y:  # Ensure there are y values to plot
            print(f"No data to plot for {title}")
            return
        plt.figure(figsize=(12, 6))
        plt.plot(x, y, linestyle='-', label=title)
        plt.title(title, fontsize=16, weight='bold')
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(f'{ylabel} ({unit})', fontsize=14)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
        plt.tight_layout()
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

    def create_combined_plot(self, data_dict, title, xlabel, ylabel, output_file):
        plt.figure(figsize=(12, 6))
        for container_name, values in data_dict.items():
            timestamps, y_values = values
            y_values, unit = self.scale_values(y_values, ylabel)
            plt.plot(timestamps, y_values, label=container_name)
        plt.title(title, fontsize=16, weight='bold')
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(f'{ylabel} ({unit})', fontsize=14)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
    def process_averages(self,full_process):

        for container in self.additional_containers :
            

            for container_name, container_entries in pd.DataFrame(self.migration_data).groupby('container_Name'):
                output_folder =  "output/" + container_name
                if full_process:
                    os.makedirs(output_folder, exist_ok=True)
                
                timestamps = [self.parse_timestamp(entry['timestamp']) for entry in container_entries.to_dict('records')]
                container_stats = container_entries.to_dict('records')
                experimentsStartTS = timestamps[0]
                experimentsEndTS = timestamps[-1]
                additional_container_stats = []
                format = "%Y-%m-%dT%H:%M:%S.%f"
                for container in self.additional_containers :
                    additional_container_stats = additional_container_stats + [entry for entry in self.migration_data if( entry['container_Name'] == container and experimentsStartTS <= datetime.strptime(entry['timestamp'].rstrip('Z')[:26],format) <= experimentsEndTS ) ]

                if full_process:
                    self.save_container_data(container_stats + additional_container_stats, output_folder)

    def process_all(self, full_process=True):
        self.load_data_from_file()
        self.filter_migration_data()
        self.process_container_data(full_process)
        self.process_averages(full_process)
        self.create_combined_plots()
        print("All containers processed.")
#"diskio":{"io_service_bytes":[{"device":"/dev/vda","major":254,"minor":0,"stats":{"Async":0,"Discard":0,"Read":696320,"Sync":696320,"Total":696320,"Write":0}}],
          
#"io_serviced":[{"device":"/dev/vda","major":254,"minor":0,"stats":{"Async":0,"Discard":0,"Read":49,"Sync":49,"Total":49,"Write":0}}]}
