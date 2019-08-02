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

