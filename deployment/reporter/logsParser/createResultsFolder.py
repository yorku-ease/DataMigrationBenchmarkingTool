import os

def create_new_exp_folder(base_folder):
    # Check if the base folder exists, if not, create it
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # List only the folders starting with 'exp' and ignore others
    existing_folders = [folder for folder in os.listdir(base_folder) if folder.startswith('exp') and folder[3:].isdigit()]

    if not existing_folders:
        new_folder = os.path.join(base_folder, 'exp1')
    else:
        # Extract the numbers from the folder names, sort them, and find the latest
        folder_numbers = sorted(int(folder[3:]) for folder in existing_folders)
        new_folder = os.path.join(base_folder, f'exp{folder_numbers[-1] + 1}')

    # Create the new folder
    os.makedirs(new_folder)
    return new_folder


# Example usage
base_folder =  '/home/{{ hostvars["databases"]["ansible_user"] }}/dmbench/results'
new_folder_path = create_new_exp_folder(base_folder)
print(f'{new_folder_path}')