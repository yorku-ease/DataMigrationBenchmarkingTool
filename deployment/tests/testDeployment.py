import os,sys,subprocess,shutil,time,docker,re,threading,traceback
 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from reporter.kafkacluster.consumer import create_topics 
from reporter.kafkacluster.consumer import startConsumer

import unittest

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

class testDeployment(unittest.TestCase):
    bootstrap_servers = "localhost:9092"
    key_pattern = re.compile(r'Key=(.*?),')
    value_pattern = re.compile(r'Value=(.*)')

    def wait_for_container(container_name, timeout=900):
        start_time = time.time()
        client = docker.from_env()
        exist = False
        j = 0
        while time.time() - start_time < timeout and exist == False:
            try:
                # Check if the container is running
                container = client.containers.get(container_name)
                health = container.attrs.get('State', {}).get('Health', {})
                exist = health.get('Status') == 'healthy'

            except docker.errors.NotFound:
                # Container is not running, wait and retry
                j = j + 1
                print(f"check N°{j} : container {container_name} not healthy yet.")
                time.sleep(1)
                pass
            finally:
                # Close the Docker client connection
                client.close()
        return exist
    
    def keyExists(self,filename,timeout=900):
        start_time = time.time()
        key_to_check = "Key=thisIdIsForTestPurposes"
        while time.time() - start_time < timeout:

            time.sleep(1)
            print(f"Checking {filename}")
            try:
                with open(filename, 'r') as file:
                    file_content = file.read()

                    key_exists = key_to_check in file_content

                    if key_exists:
                        return True

            except FileNotFoundError:
                print(f"Error: The file {file} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
        return False
    
    def check_files_exist(self,file_paths,timeout = 900):
        start_time = time.time()
        exist = False
        while time.time() - start_time < timeout and exist == False :
            time.sleep(1)
            for file_path in file_paths :
                file_path = "target/" + file_path
                print(f"checking file {file_path}")
                if os.path.exists(file_path):
                    exist = True
                else:
                    exist = False
        return exist
    
    @classmethod
    def setUpClass(self):
        try:
            # Get the directory of the currently running script
            script_dir = os.path.dirname(os.path.abspath(__file__))

            os.chdir(script_dir)
            self.logFiles =["framework.log","migrationEngine.log","performanceBenchmark.log"]
            files = os.listdir("target")
            for file in files : 
                self.logFiles.append(f"target/{file}")

            for logfile in self.logFiles :
                if os.path.exists(logfile):
                        os.remove(logfile)

            self.kafkaComposefilePath = "../reporter/kafkacluster/docker-compose.yml"
            self.controllerComposefilePath = "../controller/docker-compose.yml"
            shutil.copy2("../reporter/kafkacluster/docker-compose.yml", "kafka-compose-file.yml")
            shutil.copy2("../controller/docker-compose.yml", "controller-compose-file.yml")
            subprocess.run(['docker', 'compose', '-f', "controller-compose-file.yml", 'down','--volumes','--remove-orphans'], check=True)        
            subprocess.run(['docker', 'compose', '-f', "kafka-compose-file.yml", 'down','--volumes','--remove-orphans'], check=True)    
            # Run docker-compose up with the specified service name
            subprocess.run(['docker', 'compose', '-f',"kafka-compose-file.yml",'up','-d'], check=True)
            self.wait_for_container(container_name='kafka1')
            create_topics(self.bootstrap_servers)
            
            # Create a thread for the startConsumer function
            self.consumer_thread = threading.Thread(target=startConsumer)

            # Set the thread as a daemon, so it will exit when the main program exits
            self.consumer_thread.daemon = True

            # Start the consumer thread
            self.consumer_thread.start()

            subprocess.run(['docker', 'compose', '-f',"controller-compose-file.yml",'up','-d'], check=True)

        except Exception as e:
            print(f"Error: {e}")
            # Handle the error as needed


    
    def test_frameworkLoggingtoKafka(self):
        self.assertTrue(self.keyExists("framework.log"))

    def test_performanceLoggingtoKafka(self):
        self.assertTrue(self.keyExists("performanceBenchmark.log"))
    def test_migrationLoggingtoKafka(self):
        self.assertTrue(self.keyExists("migrationEngine.log"))
    def test_OneStreamExperiment(self):
        self.assertTrue(self.check_files_exist(['test.1048576']))
    def test_TwoStreamsExperiment(self):
        self.assertTrue(self.check_files_exist(['test_3_001.1048576','test_3_002.1048576','test_3_003.1048576']))

    @classmethod
    def tearDownClass(self):
        try:
            subprocess.run(['docker', 'compose', '-f', "controller-compose-file.yml", 'down','--volumes','--remove-orphans'], check=True)        
            subprocess.run(['docker', 'compose', '-f', "kafka-compose-file.yml", 'down','--volumes','--remove-orphans'], check=True)        
        except subprocess.CalledProcessError as e:
            print(f"Error during tearDown: {e}")
            # Handle the error as needed

if __name__ == '__main__':
    unittest.main()