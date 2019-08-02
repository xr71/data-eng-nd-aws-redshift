# Udacity Project - AWS Redshift Cloud Data Warehouse

## Introduction

## Setup
I am using the `awscli` to setup my Redshift Cluster. If you would like to follow along using `awscli`, make sure that you have first installed the CLI as well as configured it for use with your account by running `aws configure` after installation.  

First, I run a command like the one below (make sure to replace all variables in [] with your actual names and passwords) (and additionally, please make sure to attach the correct vpc-security-group and iam-role for your AWS console as created from following the Udacity classroom instructions): 
```
aws redshift create-cluster --cluster-identifier [CLUSTERNAME] --master-username [USERNAME] --master-user-password [SECRETPW] --node-type dc2.large --cluster-type multi-node --number-of-nodes 4 --iam-roles arn:aws:iam::848672232758:role/myRedshiftRole --vpc-security-group-ids sg-054b11e9abce542e3
``` 
This will create a 2-node cluster in AWS for you, and you can check the status of the cluster by running `aws redshift describe-clusters`

Finally, when you are done with the exercise, you can delete the cluster via:

```
aws redshift delete-cluster --cluster-identifier [CLUSTERNAME] --skip-final-cluster-snapshot
```

## ETL Pipeline
This project transforms multiple JSON files stored in S3 into staging tables in Redshift as well as a star-schema based set of dimension tables and a fact table.  
The files are stored in S3 consist of two schemas: one for SONG tracks based off of a subset from the Million Song Dataset, and the second set of files being a running log of user listening events on the song app. 
To create this pipeline of lifting the files from S3 to Redshift, we run three Python scripts:
* sql_queries.py : which constructs all of the DDLs and the INSERT statements for the star-schema warehouse.
* create_table.py : which takes the drop and create statements from the previous python file and executes them against the Redshift endpoint in AWS. 
* etl.py : which loads the data from S3, using parallel COPY, and then performs the ETL's for INSERT to create the star-schema tables. 

## Instructions
* clone this repository and make sure that you have done the important step in the setup step, which includes the AWSCLI command for creating a 4-node cluster in Redshift, located in the US-West-2 region. 
* cd into this repository and run `python create_tables.py`
* OPTIONAL: feel free to use the query editor in AWS Console or any other SQL Client to check the tables created
* run `python etl.py` to load the data and ensure that it ran without errors
* OPTIONAL: check the DIM and FACT tables by using Query Editor or any other Postgres compatible SQL Client


