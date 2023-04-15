
# Manual for using the data migration tool 

## Overview
blablalbla

## Physical Requirements
blablalbla


## Prerequisites

Docker


 ## Get Started

<details><summary> Step 1 : Setting Up Folders and Files</summary>

```bash
.
├── data/
│   ├── file1.txt
│   ├── file2.csv
│   └── file3.jpg
├── output/
└── configs/
    └── config.ini
```

  This is the structure you need to setup first.<br />
  
  **data**    : In this folder you need to put all the files you want to migrate.<br />
  **output**  : All outputs of the experiment will be found here.<br />
  **configs** : All configs of the experiment must be here.<br />
     &nbsp; &nbsp;**config.ini** :  The configuration file you'll need to edit in step 2.

</details>


<details><summary> Step 2 : Choosing the right configuration for the experiment</summary>
<br />

In this step, you'll edit the config.ini file in the configs folder.
Copy the template of config.ini from configs/config.ini in this repository and change it according to your needs.

**[remoteServer]**  here you save all SSH credentials of the remote server where to migrate the files

&nbsp; &nbsp; - **host** : hostname / IP address of the server<br />
&nbsp; &nbsp; - **username** : username of the server<br />
&nbsp; &nbsp; - **password** : password of the server<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files are going to be stored on the remote server ( path should always end with / )<br />

**[localServer]**  The migration tool is going to be running on the localServer, But we need the password for this server  to run some sudo commands

&nbsp; &nbsp; - **password** : password to run sudo command<br />
&nbsp; &nbsp; - **dataFolder_path** : folder where files that are going to be migrated are savedb (path should always end with /). This value should always be data/ since you're saving your files in that folder as specified in step 1.
  
**[experiment]** 


&nbsp; &nbsp; - **numberOfExperiments** : how many times each experiment is repeated with the same configuration ( for the accuracy of the results ).

&nbsp; &nbsp; - **files** = file1,file2,file3 :  only provide the names of the files. These files must be stored in the data folder specified above.

&nbsp; &nbsp; - **limits** = 1,10,1024 : limits should be in bytes 

&nbsp; &nbsp; - **compressionTypes** = None,lz4,gzip : compression types can be None, lz4 and gzip

**[output]**

&nbsp; &nbsp; - **path** = output/output.csv : path to the file to save the output of the experiments (CSV Format).This value should always be output/something.csv since as specified in step 1, the output of te experiment will be saved in the output folder.

</details>

<details><summary> Step 3 : Run the experiment</summary>

Now everything is ready. 
Go to the root directory of the project and launch this command 
```docker

docker run --privileged --memory="0" --cpus="0" -v "$(pwd)"/data:/app/data -v "$(pwd)"/configs:/app/configs -v "$(pwd)"/output:/app/output fareshamouda/datamigrationbenchmarkingtool

```

this code will run the container with unlimited resources amd launch the experiment.
</details>

<details><summary> Step 4 : Result</summary>

The result of the experiment will be found in output folder in a CSV format file.

</details>