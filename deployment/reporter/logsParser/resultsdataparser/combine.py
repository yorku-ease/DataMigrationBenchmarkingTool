import os
import json

def collect_and_save_data(root_dir, output_file):
    with open(output_file, 'w') as outfile:
        for subdir, _, files in os.walk(root_dir):
            if os.path.basename(subdir).startswith("MigrationEngine"):
                for file in files:
                    if file == 'data.json':
                        file_path = os.path.join(subdir, file)
                        with open(file_path, 'r') as f:
                            try:
                                data = json.load(f)
                                for entry in data:
                                    try:
                                        json.dump(entry, outfile)
                                        outfile.write('\n')
                                    except json.JSONDecodeError as e:
                                        print(f"Problematic entry in file {file_path}: {entry}")
                                        print(f"Error: {e}")
                            except json.JSONDecodeError as e:
                                print(f"Error decoding JSON from file {file_path}: {e}")
                                f.seek(0)  # Go back to the beginning of the file
                                for i, line in enumerate(f, 1):
                                    try:
                                        json.loads(line)
                                    except json.JSONDecodeError as le:
                                        print(f"Problematic line {i} in file {file_path}: {line.strip()}")
                                        print(f"Error: {le}")
                            except Exception as e:
                                print(f"Unexpected error reading file {file_path}: {e}")


def combine_log_files(output_file):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(os.getcwd()):  # Walk through all directories
            if root == os.getcwd():
                continue  # Skip the current directory
            
            if 'cadvisor.log' in files:
                log_file_path = os.path.join(root, 'cadvisor.log')
                print(f"Reading: {log_file_path}")
                with open(log_file_path, 'r') as infile:
                    # Read and strip leading/trailing newlines
                    content = infile.read().strip()
                    outfile.write(content)
                    outfile.write('\n')

    print(f"Logs successfully combined into: {output_file}")

def main():
    root_dir = '.'  # Change this to your root directory
    #output_file = 'cadvisor_combined.log'
    output_file = 'cadvisor.log'

    combine_log_files(output_file)
    print(f'Combined data saved to {output_file}')

    # Process the combined data with full_process set to False
    #processor = ContainerDataProcessor(output_file)
    #processor.process_all(full_process=False)  # Set to False to only create combined plots

if __name__ == "__main__":
    main()
