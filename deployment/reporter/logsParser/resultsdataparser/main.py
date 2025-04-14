from container_data_processor import ContainerDataProcessor

log_file = 'cadvisor.log'
final_folder = 'output/final'
full_process = True  # Change this to True if you want to save individual container data and plots
additional_containers = ['db2target','db2source']
processor = ContainerDataProcessor(log_file, final_folder,additional_containers)
processor.process_all(full_process)
