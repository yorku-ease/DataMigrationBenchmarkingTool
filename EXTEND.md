# Manual for extending the data migration Benchmarking tool

## Overview
In this manual, we will show how to extend our tool.
## Bringing your own migration engine
TBD
## Extending the default migration engine
<details><summary>Extending the file splitting algorithm </summary>
<br />
In this case you're going to edit the code that should be deployed on the source machine.
<br />
<p> 1. clone this repository on your sourceserver.</p>
<p> 2. The class responsible of dealing with files is called FilesManager which you could find in this path : <br />
DataMigrationBenchmarkingTool/fileMigration/classes/migrationEngine/defaultEngine/filesmanager/FilesManager.py <br /> 
In order to change the default splitting algorithm you have to extend this class and override 3 static functions : <br />

     splitFile(input_file,num_files = None):
        this function takes input_file which is the full path of the file and splits it into chunks and saves them in the data folder
        it's preferable to use input_file to choose the path of the chunks.
        you might optionally give it num_files if you want to specify how many chunks you want to save
    
     getChunksPaths(local_file_path,remote_file_path,num_files = None)-> Tuple[List[str], List[str]]:
        local_file_path is the full path of the file without split
        remote_file_path is the full path of the file without split on the remote machine , this is useful to choose the remote_chunks_paths
        this function returns local_chunks_paths which are the paths of the chunks after running splitFile and remote_chunks_paths which should be the paths of the chunks on the remote machine 

     removeSplittedFiles(input_file,num_files= None):
        this function deletes the local chunks after migrating them, it can stay empty if you prefer to keep the local chunks
There is file on the path /DataMigrationBenchmarkingTool/fileMigration/classes/migrationEngine/defaultEngine/filesmanager/NewFilesManager.py , you can directly put your code in there.
</p>
<p> 3. Open the file /DataMigrationBenchmarkingTool/fileMigration/classes/migrationEngine/defaultEngine/DefaultFileMigrator.py<br />
<ul>
  <li>Add this import line below to the imports at the beginning of the file. <br />
"from classes.migrationEngine.defaultEngine.filesmanager.NewFilesManager import NewFilesManager" </li>
  <li>Now you're going to edit the first line of the migrateMultipleStreams() function : <br />
  change "filesmanager = FilesManager" to "filesmanager = NewFilesManager" </li>
</ul>

 </p>
<p> 4. If there is any library that you have imported in your code and "pip install" needs to run to install it, you have to add this library to the file below <br />
/DataMigrationBenchmarkingTool/fileMigration/requirements.txt
<br />
Now that's it all changes to the code are done.
</p>
<p> 5. Change Directory ; use the 'cd' command to change your working directory to /DataMigrationBenchmarkingTool/fileMigration.</p>
<p> 6. Run docker build -t fareshamouda/datamigrationbenchmarkingtool:latest . <br />
Note : it's very important to run this command on the sourcemachine, you could do steps 1-4 on your dev machine, however you have to copy the repo with all new changes to the sourcemachine and the do steps 5-6 on that machine.
<br />
</p>
</details>
<details><summary>Extending the compression algorithm</summary>
TBD
</details>

## Final steps

Now after following the extension steps, you  need to go back to the [README.md](README.md) file and follow all the rest of the steps.


