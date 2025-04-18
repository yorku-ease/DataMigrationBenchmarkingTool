import unittest,os,subprocess,sys,threading,time,re,ctypes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from consumer import startConsumer
from consumer import create_topics
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)



class TestLogger(unittest.TestCase):
    bootstrap_servers = "localhost:9092"
    key_pattern = re.compile(r'Key=(.*?),')
    value_pattern = re.compile(r'Value=(.*)')
    @classmethod
    def tearDownClass(self):
        try:
            # Run docker-compose down to stop and remove containers
            compose_file_path = '../docker-compose.yml'
            
            # Run docker-compose up with the specified service name
            subprocess.run(['docker', 'compose', '-f', compose_file_path, 'down'], check=True) 
            replacement_text = '{{ hostvars["reporter"]["ansible_host"] }}'
            target_text = 'localhost'
            replace_text_in_file(compose_file_path, target_text, replacement_text)  
            remove_log_files()     
        except subprocess.CalledProcessError as e:
            print(f"Error during tearDown: {e}")
            # Handle the error as needed

    @classmethod
    def setUpClass(self):

        try:
            files =["framework.log","migrationEngine.log","performanceBenchmark.log"]
            for file in files:
                if os.path.exists(file):
                    os.remove(file)
            compose_file_path = '../docker-compose.yml'
            target_text = '{{ hostvars["reporter"]["ansible_host"] }}'
            replacement_text = 'localhost'
            replace_text_in_file(compose_file_path, target_text, replacement_text)
            # Run docker-compose up with the specified service name
            subprocess.run(['docker', 'compose', '-f', compose_file_path,'up','-d'], check=True)
              # Replace with your Kafka broker address
            create_topics(self.bootstrap_servers)
            
            # Create a thread for the startConsumer function
            self.consumer_thread = threading.Thread(target=startConsumer)

            # Set the thread as a daemon, so it will exit when the main program exits
            self.consumer_thread.daemon = True

            # Start the consumer thread
            self.consumer_thread.start()

        except Exception as e:
            print(f"Error: {e}")
            # Handle the error as needed


    def testframeworktopic(self):
        parseFile("framework.log","framework",self.key_pattern,self.value_pattern,self.bootstrap_servers)
        time.sleep(10)
        with open("framework.log", 'r') as file1, open('expectedFiles/framework.log', 'r') as file2:
            content1 = file1.read().strip()
            content2 = file2.read().strip()
            self.assertEqual(content1, content2)
    def testmigrationEnginetopic(self):
        parseFile("migrationEngine.log","migrationEngine",self.key_pattern,self.value_pattern,self.bootstrap_servers)
        time.sleep(10)
        with open("migrationEngine.log", 'r') as file1, open('expectedFiles/migrationEngine.log', 'r') as file2:
            content1 = file1.read().strip()
            content2 = file2.read().strip()
            self.assertEqual(content1, content2)

    def testperformanceBenchmarktopic(self):
        parseFile("performanceBenchmark.log","performanceBenchmark",self.key_pattern,self.value_pattern,self.bootstrap_servers)
        time.sleep(10)
        with open("performanceBenchmark.log", 'r') as file1, open('expectedFiles/performanceBenchmark.log', 'r') as file2:
            content1 = file1.read().strip()
            content2 = file2.read().strip()
            self.assertEqual(content1, content2)

def createProducer(bootstrap_servers):
    admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})
    print("Producer Established connection with kafka")

    # Create a Kafka producer instance
    producer = Producer({
        'bootstrap.servers': bootstrap_servers,
        'acks': 'all',  # Wait for all in-sync replicas to acknowledge
        'delivery.timeout.ms': 10000  # Set a delivery timeout (optional)
    })
    return producer 

def replace_text_in_file(file_path, target_text, replacement_text):
    """
    Replace all occurrences of target_text in the file with replacement_text.
    
    :param file_path: Path to the file
    :param target_text: Text to find and replace
    :param replacement_text: Replacement text
    """
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Escape special characters in the target text for regex
        escaped_target_text = re.escape(target_text)
        
        # Replace the target text with the replacement text
        updated_content = re.sub(escaped_target_text, replacement_text, content)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        print(f"Replaced occurrences of '{target_text}' with '{replacement_text}' in {file_path} successfully.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_log_files():
    """
    Remove all files ending with .log in the current directory.
    """
    current_dir = os.getcwd()
    log_files = [f for f in os.listdir(current_dir) if f.endswith('.log')]
    
    for log_file in log_files:
        try:
            os.remove(log_file)
            print(f"Removed: {log_file}")
        except Exception as e:
            print(f"Failed to remove {log_file}: {e}")

def parseFile(filename,topic,key_pattern,value_pattern,bootstrap_servers):
    filename = "expectedFiles/" + filename
    producer = createProducer(bootstrap_servers)
    with open(filename, "r") as file:
        # Iterate through each line in the file
        for line in file:
            key_match = key_pattern.search(line.strip())
            value_match = value_pattern.search(line.strip())
            if key_match and value_match:
                key = key_match.group(1).strip()
                value = value_match.group(1).strip()
                producer.produce(topic=topic, key=key, value=value)

    producer.flush()

if __name__ == '__main__':
    unittest.main()