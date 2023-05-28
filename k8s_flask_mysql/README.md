# Kubernetes Deployment of Flask Application with MySQL Database

## Overview
This project is a simple Kubernetes setup for deploying a Flask application with a MySQL database backend. The Flask application is containerized using Docker and served using a Kubernetes service. The MySQL database is also containerized and deployed as a separate service in the same Kubernetes cluster. This document provides a guide on how to deploy and manage the project using Minikube on a local machine.
這個項目是一個簡單的 Kubernetes 設置，用於部署帶有 MySQL 數據庫後端的 Flask 應用程序。 Flask 應用程序使用 Docker 進行容器化，並使用 Kubernetes 服務提供服務。 MySQL 數據庫也被容器化並作為單獨的服務部署在同一個 Kubernetes 集群中。本文檔提供了有關如何在本地計算機上使用 Minikube 部署和管理項目的指南。


## Project Structure
```
.
├── README.md
├── flask
│   └── flask-deployment.yaml
└── mysql
    ├── mysql-configmap.yaml
    ├── mysql-deployment.yaml
    ├── mysql-pvc.yaml
    ├── mysql-secret.yaml
    └── mysql-service.yaml
```

## Pre-requisites
* Install [Docker](https://docs.docker.com/get-docker/)
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
* Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)

## Environment Setup
Before proceeding with the deployment, you'll need to set up some environment variables. Create a .env file with the following content:

```.env
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DATABASE=shop
```

## Configuration Files Description 
Each configuration file serves a unique purpose and plays a crucial role in the deployment process.

**Flask**
* `flask-deployment.yaml`: This file contains the Kubernetes deployment and service configuration for the Flask application.

**MySQL**
* `mysql-configmap.yaml`: This file contains the configuration data for MySQL. It creates a database and populates it with some initial data.
* `mysql-deployment.yaml`: This file is responsible for deploying the MySQL database on Kubernetes.
* `mysql-pvc.yaml`: This file outlines the Persistent Volume Claim (PVC) for MySQL data. It provides storage for the MySQL data.
* `mysql-secret.yaml`: This file stores sensitive data for the MySQL database such as the root password.
* `mysql-service.yaml`: This file defines the service that makes MySQL accessible within the cluster.

## Deployment Steps
To deploy the Flask application and MySQL database on your Minikube cluster, follow these steps:

Start Minikube by running the command minikube start.
Apply the Kubernetes configuration files in the following order:

1. Start Minikube with the command `minikube start`.
2. Navigate to the root directory of the project.
3. Deploy the MySQL database:
```bash
#Apply the secret for MySQL: 
kubectl apply -f mysql/mysql-secret.yaml
#Apply the ConfigMap for MySQL: 
kubectl apply -f mysql/mysql-configmap.yaml
# Set up the Persistent Volume Claim: 
kubectl apply -f mysql/mysql-pvc.yaml
# Deploy MySQL: 
kubectl apply -f mysql/mysql-deployment.yaml
# Apply the service: 
kubectl apply -f mysql/mysql-service.yaml
```
4. Once the MySQL service is up and running, deploy the Flask application: `kubectl apply -f flask/ flask-deployment.yaml`
   
These commands will create a MySQL database and a Flask application running in your Minikube cluster.


5. Since the Flask service is of type `LoadBalancer` and **Minikube doesn't support `LoadBalancer` Services out of the box**, we'll use `kubectl port-forward` to access the Flask application. Find the name of the Flask app pod by running `kubectl get pods`, then port-forward traffic from a local port (for example, 8080) to the port your Flask application is running on inside the cluster (8000):

```bash
kubectl port-forward pod/<your-flask-pod> 8080:8000
```
Replace <your-flask-pod> with the name of your Flask application pod. Now, you should be able to access your Flask application at `http://localhost:8080`.

6. Check the status of the deployments and services with `kubectl get pods,svc`.

After following these steps, both the Flask application and the MySQL database should be running on your Minikube cluster. You can access the application using the Minikube IP and the NodePort of the Flask service. You can obtain the Minikube IP with the command `minikube ip`, and the NodePort using `kubectl get svc`.
完成這些步驟後，Flask 應用程序和 MySQL 數據庫都應該在您的 Minikube 集群上運行。您可以使用 Minikube IP 和 Flask 服務的 NodePort 訪問應用程序。您可以使用命令 minikube ip 獲取 Minikube IP，使用 kubectl get svc 獲取 NodePort。


## Accessing the MySQL Database
To access the MySQL database and check the data:

1. Get the MySQL pod name using `kubectl get pods`.
2. Connect to the MySQL shell using `kubectl exec`. Replace <your-mysql-pod> with the name of your MySQL pod:

```bash
kubectl exec -it <your-mysql-pod> -- mysql -u root -p
```
3. When prompted, enter the MySQL root password. You can find this in the `mysql-secret.yam`l` file.
4. Now, you should be connected to your MySQL server. You can list all databases with the command `SHOW DATABASES;`
5. To select the 'shop' database, use the command `USE shop`;
6. To check the contents of the 'users' table, use `SELECT * FROM users;`
   
Remember to exit the MySQL shell using the command `exit` when you're done.