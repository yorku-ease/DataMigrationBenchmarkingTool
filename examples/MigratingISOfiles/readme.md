# Example of an experiment 

In this folder you can find the `config.ini` that was used to run the experiment to migrate a file of around 5GB.

All output of the experiment is saved in the output folder.

Note :  Data in `resourceConsumption.json`  was generated from the endpoint "http://localhost:9090/api/v1/query?query=container_memory_rss{job=%22cAdvisor%22}[1h]"
We generated data for the metric 'container_memory_rss", the same thing can be done for any other metric (CPU, Network ...)
