import unittest,os,subprocess,time,docker,shutil

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

class TestDeployment(unittest.TestCase):

    def wait_for_container(self, container_name, timeout=900):
        start_time = time.time()
        client = docker.from_env()
        exist = False
        j = 0
        while time.time() - start_time < timeout and exist == False:
            try:
                # Check if the container is running
                container = client.containers.get(container_name)
                exist = container.status == 'running'
            except docker.errors.NotFound:
                # Container is not running, wait and retry
                j = j + 1
                print(f"check N°{j} : container {container_name} not found yet.")
                time.sleep(1)
                pass
            finally:
                # Close the Docker client connection
                client.close()
        
        return exist
    
    def test_deploy(self):
        try:
            shutil.copy2('../docker-compose.yml', 'docker-compose.yml')

            # Run docker-compose up with the specified service name
            subprocess.run(['docker', 'compose','up', '-d', "controller"], check=True)

            self.assertTrue(self.wait_for_container('controller'), "Timed out waiting for 'controller' container to start.")
            migrationContainerStarted = False
            controllerisAlive = True
            while(not migrationContainerStarted and controllerisAlive):
                migrationContainerStarted = self.wait_for_container('MigrationEngine')
                controllerisAlive = self.wait_for_container('controller')

            self.assertTrue(migrationContainerStarted, "'MigrationEngine' not started.")
  
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            # Handle the error as needed

    def tearDown(self):
        try:
            # Run docker-compose down to stop and remove containers
            
            # Run docker-compose up with the specified service name
            subprocess.run(['docker', 'compose', 'down'], check=True)        
        except subprocess.CalledProcessError as e:
            print(f"Error during tearDown: {e}")
            # Handle the error as needed
if __name__ == '__main__':
    unittest.main()