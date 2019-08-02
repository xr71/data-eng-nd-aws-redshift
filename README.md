# Udacity Project - AWS Redshift Cloud Data Warehouse

## Introduction

## Setup
I am using the `awscli` to setup my Redshift Cluster. If you would like to follow along using `awscli`, make sure that you have first installed the CLI as well as configured it for use with your account by running `aws configure` after installation.  

First, I run a command like the one below (make sure to replace all variables in [] with your actual names and passwords): 
```
aws redshift create-cluster --cluster-identifier [CLUSTERNAME] --master-username [USERNAME] --master-user-password [SECRETPW] --node-type dc2.large --cluster-type multi-node --number-of-nodes 2
``` 
