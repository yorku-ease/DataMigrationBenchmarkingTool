
# DB2 Migration Service Documentation

## Overview

This document outlines the steps needed to run **DMBench** with the **DB2 Migration Service**, which is specifically designed for migrating DB2 databases.  

This file assumes that you have already read the main [README.md](README.md). Here, we will focus on some specific configurations for the DB2 Migration Service. All other steps remain as described in the README file.

---

## Prerequisites

Before proceeding, ensure the following:

1. **Databases Setup**:  
   - A **source database** and a **target database** must be up and running. These will serve as the origin and destination for the DB2 migration process.  
   - The **source database** should already contain the data you want to transfer.  

2. **Dummy Table Option**:  
   - The **source database** can optionally include a table named `dummy`.  
   - This is used to run a preliminary experiment before each combination of parameters, ensuring that cache from previous experiments is overwritten.  
   - If you choose to use this option, set `dummy = true` in the configuration file.
