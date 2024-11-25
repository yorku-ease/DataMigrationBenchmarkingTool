# Extending the Default Migration Engine

## Overview
This document explains how to extend the **Default Migration Engine** of the Data Migration Benchmarking Tool by editing code in the `migrationengine/defaultengine` directory.

---

## Extending the File Splitting Algorithm

### Steps to Customize the Splitting Logic

#### 1. Clone the Repository
Clone the repository from:
```bash
git clone https://github.com/yorku-ease/DataMigrationBenchmarkingTool.git
cd DataMigrationBenchmarkingTool
```

#### 2. Modify the Code in the `migrationengine/defaultengine` Directory
The `FilesManager.py` file, which handles file splitting, is located at:
```
defaultEngine/filesmanager/FilesManager.py
```

To implement a custom file splitting logic:
1. Create a new class by extending `FilesManager`.  
   - Use the provided template file at:
     ```
     defaultEngine/filesmanager/newFilesManager.py
     ```
   - Override these methods as needed:
     - `splitFile(input_file, num_files=None)`  
       Splits `input_file` into chunks and saves them locally. Optionally, specify `num_files` for a fixed number of chunks.
     - `getChunksPaths(local_file_path, remote_file_path, num_files=None) -> Tuple[List[str], List[str]]`  
       Defines local and remote chunk paths for migration.
     - `removeSplittedFiles(input_file, num_files=None)`  
       Deletes local chunks after migration (can remain empty if keeping local chunks).

2. Save your custom logic in `newFilesManager.py`.

---

#### 3. Integrate the New Logic in `DefaultFileMigrator`
The `DefaultFileMigrator` class is responsible for orchestrating the file migration. To use your new file manager:
1. Open the file:
   ```
   defaultEngine/defaultFileMigrator.py
   ```
2. Add this import statement:
   ```python
   from filesmanager.newFilesManager import NewFilesManager
   ```
3. Modify the first line of the `migrateMultipleStreams` method:
   ```python
   filesmanager = NewFilesManager
   ```

---

#### 4. Add Any Required Dependencies
If your code uses new libraries, add them to:
```
defaultengine/requirements.txt
```

---

## Extending the Compression Algorithm

### Steps to Add a New Compression Algorithm

#### 1. Create a New Compressor Class
In the directory:  
```
defaultEngine/compression
```  
1. Create a new class that implements the `Compressor` interface found in:  
```
defaultEngine/compression/compressor.py
```  
2. Implement the following methods:  
```python
@abstractmethod
def compress(self, data) -> str:
    pass

@abstractmethod
def addFileExtension(self, filename) -> str:
    pass
```  
3. Your `compress` method should handle the logic for compression.  
4. The `addFileExtension` method should take a `filename` and add the appropriate extension (e.g., `.gz` for Gzip).  

For reference, check the existing implementations:  
- `GzipCompressor.py`  
- `Lz4Compressor.py`  

---

#### 2. Update the FilesManager Class
Navigate to:  
```
defaultEngine/filesmanager/FilesManager.py
```  
1. Import your new compressor class:  
```python
from compression.YourCompressor import YourCompressor
```  
2. In the `transferFile` static method, locate the following section:  
```python
if compression == "gzip":
    compressor = GzipCompressor()
elif compression == "lz4":
    compressor = Lz4Compressor()
elif compression == "None":
    pass
else:
    print("Wrong compression type")
    return 0
```  
3. Add a new `if` statement for your compressor:  
```python
elif compression == "yourcompression":
    compressor = YourCompressor()
```  
Replace `yourcompression` with the value you want to use for the `compressionType` in `config.ini`.  

---

#### 4. Add Any Required Dependencies
If your code uses new libraries, add them to:
```
defaultengine/requirements.txt
```

---

## Build and Push the Updated Docker Image

Once you've made the necessary changes, build and push the updated Docker image:

### 1. Build the Docker Image
Change your working directory to the folder containing the Dockerfile:
```bash
cd migrationengine/defaultengine
```
Run the following command to build the Docker image:
```bash
docker build -t your-dockerhub-username/defaultengine:custom .
```

---

### 2. Push the Image to Docker Hub
Log in to Docker Hub:
```bash
docker login
```
Push the updated image:
```bash
docker push your-dockerhub-username/defaultengine:custom
```

---

## Update the Controller Configuration

To use your custom image, update the `docker-compose.yml` file:
1. Navigate to:
```plaintext
deployment/controller/examples/defaultEngine/controller/configs
```
2. Edit the `docker-compose.yml` file to replace the image with your new custom image:
```yaml
    image: your-dockerhub-username/datamigrationbenchmarkingtool:custom
```
