import os,configparser,json
class ConfigManager: 

    def __init__(self):
        # Get the directory of the currently running script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Change the working directory to the script's directory
        os.chdir(script_dir)

        pass
    def str_to_bool(self,value):
        return str(value).strip().lower() in ("true", "1", "yes", "y")
    
    def readConfig(self):
        
        parser = configparser.ConfigParser()
        parser.comment_prefixes = (';',)  
        parser.read('/app/configs/migrationEngineConfig.ini')
        conf = {}
        conf["sourceDB2host"] = parser.get('sourceServer', 'host')
        conf["sourceDB2Username"] = parser.get('sourceServer', 'username')
        conf["sourceDB2Password"]= parser.get('sourceServer', 'password')
        conf["sourceDB2Port"] = int(parser.get('sourceServer', 'port'))

        #conf["sourceSshHost"] = parser.get('sourceServerSSH', 'host')
        #conf["sourceSshPort"] = parser.get('sourceServerSSH', 'port')
        #conf["sourceSshUsername"] = parser.get('sourceServerSSH', 'username')
        #conf["sourceSshPassword"] = parser.get('sourceServerSSH', 'password')
        #conf["sourceClearingscriptpath"] = parser.get('sourceServerSSH', 'clearingscriptpath')
        #conf["sourceContainerName"] = parser.get('sourceServerSSH', 'containerName')


        conf["targetDB2host"] = parser.get('targetServer', 'host')
        conf["targetDB2Username"] = parser.get('targetServer', 'username')
        conf["targetDB2Password"] = parser.get('targetServer', 'password')
        conf["targetDB2Port"] = int(parser.get('targetServer', 'port'))
        conf["targetDB2type"] = parser.get('targetServer', 'type') 

        #conf["targetSshHost"] = parser.get('targetServerSSH', 'host')
        #conf["targetSshPort"] = parser.get('targetServerSSH', 'port')
        #conf["targetSshUsername"] = parser.get('targetServerSSH', 'username')
        #conf["targetSshPassword"] = parser.get('targetServerSSH', 'password')
        #conf["targetClearingscriptpath"] = parser.get('targetServerSSH', 'clearingscriptpath')
        #conf["targetContainerName"] = parser.get('targetServerSSH', 'containerName')




        conf["compress"] = parser.get('experiment', 'compress', fallback='NO')
        conf["maxStreams"]=int(parser.get('experiment', 'maxStreams', fallback='1'))
        conf["binary"]=self.str_to_bool(parser.get('experiment', 'binary', fallback='False'))
        conf["tables"]=parser.get('experiment', 'tables').split('_')
        conf["tables"] = [ conf["sourceDB2Username"].upper() + '.' + element for element in conf["tables"] ]
        conf["sourceDatabasetoTargetDatabase"]=parser.get('experiment', 'sourceDatabasetoTargetDatabase').split('_')
        conf["loggingId"] = parser.get('migrationEnvironment', 'loggingId')
        conf["websiteUsername"] = parser.get('migrationEnvironment', 'websiteUsername')
        conf["websitePassword"] = parser.get('migrationEnvironment', 'websitePassword')
        conf["dummy"] = parser.getboolean('migrationEnvironment', 'dummy', fallback='False')
        #conf["dummyTable"] = conf["sourceDB2Username"].upper() + '.' + parser.get('migrationEnvironment', 'dummyTable')
        conf["dummyTable"] = parser.get('migrationEnvironment', 'dummyTable')

        
        if conf['tables'][0] == "*":
            conf["whole_db"] = True
        else:
            conf["whole_db"] = False

        with open("/app/configs/migrationengine_static.json", "r") as f:
            json_conf = json.load(f)
            conf.update(json_conf)
        
        return conf